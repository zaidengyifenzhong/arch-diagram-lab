# RHONE：从温度映射到地面份额，先问每个数属于谁

[返回固定样本目录](../catalog/README.md#reading-guide-atc2025-rhone)

本导读只采用 [USENIX ATC 2025 正式 PDF《Emulating Space Computing Networks with RHONE》](https://www.usenix.org/system/files/atc25-wang-liying.pdf)，共18个物理页（含封面），论文集第815–831页。下列页码均为 PDF 物理页。

核验范围：沿用已有15幅编号图的初步研究记录及本轮提供的原文核对信息。本轮官方 PDF 读取超时，没有新增逐图视觉复核，也没有重查 F9 的每条箭头；因此不描述未经重新查看的配色或箭头位置。既有初读不等于独立逐图审核或实验复现。本页只写原创练习与原文深链，不复制图、表或 PDF，不新增原图收录。

## F2 → F9：先把温度、目标耗时与容器份额分开

读 [F2（p6）](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=6)，并对照 [§5.2／F9（p10）](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=10)：例子中的 **15 °C 是建模的目标芯片温度**。satPerfTable 给出该温度下目标应用预期的 **3.0 s**，emuPerfTable 再用这一耗时选择地面容器的份额。§5.2 例子的最终 **90%** 应放在地面容器分配这一栏，不应改写为卫星 CPU 使用率。

**练习：给三个数各加一个名词。** 写成“目标芯片温度15 °C”“目标应用预期耗时3.0 s”“地面容器份额90%”，然后追两张表之间传递的是什么。3.0 s 在这条映射中是要匹配的应用执行时间，不是运行整个仿真器的宿主耗时；90% 也不意味着目标芯片恰有90%的忙碌周期。

F9 要按时间步读反馈：当前步的温度影响功率，功率再进入后续温度更新。练习时打开原图，沿温度→功率→后续温度核对箭头端点，并标出“当前”和“后续”；不要把它压成同一步内没有先后关系的循环，也不要将这一反馈图当成温度验证结果。

## F8 → F13：相同单位不等于相同参照

| 原文位置 | 对照的对象 | 读图问题 |
|---|---|---|
| [F8，p9](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=9) | 地面物理芯片表征与在轨芯片 | 这里比较的是物理芯片表现，还是 RHONE 输出？先写清两端对象。 |
| [F12，p12](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=12) | 温度验证 | 这是对模型温度结果的检查，不能由温度接近直接推出所有应用时延也准确。 |
| [F13，p12](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=12)，解释见 [§7.2.4，p13](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=13) | RHONE 模拟出的时延与 BUPT-1 在轨数据 | 这里才是在检验模拟输出。把绝对误差与百分比误差分别记录，检查分母。 |
| [Table 2，p11](https://www.usenix.org/system/files/atc25-wang-liying.pdf#page=11) | 宿主 CPU／内存开销及设置时间 | 这是运行工具的成本，不能拿来替代目标应用执行时间；表独立编号，不算一幅图。 |

Pi 上 YOLOfastest 的约40 ms短任务尤其适合练习误差分母：当参考时延很短，小的绝对偏差也可能呈现为较大的百分比。阅读 F13 时，先问任务与参考值，再看比例；不能只按百分比给不同长度任务排可靠性名次，也不能据一个短任务推广所有应用。

**练习：若 F8 的地面表征接近在轨表现，为什么还需要 F13？** 因为表征数据是否可用于目标芯片，与完整 RHONE 映射和执行流程是否产生接近在轨的时延，是两个问题。F12 又检验温度这一变量；三者不能互相代替。

## 与已有模拟器案例对照

在 [TraceRTL 导读](reading-tracertl-figures.md)中，固定配置误差与设计改动后的趋势分开讨论，参考还要明确为原 RTL 模型。在 [SimPhony 导读](reading-simphony-figures.md)中，先前架构模型与实际布局面积是不同参照。RHONE 则需要再拆开地面物理表征、BUPT-1 在轨数据和宿主工具开销。可重复使用同一张笔记卡：**目标对象／参照对象／单位／测量或模拟阶段**；卡片相同不表示三篇系统、模型或验证强度相同。

权限边界也要按对象区分：Baoyun 功率数据的 CC BY 授权不能延伸为 BUPT-1 数据或论文图片的再分发许可。本导读不改变目录原有许可判断，原图库与固定样本原图计数保持不变。
