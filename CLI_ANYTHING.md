# CLI-Anything × freecad-cli

## 当前状态

- `freecad-cli` 已经是一个可用的本地 CLI：`fc`
- 它通过 `freecad-mcp` 的 XML-RPC addon 控制本机 FreeCAD
- CLI-Anything 更适合做“完整 agent-harness 方法论”和 CLI 包装规范

## 结合思路

最实用的做法不是推翻 `freecad-cli`，而是：

1. **保留 `fc` 作为轻量、本机优先控制层**
2. **把 CLI-Anything 当成方法论和后续包装层**
3. 后续需要时，再把 FreeCAD 做成更完整的 `cli_anything.freecad` 命名空间包

也就是：

```text
CLI-Anything methodology
        ↓
   freecad-cli (fc)
        ↓
freecad-mcp addon RPC
        ↓
      FreeCAD
```

## 为什么这样结合

- `fc` 已经跑通，不该重做一遍
- CLI-Anything 的优势在于：
  - 目录规范
  - 测试规范
  - REPL / JSON / 发布流程
  - agent-harness 文档化
- FreeCAD 的真实控制能力目前还是来自 `freecad-mcp + FreeCAD Python`

## 对 FreeCAD 仓库的建议

你给的 `FreeCAD-Homepage` 仓库更像官网/站点内容仓库，**适合做分析参考，不适合作为 FreeCAD 核心建模能力的真实源码输入**。

如果后面要做真正的 CLI-Anything 化，建议优先分析：
- FreeCAD 主仓库
- freecad-mcp addon
- 当前 `freecad-cli`

## 下一步建议

### 方案 A：保持现在的 `fc`
继续增强：
- `fc start-rpc`
- `fc doctor --json`
- `fc create box/cylinder`
- `fc export` 子命令化
- 更强的对象编辑能力

### 方案 B：做 CLI-Anything 包装层
新建：
- `agent-harness/`
- `TEST.md`
- CLI-Anything 风格文档
- 更正式的 package/repl/json 规范

## 当前结论

**最合理的结合方式：把 CLI-Anything 当“方法论和规范层”，把 `freecad-cli` 当“实际控制层”。**
