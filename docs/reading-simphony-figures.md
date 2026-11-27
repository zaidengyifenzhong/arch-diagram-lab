# SimPhony：先认损耗、周期与能耗，再核对验证参照

[返回固定样本目录](../catalog/README.md#reading-guide-dac-2025-simphony)

本导读采用[实验室8页 PDF](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf)，首页标记 **arXiv:2411.13715v1**，并参照[该版官方 HTML](https://arxiv.org/html/2411.13715v1)。下列物理页只定位这份实验室文件。其署名包含 Amir Begovic；DAC 正式记录列 Nicholas Gangi，目录仍保留 DAC 2025 论文身份，不将两份作者列表、版本或排版视为相同。

核验范围：本次核对了可读正文、图注与 PDF 文本页定位。截图工具未返回可查看图像，云端直接下载又被代理以 `403 Forbidden` 拒绝；未改换路线获取文件，因此没有完成逐图视觉复核。下文不描述未经核验的配色、箭头位置或几何细节。仅提供原创阅读练习与原文链接，不上传图片、实验图、数据表或 PDF，也不以代码许可推断图片许可。

## 第一条路径：F2／F3 → F4 → F9

打开 [F2／F3（p3）](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=3)，先把光学连接和模型权重分开：有向边描述连接及信号方向，损耗权重用于累计插入损耗。从激光源到光探测器找“关键路径”时，优化量是**累计插入损耗最大**，不是延迟最长；它服务于链路预算和激光功率需求。不要看到 DAG 就套用软件任务的最长执行时间解释。

再读 [F4（p4）](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=4)：沿一个分块 GEMM 的部分和，依次辨认波长并行求和、核间光电流聚合、模拟时间积分和数字累加。问每一层“结果在哪个域累积、哪些工作并行、哪些要等后续周期”。这里建模的是目标系统的执行周期，不是运行 SimPhony 的宿主耗时。

<a id="loss-power-cycles-exercise"></a>

**短题：其他入参不变，核心插入损耗增加 3 dB，为何估算激光功率约乘二？F4 的周期又从哪里来？** 对照作者代码固定提交 `0bdc10df6fe50051769016614b04400d0a92d631` 的 [`cal_laser_power`（energy.py L102–119）](https://github.com/ScopeX-ASU/SimPhony/blob/0bdc10df6fe50051769016614b04400d0a92d631/onnarchsim/workflow/energy.py#L102-L119)：损耗加进 dBm 链路预算，再经指数换成线性功率。保持探测灵敏度、分配因子、位宽、墙插效率和消光比等其余输入不变，前后比值为 `10^(3/10) ≈ 1.995`，约为二倍。这是假设计算，不是实测功率。

周期走另一条链：分层工作负载、分块和架构映射等输入经 [`simu_partition_cycles`（simulator.py L179–249）](https://github.com/ScopeX-ASU/SimPhony/blob/0bdc10df6fe50051769016614b04400d0a92d631/onnarchsim/simulator.py#L179-L249)得到 partition cycles；[`simu_energy` 调用（L313–331）](https://github.com/ScopeX-ASU/SimPhony/blob/0bdc10df6fe50051769016614b04400d0a92d631/onnarchsim/simulator.py#L313-L331)将它作为 `cycles`，另将核心损耗作为 `insertion_loss` 传给 `energy_calculator`。回 F4 核对 GEMM 的分块、并行与累加安排：损耗路径不替代这条周期建模链。上述假设不支持整体能耗翻倍，也不意味着周期改变。代码仅作固定版本的实现对照，不声称该提交与论文版本完全一致；未执行代码。

最后读 [F9（p6）](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=6)。F9(a) 增加波长时也按波长数扩展调制器和激光源数量，不能解释为固定器件数量下只改变光的参数；这是模型设计探索，不是原 TeMPO 芯片的实测。F9(b) 另扫位宽，不与 (a) 合成“所有参数同时改变”的实验。

**练习：增加波长后，能否只凭更高并行度断言所有部件能耗都会下降？** 不能。先列出同时增多的器件和保持不变的器件，再分开看功率需求、执行周期与累计能量。也不能用 F2 的损耗路径直接代替 F4 的周期模型。

## 第二条路径：F6 → F10(a)，另读 F7／F8 与 F10(b)

[F6（p5）](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=5)给出考虑信号流的面积估算方法；接到 [F10(a)（p6）](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=6)，问拓扑和间距进入估算后，与实际布局面积如何对照。器件面积相加与布局占地是不同口径，不能把连线拓扑本身当作已完成物理布局。

同页 F7／F8 与先前架构论文的模拟结果对照，不是完整多核光子系统的实测验证：F7 分面积与能量，F8 分面积与功率。F10(b) 又换成 SCATTER 的数据相关相移器能耗，不能把它当作 F10(a) 的 TeMPO 面积结果，或把器件功率模型直接当成整段运行能量。

**练习：给 F7、F8、F10 的每个面板写下“设计／指标／参照”三栏。** 只有这三栏一致时才考虑比较数值；先前架构模型、实际布局与不同器件功率模型承担不同证据角色。

## F1–F11 角色索引

这是正文与图注层面的角色索引，不是完整视觉审核记录。Table I 等独立编号的表不计入11幅 Figure；混合图和实验图仅链接，不收入原图库。

| 图号 | 读图任务与证据边界 | 实验室 PDF 物理页 |
|---|---|---|
| F1 | 定位器件库、架构构建与仿真分析之间的职责；工具框架不等于被建模芯片拓扑。 | [p2](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=2) |
| F2 | 对照节点电路与加权有向无环图，辨认连接和损耗的表示。 | [p3](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=3) |
| F3 | 在参数化架构中追最大插入损耗路径；不是最长时延路径。 | [p3](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=3) |
| F4 | 跟随 GEMM 的分层累加，分开光学并行、模拟积分和数字累加。 | [p4](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=4) |
| F5 | 连接数据相关能量估算与器件功率模型；混有模拟／测量的器件模型数据，不当作纯机制整图。 | [p5](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=5) |
| F6 | 看拓扑与信号流如何进入布局感知的面积估算，再转 F10(a)。 | [p5](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=5) |
| F7 | 对照先前 TeMPO 架构模型的面积和能量；不是系统实测。 | [p6](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=6) |
| F8 | 对照先前 Lightening-Transformer 模型的面积和功率；不要把功率写成能量。 | [p6](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=6) |
| F9 | (a) 波长与配套器件扩展；(b) 位宽扫描。都是设计探索，不能拼成同一改动。 | [p6](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=6) |
| F10 | (a) TeMPO 布局面积对照；(b) SCATTER 数据相关能耗。先区分设计再读指标。 | [p6](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=6) |
| F11 | 异构层映射后的分层能量分析；是建模用例，不是宿主执行时间或普遍最优映射证明。 | [p7](https://scopex-asu.github.io/files/publications/ONN_DAC2025_Gu_SimPhony.pdf#page=7) |

可对照 [TraceRTL 整篇导读](reading-tracertl-figures.md)：它将固定配置误差与改动后的性能趋势分开。这里也应将 F7／F8 的参照验证与 F9 的参数探索分开，但两篇参照类型和系统对象不同；不能据此称 SimPhony 已完成 TraceRTL 那样的 RTL 参考验证。
