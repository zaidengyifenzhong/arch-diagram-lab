# 跨图前先核对基线

[返回跨图阅读方法](reading-mechanism-pairs.md)

两图都写“性能”或都改变同一个参数，不代表它们能拼成同一条结论。先为每幅图单独填写下面四栏，再决定哪些结果可以对照。以下是评审规则的练习选例，不代表这些现象在文献中的普遍性。

## 可复制的四栏检查

| 相同对象或自变量 | 参照／分母 | 单位 | 测量阶段 |
|---|---|---|---|
| 论文版本、图号；工作负载／配置；改变什么、固定什么？ | 与谁比较？若归一化，分母是谁？增幅和比值的定义是什么？ | 次数、周期、百分比、倍数、MHz，还是资源数量？ | 目标程序、宿主仿真、预热、抽样，还是综合后的实现？ |
| 待填 | 待填 | 待填 | 待填 |

换图时重新填一行；任一栏变化，都先解释变化，再谈改善或退化。

## Virtuoso：同讲 RestSeg，横轴与分母却变了

使用22页 arXiv v2 的 [F19／F20（物理 p14）](https://arxiv.org/pdf/2403.04635v2#page=14)。F19 按 GB 区分 RestSeg 大小配置，报告翻译延迟相对 Utopia **8 GB RestSeg** 的增幅；F20 用主内存被 restrictive segment 覆盖的比例作横轴，报告相对 **Radix** 的模拟交换周期。前者是翻译，后者是 swapping，分母和自变量的表达都变了。

**练习：能把 F19 的百分比接到 F20 上，算出“总开销”吗？** 不能。先把两图的参照分别写出来；即使都涉及时间，也缺少共同基线和可相加的绝对量。F20 不是运行模拟器的宿主时间。继续读[整篇 Virtuoso 案例](reading-virtuoso-figures.md)。

## TraceRTL：模型准确性与预热收益不是同一个比较

使用15页 HPCA 版的 [F9／F10（物理 p10）](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=10)。F9 以 XiangShan 原 RTL 为参照，比较 TraceRTL 与已校准的 XS-gem5 的性能误差；XS-gem5 是对照模型，不能替换原 RTL 的参照地位。F10 则以**采用常规详细预热的 TraceRTL** 为基线。

正文 [§VI-C「Overall Performance Accuracy」与 §VI-D「Fast Warm-up Strategy TraceDedup」（物理 p9）](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=9)在图的前一页：后者分别定义预热阶段的加速比（快速预热前后时钟周期之比）和抽样阶段的性能准确性。读图时给这两种量各填一行，不把它们合称“性能提升”。

**练习：F10 的预热加速能否直接宣称整个仿真或目标 CPU 同比例加速？** 不能；收益的测量阶段有限，抽样误差也不是加速比。完整端到端结论还需要其余阶段的成本。机制背景见[TraceRTL 短指南](../catalog/README.md#reading-guide-hpca-2026-tracertl)。

## Lilac：同一 N 配对，资源与最高频率分别判断

使用14页 ASPLOS 作者版的 [F13（物理 p11）](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=11)。比较对象是同一输入并行度 N 下，Lilac 与 ready/valid 实现的 GBP；应在同一 N 行内配对，再分别看 LUT 数、寄存器数和最高频率。它们是不同量纲，不能合成一个没有定义的“更快”。

**练习：N=4 或 N=8 时，能否说 Lilac 每项都更优？** 不能：这两种配置下 ready/valid 的最高频率更高，Lilac 的资源仍更少。最高频率也不单独决定实际端到端吞吐，还要知道每项工作的周期数与供数等条件。继续读[Lilac 整篇案例](reading-lilac-figures.md)，把接口与实现证据接回评估条件。

本文只提供原创文字和精确版本的原页链接，不嵌图、不复刻结果表。上述实验图不进入非实验原图库，不改变图片或论文覆盖计数。
