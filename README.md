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
- `fc rpc start`
- `fc doc create NAME`
- `fc doc list`
- `fc doc objects DOC`
- `fc run script.py`
- `fc create box DOC NAME --length 10 --width 20 --height 5`
- `fc create cylinder DOC NAME --radius 5 --height 20`
- `fc create sphere DOC NAME --radius 10`
- `fc create cone DOC NAME --radius1 8 --radius2 2 --height 20`
- `fc create torus DOC NAME --radius1 20 --radius2 5`
- `fc create prism DOC NAME --polygon 6 --circumradius 10 --height 20`
- `fc create drone DOC --variant quadcopter`
- `fc screenshot out.png`
- `fc preview DOC out.png`
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
fc rpc start --seconds 60
fc doc create demo
fc doc list
fc doc objects demo
fc create box demo box1 --length 20 --width 10 --height 5
fc create cylinder demo cyl1 --radius 5 --height 20
fc create sphere demo s1 --radius 8 --x 40
fc create cone demo cone1 --radius1 8 --radius2 2 --height 20 --x 60
fc create torus demo t1 --radius1 20 --radius2 5 --x 90
fc create prism demo p1 --polygon 6 --circumradius 10 --height 20 --x 120
fc create drone demo-drone --variant quadcopter
fc run ./script.py
fc screenshot ./demo.png
fc preview demo ./demo-preview.png
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
