# 文件、存储与缓存系统图组怎么读

[返回读图指南索引](../catalog/README.md#source-linked-reading-guides) · [两张机制图怎么对照读](reading-mechanism-pairs.md)

选一个数据项，分别追问：**谁决定它接下来怎么办？它的值或数据块实际在哪里？** 把目录、热度记录、版本引用等控制信息与数据所在位置分开记录，再沿箭头追踪两者如何联系。以下四例展示可练习的读法，不代表各类论文的普遍频率或必须采用的图组。

## Concord（HPCA 2025）：目录命中不等于缓存供数

这里讨论缓存一致性的 Concord，不是同名调度器。先在 [F4（物理第 4 页）](https://iacoma.cs.uiuc.edu/iacoma-papers/hpca25_1.pdf#page=4)找到代理、目录和全局存储，再在 [F5(a)（物理第 6 页）](https://iacoma.cs.uiuc.edu/iacoma-papers/hpca25_1.pdf#page=6)比较三种读路径，沿实线追数据、沿虚线追控制消息。

练习：Node 0 本地没有 B 时，标出步骤 3 查 home 目录与步骤 5 回送 B，分别回答“查到了什么”和“取回了什么”。文中的 remote hit 指 home 目录有条目，并不保证数据来自另一个缓存：共享态下若 home 没有缓存副本，可以向全局存储取数据。将图中画出的示例与正文说明的备用路径分开，不把目录条目当成缓存中的数据副本。

## HotRAP（ATC 2025）：热度决定去向，RALT 不存值

在 [F2（物理第 5 页）](https://www.usenix.org/system/files/atc25-qiu.pdf#page=5)同时追踪 K1、K2：步骤 4 提取，步骤 5 查 RALT 并更新热度，步骤 6 让热 K1 进入合并过程，而冷 K2 不进入。按图注用实线追数据、虚线追控制；“不进入这次合并”不能改写成“从底层删除 K2”。

练习：到 [F3（物理第 6 页）](https://www.usenix.org/system/files/atc25-qiu.pdf#page=6)打开同一个 RALT，区分热键记录与值的实际存放位置，并按 ATC 版的 promotion buffer 术语追踪提升相关路径。RALT 记录热键，不是值的存放处；判断热度的结构与承载值的路径应分别标记。

## SolFS（ATC 2025）：沿版本找改动，再看引用约束

先用 [F6（物理第 7 页）](https://www.usenix.org/system/files/atc25-pan.pdf#page=7)辨认版本链，再在 [F7／F8（物理第 8 页）](https://www.usenix.org/system/files/atc25-pan.pdf#page=8)追踪 APP1 如何从自己上次的 ver=1 走到 ver=4，找出发生改动的范围。F6 自己从已有 ver=1 开始，F7 则从 ver=0 起、APP1 首次备份得到 ver=1；两图的版本号不必一一接续。练习时把 APP 仍引用哪些版本另列出来，判断这些引用如何限制版本合并。

F7 解释上传，F8 解释版本化 inode 压缩；二者关联的是版本及其引用，不应把 F8 说成上传或同步的下一步。区分“需要上传哪些改动”与“哪些版本结构还能保留或合并”这两个决策。

## DeLFS（OSDI 2026）：把脏页操作接到目标日志段

沿[现有 DeLFS 指南](../catalog/README.md#reading-guide-osdi2026-delfs)，在 [F4／F5（正式 PDF 物理第 6 页）](https://www.usenix.org/system/files/osdi26-ahn.pdf#page=6)追踪一个脏页及其目标日志段。练习用共享的步骤 4 连接操作顺序与结构：从本核当前段取得下一可写块，并推进偏移。

F6 是当前段耗尽且本核无空闲段时向其他核心寻找、分配段的独立例子，另起编号。先确认这个触发条件，再追踪空间来源，不把 F6 接成 F4／F5 的同一套编号，也不把图形宽度当成实测时延。

本文只链接原文并提供原创阅读练习，不复制 PDF 或图像，不绘制替代图，不收录实验图，也不增加原图库数量。图组中的示例解释控制与位置的关系，不替代性能测量或正确性证明。
