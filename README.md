# freecad-cli

A local CLI wrapper for controlling macOS FreeCAD through the `freecad-mcp` addon RPC server, without Docker.

## Architecture

```text
fc CLI -> XML-RPC (localhost:9875) -> freecad-mcp addon -> FreeCAD
```

This project does **not** talk to the standalone `freecad-mcp` MCP server directly.
It reuses the same FreeCAD addon/RPC layer that `freecad-mcp` depends on, then wraps it in a local CLI.

## MVP commands

- `fc install-addon`
- `fc addon-path`
- `fc ping`
- `fc status`
- `fc doctor`
- `fc create-document NAME`
- `fc list-objects DOC`
- `fc exec script.py`
- `fc screenshot out.png`
- `fc export step DOC out.step`
- `fc export stl DOC out.stl`

## Install

```bash
cd freecad-cli
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Quickstart (tested on this Mac)

1. Install addon:

```bash
fc install-addon
```

2. Restart FreeCAD.
3. In FreeCAD, switch to **MCP Addon** workbench.
4. Click **Start RPC Server**.
5. Verify:

```bash
fc doctor
fc ping
fc status
```

## Alternative: start RPC from a FreeCAD script

This was validated locally too. Example:

```python
import sys, time
sys.path.insert(0, '/Users/cai/Library/Application Support/FreeCAD/Mod/FreeCADMCP')
from rpc_server.rpc_server import start_rpc_server
print(start_rpc_server())
time.sleep(20)
```

Run with:

```bash
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD /path/to/script.py
```

## Example session

```bash
fc create-document demo
fc exec ./box.py
fc list-objects demo
fc screenshot ./demo.png
fc export step demo ./demo.step
fc export stl demo ./demo.stl
```

## Notes

- Default host/port: `localhost:9875`
- Override with `--host` and `--port`
- `export` is currently implemented by sending Python through `execute_code`
- `screenshot` depends on current active FreeCAD view supporting image capture
- This is an MVP intended to make FreeCAD scriptable like `gh`-style local CLIs

## Common failure cases

- `Connection refused` on `9875`: RPC server not started in FreeCAD
- `fc ping` fails: addon missing, wrong host/port, or FreeCAD not running with RPC
- `screenshot` fails: current active view does not support screenshots
- `install-addon` succeeds but toolbar missing: restart FreeCAD
