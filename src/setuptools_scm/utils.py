"""
utils
"""
from __future__ import annotations

import logging
import subprocess
import textwrap
import warnings
from pathlib import Path
from typing import Sequence
from typing import TYPE_CHECKING

from . import _run_cmd

if TYPE_CHECKING:
    from . import _types as _t

log = logging.getLogger(__name__)


def data_from_mime(path: _t.PathT) -> dict[str, str]:
    content = Path(path).read_text(encoding="utf-8")
    log.debug("mime %s content:\n%s", path, textwrap.indent(content, "    "))
    # the complex conditions come from reading pseudo-mime-messages
    data = dict(x.split(": ", 1) for x in content.splitlines() if ": " in x)

    log.debug("mime %s data:\n%s", path, data)
    return data


def has_command(name: str, args: Sequence[str] = ["help"], warn: bool = True) -> bool:
    try:
        p = _run_cmd.run([name, *args], cwd=".", timeout=5)
    except OSError as e:
        log.warning("command %s missing: %s", name, e)
        res = False
    except subprocess.TimeoutExpired as e:
        log.warning("command %s timed out %s", name, e)
        res = False

    else:
        res = not p.returncode
    if not res and warn:
        warnings.warn("%r was not found" % name, category=RuntimeWarning)
    return res


def require_command(name: str) -> None:
    if not has_command(name, warn=False):
        raise OSError(f"{name!r} was not found")
