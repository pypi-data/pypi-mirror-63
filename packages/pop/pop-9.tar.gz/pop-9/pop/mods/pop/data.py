import collections.abc as abc
import inspect
import logging
import pop.contract as contract
import sys
from typing import Any, Coroutine, Dict, Iterable, Iterator

log = logging.getLogger(__name__)

__func_alias__ = {
    "immutable_namespaced_map": "imap",
    "mutable_namespaced_map": "map",
    "dynamic_mutable_namespaced_map": "dmap",
}


def immutable_namespaced_map(hub, init: Dict[str, Any], **kwargs) -> abc.MutableMapping:
    class IMAP(abc.MutableMapping):
        """
        An abstract base class that implements the interface of a `dict` but is immutable.
        Items can be retrieved via namespacing.
        No values can be changed after initialization
        """

        def __init__(self, init_: Dict[str, Any], **c_kwargs):
            """
            :param init_: A dictionary from which to inherit data
            """
            init_.update(**c_kwargs)
            values = {}
            for k, v in init_.items():
                if isinstance(v, Dict):
                    values[k] = IMAP(init_=v)
                elif isinstance(v, (tuple, int, str, bytes)):
                    values[k] = v
                elif isinstance(v, Iterable):
                    values[k] = tuple(v)
                else:
                    values[k] = v
            # __setattr__ is borked (on purpose) so we have to call it from super() right here
            super().__setattr__("_IMAP__store", values)
            log.debug("Initialized immutable namespaced map")

        def __delitem__(self, k: str):
            raise TypeError(f"{self.__class__.__name__} does not support item deletion")

        def __setitem__(self, k: str, v: Any):
            raise TypeError(
                f"{self.__class__.__name__} does not support item assignment"
            )

        def __setattr__(self, k: str, v: Any):
            raise TypeError(
                f"{self.__class__.__name__} does not support attribute assignment"
            )

        def __getattr__(self, k: str):
            return self.__store[k]

        def __getitem__(self, k: str) -> Any:
            return self.__store[k]

        def __contains__(self, k: str) -> bool:
            return k in self.__store

        def __iter__(self):
            return iter(self.__store)

        def __len__(self) -> int:
            return len(self.__store.keys())

        def __unpack(self) -> Dict[str, Any]:
            ret = {}
            # Unpack IMAP items so that it's turtles all the way down
            for k, v in self.items():
                if isinstance(v, IMAP):
                    ret[k] = dict(v)
                else:
                    ret[k] = v
            return ret

        def __str__(self):
            return str(self.__unpack())

    return IMAP(init_=init, **kwargs)


def mutable_namespaced_map(
    hub, init: Dict[str, Any] = None, **kwargs
) -> abc.MutableMapping:
    class MAP(abc.MutableMapping):
        """
        :param init: A dictionary from which to inherit data

        An abstract base class that implements the interface of a `dict`
        Items can be set and retrieved via namespacing
        """

        def __init__(self, init_: Dict[str, Any] = None, **c_kwargs):
            self._store = dict(**c_kwargs)
            if init_:
                assert isinstance(init_, Dict)
                # Existing dictionaries might have values that need wrapped as well
                self.update(init_)

        def __setitem__(self, k: str, v: Any):
            """
            Cast all nested dict values as MAP so they get it's benefits as well
            """
            if isinstance(v, Dict):
                v = MAP(v)
            self._store[k] = v

        def __delitem__(self, k: str):
            """
            Cleanup method required by abc.ABC
            """
            if k in self._store:
                del self._store[k]

        def __getitem__(self, k: str) -> Any:
            return self._store[k]

        def __getattr__(self, k: str) -> Any:
            """
            Return dict values on the MAP namespace
            Create the key if it doesn't exist
            """
            if k.startswith("_"):
                return getattr(super(), k)
            try:
                if k not in self._store:
                    self.__setitem__(k, MAP())
                return self[k]
            except Exception as e:
                raise AttributeError(*e.args)

        def __setattr__(self, k: str, v: Any):
            # Don't allow underscored keys to be put in the store
            if k.startswith("_"):
                super().__setattr__(k, v)
            else:
                self[k] = v

        def __len__(self) -> int:
            return len(self._store)

        def __iter__(self) -> Iterator[Any]:
            return iter(self._store)

        def __str__(self) -> str:
            return str(self._store)

    return MAP(init, **kwargs)


def dynamic_mutable_namespaced_map(
    hub, init: Dict[str, Any] = None, ref: contract.Contracted = None, **kwargs,
) -> abc.MutableMapping:
    class DMAP(abc.MutableMapping):
        """
        :param init: A dictionary from which to inherit data

        An abstract base class that implements the interface of a `dict`

        Stores references to functions that generate the given keys
        When "refresh" is called the reference function is called again
          .. example
            def init(hub):
                hub.grains.GRAINS = hub.pop.data.dmap()

            def load_grain(hub):
                hub.grains.GRAINS.key = "value"

            def exec_module(hub):
                hub.grains.GRAINS.refresh("key")
        """

        def __init__(
            self,
            init_: Dict[str, Any] = None,
            ref_: contract.Contracted = None,
            **c_kwargs,
        ):
            """
            :param init_: A dictionary from which to inherit data
            """
            self._store = dict(**c_kwargs)
            self._parent_ref = ref_ or ref
            # A reference for the functions that created this value
            self._ref = {}
            if init_:
                # Existing dictionaries might have properties that need wrapped as well
                self.update(init_)

        def refresh(self, k: str = None) -> None or Coroutine:
            """
            Call the underlying function that generated a grain,
            If the underlying function was a coroutine, return the awaitable
            """
            # If a key was supplied then call it's ref
            if k in self._ref:
                return self._ref[k]()
            # If refresh was called on this object then access the parent ref
            elif self._parent_ref is not None:
                return self._parent_ref()
            else:
                raise KeyError(
                    f"No function found for '{k}'. Try creating this dmap with a ref"
                )

        def __get_caller(self) -> contract.Contracted:
            """
            This function allows for hub to pop introspective calls.
            This should only ever be called from within a hub module, otherwise
            it should stack trace, or return heaven knows what...
            """
            # Nested values might share a contracted function
            if self._parent_ref is not None:
                return self._parent_ref

            for f in range(3, 20):
                if hasattr(sys, "_getframe"):
                    # implementation detail of CPython, speeds things up by 100x.
                    call_frame = sys._getframe(f)
                else:
                    call_frame = inspect.stack(context=0)[f].frame
                if isinstance(call_frame.f_locals.get("self"), contract.Contracted):
                    break
            contracted = call_frame.f_locals["self"]
            log.debug(f"Found contract '{contracted.name}'")
            return contracted

        def __setitem(self, k: str, v: Any):
            """
            This needs to exist so that __setattr__ and __setitem__ get the caller at the same level
            """
            # Find the calling function on the hub and store it in the cache
            if k not in self._ref:
                log.debug(f"Finding contract for grain '{k}'")
                self._ref[k] = self.__get_caller()

            if isinstance(v, dict):
                # Cast all nested dict values as DMAP so they get it's benefits as well
                # Contracts are shared between nested items until they are overridden
                v = DMAP(init_=v, ref_=self._ref[k])
                self._store[k] = v
            else:
                self._store[k] = v

        def __setitem__(self, k: str, v: Any):
            self.__setitem(k, v)

        def __delitem__(self, k: str):
            """
            Cleanup method required by abc.ABC
            """
            if k in self._store:
                del self._store[k]
            if k in self._ref:
                del self._ref[k]

        def __getitem__(self, k: str) -> Any:
            return self._store[k]

        def __getattr__(self, k: str) -> Any:
            """
            Return dict values on the GRAINS namespace
            Create the key if it doesn't exist, this allows nested grains to be created in any order
            i.e. hub.grains.GRAINS.dict_grain.value = property(func)
            """
            # Do not allow underscored keys to be accessed through the namespace
            if k.startswith("_"):
                return super().__getattr__(k)
            try:
                if k not in self._store:
                    self.__setitem(k, DMAP())
                return self[k]
            except Exception as e:
                raise AttributeError(*e.args)

        def __setattr__(self, k: str, v: Any):
            # Don't allow underscored keys to be put in the store
            if k.startswith("_"):
                super().__setattr__(k, v)
            else:
                self.__setitem(k, v)

        def __len__(self) -> int:
            return len(self._store)

        def __iter__(self) -> Iterator[Any]:
            return iter(self._store)

        def __str__(self) -> str:
            return str(self._store)

    return DMAP(init_=init, ref_=ref, **kwargs)
