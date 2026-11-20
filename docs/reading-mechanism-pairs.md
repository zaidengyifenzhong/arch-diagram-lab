# 两张机制图怎么对照读

[返回原文链接读图指南索引](../catalog/README.md#source-linked-reading-guides)

专题练习：[文件、存储与缓存系统图组怎么读](reading-storage-figures.md)。

先问两图**保留了什么、改变了什么**：共同的可能是一次操作、事件职责或到达场景；变化的可能是观察视角、表达层次或新增机制。找到共同参照后再对应细节，不能只凭相同编号、相似布局或重复标签认定同一个事件或实例。

## DeLFS：同一次操作，换一个观察视角

[图 4／图 5（正式 PDF 物理第 6 页）](https://www.usenix.org/system/files/osdi26-ahn.pdf#page=6)共享同一次脏页刷写的操作编号：图 4 看操作顺序，图 5 看结构与资源，第 4 步可用来核对如何取本核下一可写块并递增偏移。这里可以按编号对齐两图，但图 6 另起编号，不能把它接成同一串操作；图 4 的横向宽度也不是实测时延。

[查看 DeLFS 详细指南](../catalog/README.md#reading-guide-osdi2026-delfs)

## SBB：保留事件职责，展开请求阶段

[图 5（正式 PDF 物理第 7 页）](https://www.usenix.org/system/files/osdi26-hu-kang.pdf#page=7)与[图 6（物理第 9 页）](https://www.usenix.org/system/files/osdi26-hu-kang.pdf#page=9)共享网卡到达通知和定时器抢占的职责，前者展示来源与组织，后者展开请求阶段。两图编号独立，应把到达通知对应接收阶段、把抢占对应应用处理阶段，不能把图 5 的事件号直接当作图 6 的步骤号。

[查看 SBB 详细指南](../catalog/README.md#reading-guide-osdi2026-sbb)

## FARLock：保留到达场景，加入排序信息

[图 1（正式 PDF 物理第 4 页）](https://www.usenix.org/system/files/osdi26-hu-yuehao.pdf#page=4)与[图 4（物理第 6 页）](https://www.usenix.org/system/files/osdi26-hu-yuehao.pdf#page=6)保持 A–E 的到达场景和本地／远程归属，图 4 在双队列上加入全局票号。固定这个共同场景，再比较示例中的授锁顺序怎样变化；到达顺序和等待数字不能当作实测结果或一般时钟保证。

[查看 FARLock 详细指南](../catalog/README.md#reading-guide-osdi2026-farlock)

这些选例提供三种对照思路，不是所有论文必须遵循的作图规范。本文仅链接原页并提供原创建议，不复制论文 PDF 或图像，不增加原图库图片数量；机制图也不替代实验评估或正确性证明。
