# FREECAD.md

## Scope
- document management
- primitive creation
- object inspection
- export
- script execution

## Backend reality
Current control path:
`fc -> freecad-mcp XML-RPC addon -> FreeCAD`

## Short-term strategy
Keep `fc` as the real execution path and grow command coverage incrementally.
