# -*- coding: utf-8 -*-
"""
The pop top level module
"""

# Import python libs
import os

INSTALL_DIR = os.path.dirname(os.path.realpath(__file__))


# ----- Detect System Encoding -------------------------------------------------------------------------------------->
# This will install a globally available variable which will hold the detected encoding
def __define_global_system_encoding_variable__():
    import sys

    # sys.stdin.encoding is the most trustworthy source of the system encoding, though, if
    # pop is being imported after being daemonized, this information is lost and reset to None
    encoding = None

    if not sys.platform.startswith("win") and sys.stdin is not None:
        # On linux we can rely on sys.stdin for the encoding since it
        # most commonly matches the filesystem encoding. This however
        # does not apply to windows
        encoding = sys.stdin.encoding

    if not encoding:
        # If the system is properly configured this should return a valid
        # encoding. MS Windows has problems with this and reports the wrong
        # encoding
        import locale

        try:
            encoding = locale.getdefaultlocale()[-1]
        except ValueError:
            # A bad locale setting was most likely found:
            #   https://github.com/saltstack/salt/issues/26063
            pass

        # This is now garbage collectible
        del locale

        if not encoding:
            if sys.platform.startswith("darwin"):
                # Mac OS X uses UTF-8
                encoding = "utf-8"
            elif sys.platform.startswith("win"):
                # Windows uses a configurable encoding; on Windows, Python uses the name “mbcs”
                # to refer to whatever the currently configured encoding is.
                encoding = "mbcs"
            else:
                # This is most likely ascii which is not the best but we were
                # unable to find a better encoding. If this fails, we fall all
                # the way back to ascii
                # On linux default to ascii as a last resort
                encoding = sys.getdefaultencoding() or "ascii"

    try:
        # Return the detected encoding
        return encoding
    finally:
        # This is now garbage collectible
        del sys
        del encoding


PACK_SYSTEM_ENCODING = __define_global_system_encoding_variable__()

# This is now garbage collectible
del __define_global_system_encoding_variable__
# <---- Detect System Encoding ---------------------------------------------------------------------------------------
