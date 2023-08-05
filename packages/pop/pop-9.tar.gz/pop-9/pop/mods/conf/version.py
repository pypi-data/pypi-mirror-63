"""
Support embedding version number lookup into cli
"""
# IMport python libs
import importlib
import sys


CONFIG = {
    "version": {
        "default": False,
        "action": "store_true",
        "help": "Display version information",
    }
}


def run(hub, primary):
    """
    Check the version number and then exit
    """
    mod = importlib.import_module(f"{primary}.version")
    print(f"{primary} {mod.version}")
    sys.exit(0)
