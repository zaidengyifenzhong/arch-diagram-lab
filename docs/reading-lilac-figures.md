# Lilac：从参数来源读到时序保证与实现代价

[返回目录指南](../catalog/README.md#reading-guide-asplos-2026-lilac) · [完整指南索引](../catalog/README.md#source-linked-reading-guides)

本案例使用作者站的 **14页 ASPLOS 2026会议版**《Parameterized Hardware Design with Latency-Abstract Interfaces》，DOI [10.1145/3779212.3790199](https://doi.org/10.1145/3779212.3790199)。下列页码均为这份 PDF 的物理页，不混用13页 arXiv v2。这里研究图组怎样支撑论证，不复刻代码、结果表或图像。

## 先用一个问题串起 F3 → F5 → F6

**问：生成器换了加法器或乘法器的延迟，父模块怎样继续把同一次运算的数据和选择信号对齐？**

**答：** [F3（p4）](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=4)先定位参数从哪里来：生成器确定的时序信息应由子模块向上提供。再到 [F5（p5）](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=5)，用两条路径延迟的最大值决定共同输出时刻，为较短路径和选择信号补足延迟。最后用 [F6（p6）](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=6)逐级检查移位寄存器的可用时间窗口。参数求值和模块展开发生在 elaboration；电路运行时才有数据逐拍流动，不能把这两种“流”混为一谈。

## 逐图索引：每幅图承担什么任务

| 图号 | 目的与阅读动作 | 表现形式与边界 | 原文物理页 |
|---|---|---|---|
| F1 | 比较同一类 FPU 如何协调加法和乘法：先看 (a) 固定时序，再看 (b) 可适应时序的接口。 | 两个电路示意；固定时序与弹性接口是设计取舍，不是性能排名。 | [p2](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=2) |
| F2 | 把 F1(a) 落到 Verilog：2拍加法补2拍以对齐4拍乘法，op 选择信号也延迟4拍。 | 固定时序代码 listing；这些常数属于该例，不能推广到所有生成器配置。 | [p3](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=3) |
| F3 | 追两种模块层级中的参数来源：父模块向下给值，与生成器产生参数后向上提供。 | 层级与参数流示意；箭头描述设计展开时的信息，不是运行时数据通路。 | [p4](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=4) |
| F4 | 找接口中的输出参数，观察调用方如何得知生成模块的时序约束。 | 接口代码；输出参数是编译期信息，不能读成额外硬件输出端口。 | [p5](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=5) |
| F5 | 对照错误与修正两份 listing：错误在于使用时刻不匹配，修正通过 max 延迟安排补偿和选择。 | 代码对照与类型检查案例；展示参数化对齐方式，不是运行时测量。 | [p5](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=5) |
| F6 | 从 shift register 代码追到逐拍时序，每前进一级，可用窗口的起止时刻都加一。 | (a) 实现代码与 (b) 时间窗口图；图中时刻来自调度约束，不是仪器测出的延迟分布。 | [p6](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=6) |
| F7 | 先辨认 (a) 语言语法，再看 (b) 怎样把构造编码为 SMT 约束。 | 语法定义与形式规则两部分；公式符号表示语言和推理对象，不是电路连线。 | [p7](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=7) |
| F8 | 检查跨设计的类型检查成本，用来追问方法是否可实际使用。 | 编号为 Figure 的时间表，包含设计、规模和检查时间；是评估证据，不是机制图。 | [p9](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=9) |
| F9 | 比较三种 Vivado divider 的接口，再看按位宽选实现的封装如何隐藏差异。 | 三组接口及选择代码；统一调用接口不意味着内部硬件相同。 | [p10](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=10) |
| F10 | 对同一 Aetherling convolution，比较 Lilac 接口与 ready/valid Verilog 接口把哪些时序责任交给调用方。 | 两组接口 listing；先识别契约，再比较控制实现。 | [p10](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=10) |
| F11 | 跟踪参数化 serializer 如何按输入并行度组织数据供应。 | Lilac 代码；参数决定数据分组及可用时序，不是实测吞吐曲线。 | [p11](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=11) |
| F12 | 找到 ready/valid 实现的发送与接收状态机，观察何时推进数据索引。 | 两个 FSM 的代码；与 F11 比较控制责任，不把不同代码行数直接当作硬件成本。 | [p11](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=11) |
| F13 | 在相同输入并行度 N 下比较完整 GBP 实现的 FPGA 资源和最大频率。 | 综合评估表，虽叫 Figure 仍是实验结果；不是机制图，也不只是 serializer 单模块的成本。 | [p11](https://people.csail.mit.edu/rachit/files/pubs/lilac.pdf#page=11) |

F1–F13 是论文的 Figure 编号序列；正式 **Table 1–3** 另行编号，不计入这13幅，也不能因有些 Figure 呈现为表格就把它们漏掉。

## 两条论证链

**F1(a) → F2 → F3 → F4/F5 → F6：从固定时序集成到可检查的参数化集成。** 先问固定 FPU 依赖哪些延迟常数，再检查生成器改变它们时，父模块从哪里获得新值。F4/F5 把参数来源与使用时刻连起来；F6 则把补偿延迟展开为可以逐级核对的时间窗口。读到末尾应能解释“参数如何帮助对齐”，而不是只记住“加了寄存器”。F7 是另一层证据：它解释编译器如何组织语法与约束检查，不是这条数据通路的下一硬件阶段。

**F10 → F11/F12 → F13：从接口责任到实现，再到有条件的成本比较。** 先以同一卷积为参照，辨认 Lilac 的参数化时序契约与 ready/valid 握手契约。然后比较 serializer 和收发 FSM 如何完成数据供应与接收，最后到 F13 按同一 N 配对查看资源、频率。F13 衡量的是包含这些集成逻辑的 Gaussian Blur Pyramid（GBP）实现，不能把全部差异归因于某一行代码。

例如，N=1 时 Lilac 的 LUT、寄存器用量更少，频率也更高；但 N=4、N=8 时 ready/valid 的频率更高。这个反例足以阻止“Lilac 在每个配置下都更快”的概括。应分别检查资源和频率，再看实验的综合条件；最大频率也不能直接等同端到端应用吞吐。这里仅文字分析结果怎样对应设计，不展示或重画 F8、F13。

## 版本与使用边界

会议 PDF 首页标注 CC BY-NC-ND 4.0；本项目不据此裁剪并公开分发该论文图，也不将另一 arXiv 版本的声明移用于此版本。所有13项均只链接原文，未上传 PDF、截图或原图；它们不计入图库图片收录。本文是这份论文的图组阅读案例，不是实验复现或对所有参数化实现的独立正确性证明。
