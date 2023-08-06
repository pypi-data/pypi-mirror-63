from .moviewalker import MovieWalker  # noqa: F401

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version("shishakai")
