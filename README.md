# freecad-cli

本地 FreeCAD CLI，基于 `freecad-mcp` 的 XML-RPC addon，不需要 Docker。

## 架构

```text
fc CLI -> XML-RPC (localhost:9875) -> FreeCADMCP addon -> FreeCAD
```

## 目前支持

- `fc doctor`
- `fc ping`
- `fc status`
- `fc addon install`
- `fc addon path`
- `fc addon status`
- `fc doc create NAME`
- `fc doc list`
- `fc doc objects DOC`
- `fc run script.py`
- `fc screenshot out.png`
- `fc export step DOC out.step`
- `fc export stl DOC out.stl`

## 安装

```bash
cd freecad-cli
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Quickstart

### 1. 安装 addon

```bash
fc addon install
```

### 2. 重启 FreeCAD
切到 **MCP Addon** workbench，然后点击 **Start RPC Server**。

### 3. 检查

```bash
fc doctor
fc ping
fc status
```

## 常用命令

```bash
fc addon path
fc addon status
fc doc create demo
fc doc list
fc doc objects demo
fc run ./script.py
fc screenshot ./demo.png
fc export step demo ./demo.step
fc export stl demo ./demo.stl
```

## 说明

- 默认 RPC 地址：`localhost:9875`
- 可用 `--host` 和 `--port` 覆盖
- `export` 当前是通过 `execute_code` 在 FreeCAD 里执行导出脚本完成的
- `screenshot` 依赖当前 FreeCAD 视图支持截图

## CLI-Anything 集成

我已经把 CLI-Anything 插件安装到 Claude Code：
- `~/.claude/plugins/cli-anything`

在这个项目里，推荐把 CLI-Anything 当成**方法论/包装层**，把 `freecad-cli` 当成**实际控制层**。

更多说明见：
- `CLI_ANYTHING.md`

## 常见问题

### `Connection refused`
说明 FreeCAD 的 RPC server 还没启动。

### `fc ping` 失败
通常是：
- addon 没装好
- FreeCAD 没启动 RPC
- host/port 不对

### `screenshot` 失败
当前活动视图不支持截图。
