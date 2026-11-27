# 怎样判断模拟器的抽象经得住检验？

[返回问题导航](../README.md#从一个问题开始)

先给证据链中的每幅图分配职责：它是在说明为什么需要某种抽象、检查一个部件，还是把最终输出与参考对照？一处接近不能替整条链作证。本练习只讨论这些验证环节；单位、分母和测量阶段的逐项检查见[跨图前先核对基线](check-baselines-across-figures.md)，不在这里重复。

<a id="workload-control-topology"></a>

## 可选预读：先分清工作图、运行控制与硬件拓扑

样本外链接式案例 GPU-Tile-Sim 的会议归属见 [MICRO 2026 官方程序](https://microarch.org/micro59/program/)。这里仅用 **arXiv:2607.11262v1** 的图号和物理 PDF 页；ArchSim 对照固定为 **arXiv:2607.12359v1**。只核对原文、图注和文本页定位，不据此声称重新完成视觉审核；二者不新增为固定100篇或原图库收录。

**问题：三图中的框和箭头分别装着什么含义？**

- [GPU-Tile-Sim F4（v1，p6）](https://arxiv.org/pdf/2607.11262v1#page=6)：节点表示分配给 warp 或协作 warp group 的 tile 操作，边规定数据依赖或发射顺序约束。读的是工作负载及其执行约束，不能把每个操作框当作一个硬件部件。
- [GPU-Tile-Sim F7（v1，p8）](https://arxiv.org/pdf/2607.11262v1#page=8)：把工作图交给模拟器的就绪跟踪、调度与状态更新，并分派至被建模的计算、访存和片上互联资源。结合 §5，issue 释放该节点的出向顺序边，completion 才释放出向数据边；后继须满足全部入边约束才就绪。图中连接要按调度、分派和完成反馈来读，不能全部当成物理导线。
- [ArchSim F3（v1，p6）](https://arxiv.org/pdf/2607.12359v1#page=6)：节点是目标硬件模型的组件实例，边是组件间类型化端口连接。它描述硬件拓扑配置，既不是 tile 工作负载，也不是模拟器运行控制流。

**自检：** 找一条需要数据完成的依赖，说明为什么“已发射”还不够；再找一条组件端口连接，说明它为何不随某个 tile 完成而被“释放”。先确定抽象对象，再进入下面的验证证据链；这些角色区分本身不是精度或性能验证。

下列页码分别针对 TraceRTL 的15页 HPCA 2026版、SimPhony 实验室8页 arXiv:2411.13715v1版、RHONE 的18页 USENIX ATC 2025正式版。沿用已有正文、图注和初读核对记录；本轮未重新下载文件，也未完成新视觉复核。不据文本推断配色或箭头位置，三例也不代表所有模拟器论文的验证规范。

| 证据链与改了什么 | 跟谁比 | 最多能支持什么 |
|---|---|---|
| **TraceRTL**：[F4 p5](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=5)用错路访存统计说明建模动机；[F8 p9](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=9)再对比有／无错路模拟。 | 时延／性能误差的参考是原执行驱动 XiangShan RTL。§VI-B 对 F8 单项子基准设有“w/o WPS 误差超过1%”的展示门槛，同时另列套件整体性能误差和 RMSE。 | 检查错路处理这一选择是否改善所测场景的误差；不能将经过筛选的单项子基准当作全部负载，也不能由动机统计直接推出模拟器整体可靠。 |
| **SimPhony v1**：[F6 p5](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=5)给出布局感知面积估计；[F10(a) p6](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=6)将它与仅求和器件面积的方式对照。 | 参照是该 TeMPO 设计的实际布局面积。F10(b) 换成 SCATTER 的数据相关能耗，不能接成同一面积验证。 | 支持在这一布局案例中检查面积估计方法；不是芯片性能实测，也不替周期、功率或能量模型完成验证。 |
| **RHONE**：[F8 p9](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=9)检查地面物理芯片表征与在轨物理芯片的关系；[F12／F13 p12](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=12)分别检查温度模型与模拟任务时延。 | F8 两端是物理芯片；F13 是 RHONE 输出对 BUPT-1 在轨参考，解释见 [§7.2.4 p13](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=13)。 | 分开检验输入表征的适用性、温度部件和最终时延；任一层接近均不能替代另外两层，也不能抹去任务长度与误差分母的差异。 |

## 练习：给一句结论找缺少的证据

打开三例的原页，分别挑一句过强结论，圈出它跳过的验证环节，再改成有边界的表述：

1. “F8 展示的子基准改善了，所以所有 TraceRTL 负载都改善了。”
2. “SimPhony 面积接近实际布局，所以芯片性能模型也得到实测验证。”
3. “RHONE 地面芯片表征接近在轨芯片，所以模拟任务时延已经准确。”

**参考答案：** 第一条跳过了样本选择与汇总口径；先区分门槛筛出的单项和套件汇总，再只谈所测设置中的证据。第二条把面积验证扩成性能验证；将结论收回到 F10(a) 的 TeMPO 布局案例，并另找周期或能量的独立验证。第三条跳过了模型部件和输出检查；F8 不能替代 F12 的温度验证或 F13 的任务时延对照。修正措辞后，还应问原图是否足以排除其他解释，而非把这三条答案当作正确性证明。

进一步阅读：[TraceRTL 整篇导读](reading-tracertl-figures.md) · [SimPhony 导读](reading-simphony-figures.md) · [RHONE 导读](reading-rhone-figures.md)。这些页面保留各自版本与核验限制；实验图仅作原文证据链接，不进入非实验原图库。本次不新增图片、数据表或 PDF，计数与许可不变。
