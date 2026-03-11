from __future__ import annotations

import base64
import textwrap
import xmlrpc.client
from pathlib import Path
from typing import Any


class FreeCADRPCClient:
    def __init__(self, host: str = "localhost", port: int = 9875):
        self.host = host
        self.port = port
        self.server = xmlrpc.client.ServerProxy(f"http://{host}:{port}", allow_none=True)

    def ping(self) -> bool:
        return bool(self.server.ping())

    def list_documents(self) -> list[str]:
        return list(self.server.list_documents())

    def create_document(self, name: str) -> dict[str, Any]:
        return dict(self.server.create_document(name))

    def get_objects(self, doc_name: str) -> list[dict[str, Any]]:
        return list(self.server.get_objects(doc_name))

    def execute_code(self, code: str) -> dict[str, Any]:
        return dict(self.server.execute_code(code))

    def screenshot(self, output: str | Path, view: str = "Isometric", width: int | None = None, height: int | None = None, focus_object: str | None = None) -> Path:
        data = self.server.get_active_screenshot(view, width, height, focus_object)
        if not data:
            raise RuntimeError("No screenshot returned from FreeCAD")
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(data))
        return out

    def export_document(self, doc_name: str, output: str | Path, kind: str, object_names: list[str] | None = None) -> dict[str, Any]:
        output = str(Path(output).expanduser().resolve())
        quoted = repr(output)
        obj_filter = repr(object_names) if object_names else "None"
        code = textwrap.dedent(f"""
        import FreeCAD as App
        import Part
        doc = App.getDocument({doc_name!r})
        if doc is None:
            raise ValueError(f'Document not found: {doc_name}')
        names = {obj_filter}
        objs = [doc.getObject(n) for n in names] if names else list(doc.Objects)
        objs = [o for o in objs if o is not None]
        if not objs:
            raise ValueError('No exportable objects found')
        if {kind!r} == 'step':
            Part.export(objs, {quoted})
        elif {kind!r} == 'stl':
            if len(objs) == 1:
                objs[0].Shape.exportStl({quoted})
            else:
                import Mesh
                Mesh.export(objs, {quoted})
        else:
            raise ValueError('Unsupported export kind')
        print({quoted})
        """)
        return self.execute_code(code)
