"""Permissive stand-in for the ``mega`` module (MEGA SDK python bindings).

The real module is compiled C++ bindings and is only shipped inside the
official WZML-X docker image — it is not on PyPI, so a Colab/host install
cannot have it. The bot imports it unconditionally at startup
(``bot/helper/listeners/task_listener.py`` -> ``mega_upload``), so without
this file the whole process dies with ``ModuleNotFoundError: No module named
'mega'``.

What this stub does:

* makes every ``from mega import MegaApi, MegaError, ...`` succeed, so the
  bot can start and every non-Mega feature works normally;
* returns unique int-like constants for things like
  ``MegaRequest.TYPE_LOGIN``, so nothing is accidentally "equal" to something
  else;
* raises a clear ``RuntimeError`` the moment anything actually tries to use
  the SDK (``MegaApi(...)``, ``MegaUploadOptions.createInstance()``, ...).

Keep ``DISABLE_MEGA = True`` in ``config.py`` so Mega links are rejected with a
friendly message instead of hitting that RuntimeError. The notebook copies this
file into the repo root as ``mega.py`` only when the real module is missing.
"""

_MSG = (
    "MEGA support is unavailable in this build: the 'mega' SDK python bindings "
    "ship only inside the official WZML-X docker image. Set DISABLE_MEGA = True "
    "(Mega links are rejected cleanly) or deploy with Docker."
)

_counter = [0]


class _Constant(int):
    """Int-like value that is unique per attribute and explodes when called."""

    def __new__(cls, path, value):
        obj = int.__new__(cls, value)
        obj._path = path
        return obj

    def __getattr__(self, item):
        return _constant(f"{self._path}.{item}")

    def __call__(self, *args, **kwargs):
        raise RuntimeError(_MSG)

    def __repr__(self):
        return f"<mega stub {self._path}>"


def _constant(path):
    _counter[0] += 1
    return _Constant(path, _counter[0])


class _StubMeta(type):
    def __getattr__(cls, item):
        if item.startswith("__"):
            raise AttributeError(item)
        return _constant(f"{cls.__name__}.{item}")


class MegaListener(metaclass=_StubMeta):
    def __init__(self, *args, **kwargs):
        pass


class MegaError(metaclass=_StubMeta):
    def __init__(self, *args, **kwargs):
        pass

    def toString(self):
        return _MSG

    def getErrorCode(self):
        return 0

    def __str__(self):
        return _MSG


class MegaRequest(metaclass=_StubMeta):
    pass


class MegaTransfer(metaclass=_StubMeta):
    pass


class MegaUploadOptions(metaclass=_StubMeta):
    pass


class MegaApi(metaclass=_StubMeta):
    def __init__(self, *args, **kwargs):
        raise RuntimeError(_MSG)


# The bot checks ``if MegaCancelToken is None`` and skips cancellation support,
# which is exactly what we want.
MegaCancelToken = None

SDK_STUB = True
