from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .config import Settings, mac_mod_dir
from .rpc import FreeCADRPCClient


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fc", description="FreeCAD local CLI over freecad-mcp RPC")
    p.add_argument("--host", default=Settings().host)
    p.add_argument("--port", default=Settings().port, type=int)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("ping")
    sub.add_parser("status")
    sub.add_parser("doctor")

    cdoc = sub.add_parser("create-document")
    cdoc.add_argument("name")

    lobj = sub.add_parser("list-objects")
    lobj.add_argument("document")

    ex = sub.add_parser("exec")
    ex.add_argument("python_file")

    shot = sub.add_parser("screenshot")
    shot.add_argument("output")
    shot.add_argument("--view", default="Isometric")
    shot.add_argument("--width", type=int)
    shot.add_argument("--height", type=int)
    shot.add_argument("--focus-object")

    export = sub.add_parser("export")
    export.add_argument("kind", choices=["step", "stl"])
    export.add_argument("document")
    export.add_argument("output")
    export.add_argument("--object", action="append", dest="objects")

    addon = sub.add_parser("install-addon")
    addon.add_argument("--repo", default=Settings().mcp_repo)
    addon.add_argument("--ref", default="main")
    addon.add_argument("--mod-dir", default=str(mac_mod_dir()))

    sub.add_parser("addon-path")
    return p


def client_from(args) -> FreeCADRPCClient:
    return FreeCADRPCClient(host=args.host, port=args.port)


def _print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_ping(args) -> int:
    ok = client_from(args).ping()
    print("ok" if ok else "fail")
    return 0 if ok else 1


def cmd_status(args) -> int:
    c = client_from(args)
    docs = c.list_documents()
    _print_json({"host": args.host, "port": args.port, "online": c.ping(), "documents": docs})
    return 0


def cmd_doctor(args) -> int:
    mod_dir = mac_mod_dir()
    addon_dir = mod_dir / "FreeCADMCP"
    freecad_bin = Path(Settings().freecad_app) / "Contents/MacOS/FreeCAD"
    report = {
        "freecad_app": Settings().freecad_app,
        "freecad_bin_exists": freecad_bin.exists(),
        "mod_dir": str(mod_dir),
        "mod_dir_exists": mod_dir.exists(),
        "addon_dir": str(addon_dir),
        "addon_installed": addon_dir.exists(),
        "rpc_host": args.host,
        "rpc_port": args.port,
        "rpc_online": False,
        "documents": [],
    }
    try:
        c = client_from(args)
        report["rpc_online"] = c.ping()
        if report["rpc_online"]:
            report["documents"] = c.list_documents()
    except Exception as e:
        report["rpc_error"] = str(e)
    _print_json(report)
    return 0 if report["freecad_bin_exists"] else 1


def cmd_create_document(args) -> int:
    _print_json(client_from(args).create_document(args.name))
    return 0


def cmd_list_objects(args) -> int:
    _print_json(client_from(args).get_objects(args.document))
    return 0


def cmd_exec(args) -> int:
    code = Path(args.python_file).read_text()
    _print_json(client_from(args).execute_code(code))
    return 0


def cmd_screenshot(args) -> int:
    out = client_from(args).screenshot(args.output, view=args.view, width=args.width, height=args.height, focus_object=args.focus_object)
    print(out)
    return 0


def cmd_export(args) -> int:
    _print_json(client_from(args).export_document(args.document, args.output, args.kind, args.objects))
    return 0


def cmd_install_addon(args) -> int:
    mod_dir = Path(args.mod_dir).expanduser()
    mod_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="freecad-mcp-") as td:
        repo = Path(td) / "repo"
        subprocess.run(["git", "clone", "--depth=1", "--branch", args.ref, args.repo, str(repo)], check=True)
        src = repo / "addon" / "FreeCADMCP"
        dst = mod_dir / "FreeCADMCP"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(dst)
    return 0


def cmd_addon_path(args) -> int:
    print(mac_mod_dir() / "FreeCADMCP")
    return 0


def main() -> int:
    args = build_parser().parse_args()
    try:
        return {
            "ping": cmd_ping,
            "status": cmd_status,
            "doctor": cmd_doctor,
            "create-document": cmd_create_document,
            "list-objects": cmd_list_objects,
            "exec": cmd_exec,
            "screenshot": cmd_screenshot,
            "export": cmd_export,
            "install-addon": cmd_install_addon,
            "addon-path": cmd_addon_path,
        }[args.cmd](args)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
