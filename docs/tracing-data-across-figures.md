# 跨图追踪同一数据

[返回两张机制图怎么对照读](reading-mechanism-pairs.md) · [读图指南索引](../catalog/README.md#source-linked-reading-guides)

先选一个有名字的数据项，再核对它的值、坐标与表示是否保留。跨图可以追踪同一数据，但相邻图号不意味着同一次执行，也不保证整组输入完全相同。以下只链接已公开原图，不新增或修改图片。

## VLA Quantum：从 ld2 到实虚部分离，再比较新布局

固定 arXiv:2602.09604v3，F3、F4、F5 均在 [PDF 物理第 4 页](https://arxiv.org/pdf/2602.09604v3#page=4)。

先看 [F3 原图](../gallery/assets/ipdps2026-vla-quantum-F3-12f73a404ccfb17e.png)的 `ld2 {v0.4s,v1.4s},[x2]`，再到 [F4 原图](../gallery/assets/ipdps2026-vla-quantum-F4-43f0b9e0fd3d6e69.png)追 `s[i].re` 与 `s[i].im`：基线内存将实部、虚部交错排列，加载时拆到 v0 的实部序列和 v1 的虚部序列。这两图分别给出代码和访问模式。

[F5 原图](../gallery/assets/ipdps2026-vla-quantum-F5-5f640e488c7322ee.png)展示新方案：Step 1 比较布局调整前后，示例按四个实部、四个虚部分组，后续另有临时缓冲与计算。它不是 F4 同一次 load 的下一步。图中的量子电路是被模拟的对象，线程、内存和向量寄存器属于运行模拟器的 ARM 平台；图内三角标出施加门的量子位，图注将此例指定为 q3 上的 Hadamard 门，不能当作 ARM 寄存器编号。参见[原文图注及 §III–IV](https://arxiv.org/html/2602.09604v3)。

**看图回答：** F4 的 `s[i+2].im` 最终进入 v0 还是 v1？用它的下标和 `.im` 标记沿箭头核对，不仅凭颜色猜测。

## RTeAAL Sim：从矩阵坐标到 fibertree，再到格式描述

固定扩展版 arXiv:2601.18140v1。[F2 原图](../gallery/assets/asplos-2026-rteaal-F2-db323cecbaebcefa.png)位于 [PDF 物理第 2 页](https://arxiv.org/pdf/2601.18140v1#page=2)，[F6 原图](../gallery/assets/asplos-2026-rteaal-F6-4c75b7a7781f85f6.png)位于 [物理第 4 页](https://arxiv.org/pdf/2601.18140v1#page=4)。

在 F2 选 `A[0,2]=1`，沿 fibertree 的 M=0、K=2 到叶值 1，再在 F6 找同一坐标与叶值。F6 还增加了 `A[1,1]=5`，所以可以对照这个保留的数据项，却不能称两图是完全同一矩阵。

最后读 F6 右侧格式描述：rank-order 为 `[M, K]`；M 用非压缩 U 格式、`cbits: 0`，坐标由数组位置隐式编码，并非没有 M 层；K 用压缩 C 格式，`cbits` 非零。矩阵、树和格式描述分别说明数据、层次与存储表示，不能把表示变化误读成又执行了一次计算。参见[原文 §2.5.2 与 F6 图注](https://arxiv.org/html/2601.18140v1)。

**看图回答：** F6 相比 F2 新增的叶值 5，沿哪一对 M、K 坐标到达？再检查原来的 `A[0,2]=1` 是否仍能找到。

这些是非实验读图练习，不比较两篇性能，不宣称量子电路与 RTL 示例是同一被模拟设计，也不改变原图库论文数或图片数。
