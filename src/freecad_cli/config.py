from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_HOST = os.environ.get("FREECAD_RPC_HOST", "localhost")
DEFAULT_PORT = int(os.environ.get("FREECAD_RPC_PORT", "9875"))
DEFAULT_FREECAD_APP = os.environ.get("FREECAD_APP", "/Applications/FreeCAD.app")
DEFAULT_MCP_REPO = os.environ.get("FREECAD_MCP_REPO", "https://github.com/neka-nat/freecad-mcp.git")


def mac_mod_dir() -> Path:
    return Path.home() / "Library/Application Support/FreeCAD/Mod"


@dataclass
class Settings:
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    freecad_app: str = DEFAULT_FREECAD_APP
    mcp_repo: str = DEFAULT_MCP_REPO
