# TraceRTL：从接口替换读到模型验证与设计趋势

[返回目录中的 F2／F7 短指南](../catalog/README.md#reading-guide-hpca-2026-tracertl)

本案例仅使用 XiangShan 站的 **15页 HPCA 2026会议版**《TraceRTL: Agile Performance Evaluation for Microarchitecture Exploration》，[DOI 10.1109/HPCA68181.2026.11408626](https://doi.org/10.1109/HPCA68181.2026.11408626)。所有图号和物理页都对应[这份 PDF](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf)，不混用 TBench 期刊版。这里只提供原创练习与原文链接；实验图用于理解论文论证，不收入原图库，也不复刻结果表。

核验范围：已核对该会议版的公开可读文本、图注、章节及页码，并结合已有 F2／F7 读图记录。本次云端直接下载返回代理 `403 Forbidden`，未取得本地 PDF，也未重新完成16幅图的逐图渲染审核。因此下文区分机制和实验角色，但不宣称核验了全部配色、线型、图例位置或面板几何；需要辨别这些视觉编码时，请打开相应原页。没有改换下载路线或请求期刊文件。

## 先问 F9 → F16：一个配置准确，等于改设计也准确吗？

**F9 问固定配置下模型离参考有多远。** [p10 的 F9](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=10)结合 §VI-C（p9）比较 TraceRTL、XS-gem5 与原始 XiangShan RTL 参考。这里的参考是原 RTL 模型，不要把模型结果误称为真机测量。

**F16 问改变一个设计变量时，模型能否跟上参考的变化。** [p12 的 F16](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=12)结合 §VII-C（p11–12），分别改变 BTB、FMA 数量和 L2 BOP。练习：即使两个模型在旧配置给出相近结果，能否由此推出它们在新配置也同样准确？不能；需要另查变化的方向与幅度。F9 与 F16 的验证对象不同，不能把一幅的误差概括成另一幅的保证。

## F1–F16：逐图阅读清单

下表的形式与面板说明仅采用图注、正文可确立的信息，不凭文本提取结果猜颜色或空间位置。F4 和 F8–F16 是实验或统计证据；表格编号 Table I 等另计，不属于16幅 Figure。

| 图号 | 目的与可操作的阅读问题 | 形式、面板与边界 | 原文物理页 |
|---|---|---|---|
| F1 | 先找 TraceRTL 的定位，再问性能探索何时进入开发流程。 | (a) 方法定位，(b) 工作流比较；RTL 是目标设计层次，不能当作运行模拟器的宿主。 | [p1](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=1) |
| F2 | 谁提出取指范围，谁供应 trace？把两个区间取交集，检查送入 backend 的指令。 | 取指机制示例；沿用短指南中的地址例子，记录中的下一条不自动属于当前请求。基础方案不能表示任意错路。 | [p4](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=4) |
| F3 | trap 如何影响重定向，又如何由 trace 接管？ | (a) 原生异常／中断，(b) 拦截并按 trace 重注入；对比控制来源，不把它当作异常处理性能曲线。 | [p5](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=5) |
| F4 | 为什么缺少错路访存会改变缓存行为？ | 正确路径专有、错误路径专有与重叠访问的统计动机；不是流水线示意，也不能单独证明后续近似对所有负载有效。 | [p5](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=5) |
| F5 | 指令变换后，旧 PC 怎样对应新 PC，分支目标是否也要跟着更新？ | 原 trace、映射与目标 trace 的示例；不是目标处理器布局。可另查同页 Table I 的接口职责，但不把该表算作 F5 面板。 | [p6](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=6) |
| F6 | 相似输入为何能省去一部分预热，又有哪些历史不能随意删？ | TraceDedup 的 trace、signature 和指令消除示例；这是预热机制，不是任意程序的语义等价压缩规则。 | [p7](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=7) |
| F7 | 六步流程里，何时做性能反馈，何时补完整功能验证？ | trace 准备、原型、trace-driven 仿真、性能分析、功能正确性、execution-driven 仿真；前一轮探索不替代后一轮验证。 | [p8](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=8) |
| F8 | 开启／关闭错路模拟，对误差有什么影响？ | 消融结果；先辨认被改的是模拟方法，再读误差，不能当成目标硬件增加了一个优化模块。 | [p9](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=9) |
| F9 | 固定目标配置下，TraceRTL 与 XS-gem5 各自相对原 RTL 有多大误差？ | 模型准确性比较；参考是 XiangShan，不是拿 XS-gem5 当所有模型的真值。 | [p10](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=10) |
| F10 | 预热省了多少模拟周期，之后采样阶段的误差如何？ | 两种不同指标的联合评估；基线为详细预热版 TraceRTL。预热周期比不是宿主秒数，也不是端到端仿真或目标 CPU 的加速。 | [p10](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=10) |
| F11 | TraceBridge 变换前后，指令表示膨胀了多少？ | trace 变换统计；先区分指令数量与字节尺寸、静态与动态口径，再讨论输入表示成本。 | [p10](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=10) |
| F12 | 各类负载的性能瓶颈组成是否相同？ | Top-down 分解；与 F11 相邻不代表膨胀直接造成了全部瓶颈，不能只凭这两图建立因果。 | [p10](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=10) |
| F13 | 指令映射后，分支与数据缓存行为是否保留？ | (a) 分支预测 MPKI，(b) 数据缓存 MPKI，对照 TraceRTL 与 TraceBridge-RV2RV；不是完整跨 ISA 等价证明。 | [p11](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=11) |
| F14 | 在 TraceRTL 模型内，采用两级地址翻译相对普通翻译付出什么代价？ | 性能降幅实验；图注指向 SPEC CPU2006。邻近正文出现一次 SPECfp2017，套件措辞不一致，本指南不据此转录数值或混写套件。 | [p11](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=11) |
| F15 | 两级翻译原型相对功能完整的香山参考是否准确？ | KVM 虚拟化下的误差验证；参考是功能完整的 XiangShan Hypervisor，不是 F14 中普通翻译的模型配置。 | [p11](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=11) |
| F16 | 对三个独立设计改动，模型预测的性能趋势是否与 RTL 参考一致？ | (a) BTB 1024→2048；(b) FMA 2→4，仅 SPECfp2017；(c) L2 BOP 关闭→启用。分别比较，不是三项同时改变的一次实验。 | [p12](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=12) |

## 三条证据链：先写问题，再追图

**机制动机与验证：F2 → F3／F4 → F8 → F9。** 从取指接口问 trace 缺失了什么，再将控制流接管与错路访存动机分开。F8 检查错路处理这一选择；F9 扩展到固定配置的整体误差。机制示例、统计动机、消融和整体验证各承担一个环节，不能由 F2 的清楚箭头直接推出 F9 的准确性。

**表示变换与行为检查：F5 → F11 → F12／F13。** 先追 PC 和指令表示，再查变换的膨胀口径。F12 是负载瓶颈分析，F13 是映射后特定行为指标的对照；两者不是同一种验证，也不能用 MPKI 接近替代所有时序行为的检验。

**原型探索与参考验证：F7 → F14 → F15 → F16。** 用 F7 定位探索阶段，再给每幅结果图写一句“谁相对谁”：F14 是模型内翻译方案变化，F15 是原型与完整参考的误差，F16 是独立硬件改动带来的趋势。练习：如果 F14 显示有代价，为什么还需要 F15？因为估计一个代价与验证估计可靠性是不同问题。

## 把目标时序与宿主成本分开

读 [§VI-D（p9）与 F10（p10）](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=9)时，在笔记上分写“预热阶段模拟周期比”和“采样阶段性能误差”。宿主花了几秒，需要另有宿主计时证据；不能把周期比直接填进该栏。可接着读 [Virtuoso 整篇案例](reading-virtuoso-figures.md)，对照它如何区分机制、模型验证、宿主成本和目标系统代价；两篇指标不能直接相除。

[§VIII（p12）](https://tutorial.xiangshan.cc/hpca26/slides/tracertl_hpca2026.pdf#page=12)将 Assassyn 列为相关工作。这里仅比较路径：TraceRTL 从现有 RTL 派生 trace-driven 模型；Assassyn 从高层设计描述生成模拟器。实现语言以 [Assassyn 自己的 F9](../gallery/papers/isca-2025-assassyn.md#f9) 为据，其 Rust 调度与 [F10 的生成 RTL](../gallery/papers/isca-2025-assassyn.md#f10) 是两个实现视角；不沿用二手语言概括，也不把 RTL 当仿真宿主。此比较不表示两者用了相同架构、同一负载或相同验证基线。
