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

    def create_box(self, doc_name: str, obj_name: str, length: float, width: float, height: float, x: float = 0, y: float = 0, z: float = 0) -> dict[str, Any]:
        code = textwrap.dedent(f"""
        import FreeCAD as App
        doc = App.getDocument({doc_name!r})
        if doc is None:
            raise ValueError(f'Document not found: {doc_name}')
        obj = doc.getObject({obj_name!r})
        if obj is None:
            obj = doc.addObject('Part::Box', {obj_name!r})
        obj.Length = {float(length)!r}
        obj.Width = {float(width)!r}
        obj.Height = {float(height)!r}
        obj.Placement.Base = App.Vector({float(x)!r}, {float(y)!r}, {float(z)!r})
        doc.recompute()
        print(obj.Name)
        """)
        return self.execute_code(code)

    def create_cylinder(self, doc_name: str, obj_name: str, radius: float, height: float, x: float = 0, y: float = 0, z: float = 0) -> dict[str, Any]:
        code = textwrap.dedent(f"""
        import FreeCAD as App
        doc = App.getDocument({doc_name!r})
        if doc is None:
            raise ValueError(f'Document not found: {doc_name}')
        obj = doc.getObject({obj_name!r})
        if obj is None:
            obj = doc.addObject('Part::Cylinder', {obj_name!r})
        obj.Radius = {float(radius)!r}
        obj.Height = {float(height)!r}
        obj.Placement.Base = App.Vector({float(x)!r}, {float(y)!r}, {float(z)!r})
        doc.recompute()
        print(obj.Name)
        """)
        return self.execute_code(code)

    def create_sphere(self, doc_name: str, obj_name: str, radius: float, x: float = 0, y: float = 0, z: float = 0) -> dict[str, Any]:
        code = textwrap.dedent(f"""
        import FreeCAD as App
        doc = App.getDocument({doc_name!r})
        if doc is None:
            raise ValueError(f'Document not found: {doc_name}')
        obj = doc.getObject({obj_name!r})
        if obj is None:
            obj = doc.addObject('Part::Sphere', {obj_name!r})
        obj.Radius = {float(radius)!r}
        obj.Placement.Base = App.Vector({float(x)!r}, {float(y)!r}, {float(z)!r})
        doc.recompute()
        print(obj.Name)
        """)
        return self.execute_code(code)

    def create_cone(self, doc_name: str, obj_name: str, radius1: float, radius2: float, height: float, x: float = 0, y: float = 0, z: float = 0) -> dict[str, Any]:
        code = textwrap.dedent(f"""
        import FreeCAD as App
        doc = App.getDocument({doc_name!r})
        if doc is None:
            raise ValueError(f'Document not found: {doc_name}')
        obj = doc.getObject({obj_name!r})
        if obj is None:
            obj = doc.addObject('Part::Cone', {obj_name!r})
        obj.Radius1 = {float(radius1)!r}
        obj.Radius2 = {float(radius2)!r}
        obj.Height = {float(height)!r}
        obj.Placement.Base = App.Vector({float(x)!r}, {float(y)!r}, {float(z)!r})
        doc.recompute()
        print(obj.Name)
        """)
        return self.execute_code(code)

    def create_torus(self, doc_name: str, obj_name: str, radius1: float, radius2: float, x: float = 0, y: float = 0, z: float = 0) -> dict[str, Any]:
        code = textwrap.dedent(f"""
        import FreeCAD as App
        doc = App.getDocument({doc_name!r})
        if doc is None:
            raise ValueError(f'Document not found: {doc_name}')
        obj = doc.getObject({obj_name!r})
        if obj is None:
            obj = doc.addObject('Part::Torus', {obj_name!r})
        obj.Radius1 = {float(radius1)!r}
        obj.Radius2 = {float(radius2)!r}
        obj.Placement.Base = App.Vector({float(x)!r}, {float(y)!r}, {float(z)!r})
        doc.recompute()
        print(obj.Name)
        """)
        return self.execute_code(code)

    def create_prism(self, doc_name: str, obj_name: str, polygon: int, circumradius: float, height: float, x: float = 0, y: float = 0, z: float = 0) -> dict[str, Any]:
        code = textwrap.dedent(f"""
        import FreeCAD as App
        doc = App.getDocument({doc_name!r})
        if doc is None:
            raise ValueError(f'Document not found: {doc_name}')
        obj = doc.getObject({obj_name!r})
        if obj is None:
            obj = doc.addObject('Part::Prism', {obj_name!r})
        obj.Polygon = {int(polygon)!r}
        obj.Circumradius = {float(circumradius)!r}
        obj.Height = {float(height)!r}
        obj.Placement.Base = App.Vector({float(x)!r}, {float(y)!r}, {float(z)!r})
        doc.recompute()
        print(obj.Name)
        """)
        return self.execute_code(code)

    def create_drone(self, doc_name: str, variant: str = "quadcopter") -> dict[str, Any]:
        if variant != "quadcopter":
            raise ValueError("Only quadcopter variant is supported for now")
        code = textwrap.dedent(f"""
        import FreeCAD as App
        if {doc_name!r} in App.listDocuments():
            doc = App.getDocument({doc_name!r})
        else:
            doc = App.newDocument({doc_name!r})
        App.setActiveDocument(doc.Name)
        names = ['Body','ArmX','ArmY','Motor1','Motor2','Motor3','Motor4','Prop1','Prop2','Prop3','Prop4']
        for name in names:
            obj = doc.getObject(name)
            if obj:
                doc.removeObject(obj.Name)
        body = doc.addObject('Part::Box', 'Body')
        body.Length = 40; body.Width = 25; body.Height = 8
        body.Placement.Base = App.Vector(-20, -12.5, 0)
        armx = doc.addObject('Part::Box', 'ArmX')
        armx.Length = 140; armx.Width = 8; armx.Height = 6
        armx.Placement.Base = App.Vector(-70, -4, 1)
        army = doc.addObject('Part::Box', 'ArmY')
        army.Length = 8; army.Width = 140; army.Height = 6
        army.Placement.Base = App.Vector(-4, -70, 1)
        positions = [(60,0),(-60,0),(0,60),(0,-60)]
        for i,(x,y) in enumerate(positions, start=1):
            m = doc.addObject('Part::Cylinder', f'Motor{{i}}')
            m.Radius = 8; m.Height = 10
            m.Placement.Base = App.Vector(x-8, y-8, 7)
            p = doc.addObject('Part::Cylinder', f'Prop{{i}}')
            p.Radius = 28; p.Height = 1.5
            p.Placement.Base = App.Vector(x-28, y-28, 17)
        doc.recompute()
        print('drone_created')
        """)
        return self.execute_code(code)

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
