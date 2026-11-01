# 从问题到图：最小可编辑规范

这个工具不是自动理解论文的 AI，也不会证明图表达的机制是真的。它把你已经想清楚的模块、关系和位置，稳定地画成可编辑 SVG。所有示例都是原创、虚构教学例子，不是论文结果，也没有性能数据。

运行环境：Python **3.9+**（本次实际测试为 Python 3.12）。核心仅用标准库；`--preview` 需另有 Inkscape。测试只读取仓库输入并向临时目录写入，不会重建或改写 `generated/`。

## 先手画，再填字段

1. 用一句话写 `question`：读者看完要回答什么？
2. 用一句话写 `takeaway`：图能支撑的结论是什么？不要填未测量的“更快”。
3. 列出 `nodes`，每个框只承担一个清楚的职责。
4. 列出 `edges`，每根箭头都说得出“什么，从谁，到谁”。
5. 最后调整 `x/y/w/h` 与 `via`。坐标原点在左上，x 向右，y 向下。

入门直接复制 `starter.json`。标题与节点默认英文是为了便于导出和字体兼容；可以写中文，但你的 SVG 编辑器/预览环境必须有合适的中文字库。文本宽度检查只是启发式，中文和其他字体仍需人工预览。

## 顶层字段

- `version`: 当前固定 `1`。
- `title`, `question`, `takeaway`, `provenance`: 必填字符串。`provenance` 写真实来源或明确的虚构声明。
- `canvas`: `width`, `height`；默认 1200 × 680。
- `nodes`: 至少一个节点。
- `edges`: 有方向的关系，可以为空。
- `panels`: 可选背景分区；每项 `x,y,w,h,label`，不代表节点或数据通道。

## 一个节点

```json
{"id":"scheduler", "label":"Scheduler", "kind":"module", "x":490, "y":410, "w":170, "h":82}
```

`id` 是稳定标识，不随名字改变；允许英文字母开头，之后字母、数字、下划线和连字符。`label` 是显示名称，可用 `\n` 换行。`kind` 可为 `module`（普通模块）、`storage`（状态/存储）、`external`（外部输入输出）、`new`（当前图强调的新模块）。这些只是本项目的视觉约定，不是所有体系结构论文的统一标准。

## 一根箭头

```json
{"id":"select", "from":"scheduler", "to":"engine", "role":"control", "direction":"forward", "from_side":"top", "to_side":"bottom", "via":[[575,378],[675,378]], "label":"select", "label_at":[625,382]}
```

- `from` 和 `to` 必须指向存在的节点。箭头固定指向 `to`；反向时交换端点与端口。
- `role`: `data` 实线，`control` 虚线，`feedback` 点线。图例同时解释线型与颜色，不靠颜色单独传意。
- 两个 `*_side`: `left/right/top/bottom`，锚定在节点边的中点。
- `via`: 按顺序走过的折点；空列表就是直线。不提供自动布局或自动避障。
- `label_at`: 标签中心 x 与文本基线 y，和路由独立。修改路由后也要检查标签位置。

## 三张图怎么读

- `01-overview.json`: 总体结构——事件的数据路径与调度控制分离；完成反馈返回调度器。
- `02-mechanism.json`: 一轮调度的局部机制——入队、选择、预留、执行、释放；容量状态参与预留并接收释放反馈。不是周期精确的时序图，也不包含所有失败路径。
- `03-before-after.json`: 职责拆分对比——保持输入相同，单独展示调度策略。不表示已经测得加速。

这三张图是不同抽象视角：总体图省略了局部的容量更新细节，机制图省略了完整策略状态。不要把“省略”解读为“系统不存在”。

## 修改练习

```bash
PYTHONPATH=src python -m arch_diagram_lab edit examples/01-overview.json \
  --node scheduler --label 'Epoch arbiter' -o generated/renamed.json
PYTHONPATH=src python -m arch_diagram_lab render generated/renamed.json \
  -o generated/renamed.svg
python scripts/mutation_demo.py --preview
```

最后一个命令还将反馈连接改为从模块右侧进入，生成 `04-edited-overview.*`。这展示的是“修改名字不破坏连接，修改连接要重新检查”，不是一个新的科研主张。

## 检查边界

自动验证：必填文字、唯一节点/边 ID、端点存在、语义角色、明确方向、端口、有限数字、基本画布边界、节点重叠、标签粗略尺寸、首尾路径从端口外侧进入/离开。错误以非零退出码 2 返回。

**仍需人检查**：科学正确性、是否选对抽象层、所有线段是否穿过其他模块、边和标签碰撞、交叉歧义、标题/脚注溢出、字体实际字宽、缩放到论文栏宽后的可读性。通过验证 ≠ 通过论文审稿。

SVG 保留文字、节点与边的 ID，可用 Inkscape 等工具继续编辑。手改 SVG 不会自动回写 JSON；要保持可重建，请优先修改 JSON 后重新导出。

## 黑白自检与语料检查

```bash
PYTHONPATH=src python -m arch_diagram_lab render examples/03-before-after.json \
  -o generated/05-before-after-monochrome.svg --monochrome --preview both
python scripts/validate_corpus.py
```

`--monochrome` 将颜色变成灰度，同时保留文字、线型与 `[NEW]` 标签。这只是黑白检查，不等于色觉差异模拟或最终栏宽验收。语料检查只验证本地记录结构与交叉引用，不会自动证明原图解读正确。

机制示例中的步骤是动作，不是五个物理模块；编号表达单个成功事件的逻辑顺序，箭头标签表达传递的数据、选择/授予控制或释放反馈。容量状态是资源模型的一个局部抽象；未画预约写入、失败重试、并发或精确周期。总览中的 Scheduler 对应选择动作，Execution engine/Resource model 覆盖执行和资源管理；不能把这幅教学流程当成完整实现规范。
