from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .config import Settings, addon_dir, freecad_bin, mac_mod_dir
from .rpc import FreeCADRPCClient


def _print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def client_from(args) -> FreeCADRPCClient:
    return FreeCADRPCClient(host=args.host, port=args.port)


def build_parser() -> argparse.ArgumentParser:
    settings = Settings()
    p = argparse.ArgumentParser(prog="fc", description="FreeCAD local CLI over freecad-mcp RPC")
    p.add_argument("--host", default=settings.host)
    p.add_argument("--port", default=settings.port, type=int)
    sub = p.add_subparsers(dest="group", required=True)

    sub.add_parser("ping")
    sub.add_parser("status")
    sub.add_parser("doctor")

    addon = sub.add_parser("addon")
    addon_sub = addon.add_subparsers(dest="addon_cmd", required=True)
    addon_install = addon_sub.add_parser("install")
    addon_install.add_argument("--repo", default=settings.mcp_repo)
    addon_install.add_argument("--ref", default=settings.mcp_ref)
    addon_install.add_argument("--mod-dir", default=str(mac_mod_dir()))
    addon_sub.add_parser("path")
    addon_sub.add_parser("status")

    doc = sub.add_parser("doc")
    doc_sub = doc.add_subparsers(dest="doc_cmd", required=True)
    doc_create = doc_sub.add_parser("create")
    doc_create.add_argument("name")
    doc_sub.add_parser("list")
    doc_objects = doc_sub.add_parser("objects")
    doc_objects.add_argument("document")

    run = sub.add_parser("run")
    run.add_argument("python_file")

    screenshot = sub.add_parser("screenshot")
    screenshot.add_argument("output")
    screenshot.add_argument("--view", default="Isometric")
    screenshot.add_argument("--width", type=int)
    screenshot.add_argument("--height", type=int)
    screenshot.add_argument("--focus-object")

    export = sub.add_parser("export")
    export.add_argument("kind", choices=["step", "stl"])
    export.add_argument("document")
    export.add_argument("output")
    export.add_argument("--object", action="append", dest="objects")

    return p


def cmd_ping(args) -> int:
    ok = client_from(args).ping()
    print("ok" if ok else "fail")
    return 0 if ok else 1


def cmd_status(args) -> int:
    c = client_from(args)
    _print_json({"host": args.host, "port": args.port, "online": c.ping(), "documents": c.list_documents()})
    return 0


def cmd_doctor(args) -> int:
    adir = addon_dir()
    report = {
        "freecad_app": Settings().freecad_app,
        "freecad_bin": str(freecad_bin()),
        "freecad_bin_exists": freecad_bin().exists(),
        "mod_dir": str(mac_mod_dir()),
        "mod_dir_exists": mac_mod_dir().exists(),
        "addon_dir": str(adir),
        "addon_installed": adir.exists(),
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
    return 0


def cmd_addon_install(args) -> int:
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
    print(addon_dir())
    return 0


def cmd_addon_status(args) -> int:
    adir = addon_dir()
    _print_json({"addon_dir": str(adir), "installed": adir.exists()})
    return 0


def cmd_doc_create(args) -> int:
    _print_json(client_from(args).create_document(args.name))
    return 0


def cmd_doc_list(args) -> int:
    _print_json(client_from(args).list_documents())
    return 0


def cmd_doc_objects(args) -> int:
    _print_json(client_from(args).get_objects(args.document))
    return 0


def cmd_run(args) -> int:
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


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.group == "ping":
            return cmd_ping(args)
        if args.group == "status":
            return cmd_status(args)
        if args.group == "doctor":
            return cmd_doctor(args)
        if args.group == "addon":
            return {
                "install": cmd_addon_install,
                "path": cmd_addon_path,
                "status": cmd_addon_status,
            }[args.addon_cmd](args)
        if args.group == "doc":
            return {
                "create": cmd_doc_create,
                "list": cmd_doc_list,
                "objects": cmd_doc_objects,
            }[args.doc_cmd](args)
        if args.group == "run":
            return cmd_run(args)
        if args.group == "screenshot":
            return cmd_screenshot(args)
        if args.group == "export":
            return cmd_export(args)
        raise ValueError(f"Unknown command group: {args.group}")
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
