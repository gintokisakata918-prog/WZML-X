"""Minimal stand-in for the ``wz_bin`` helper that ships inside the official
WZML-X docker image.

The image keeps aria2c / qbittorrent-nox / ffmpeg / rclone / sabnzbdplus in a
private prefix and ``wz_bin.bin_name()`` returns their absolute paths. On
Colab those binaries come from apt and live on ``PATH``, so returning the
plain command name (or the absolute path found by ``shutil.which``) is enough.

You can override any of them with an environment variable:

    WZ_ARIA2 / WZ_QBIT / WZ_FFMPEG / WZ_RCLONE / WZ_SABNZBD

The notebook copies this file into the repository root as ``wz_bin.py`` so it
shadows the one that is normally installed inside the image.
"""

import os
import shutil

_BINARIES = (
    ("WZ_ARIA2", "aria2c"),
    ("WZ_QBIT", "qbittorrent-nox"),
    ("WZ_FFMPEG", "ffmpeg"),
    ("WZ_RCLONE", "rclone"),
    ("WZ_SABNZBD", "sabnzbdplus"),
)


def bin_name(index: int) -> str:
    """Return the command/path to use for binary number ``index``."""
    env_key, default = _BINARIES[index]
    override = os.environ.get(env_key)
    if override:
        return override
    return shutil.which(default) or default


def bin_path(index: int) -> str:
    """Alias kept for code that expects a path-style accessor."""
    return bin_name(index)
