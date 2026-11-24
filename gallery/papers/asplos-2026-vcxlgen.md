# vCXLGen: Automated Synthesis and Verification of CXL Bridges for Heterogeneous Architectures

[返回图集](../README.md) · vCXLGen · ASPLOS 2026 · 样本外补充

研究对象：RTL验证、生成与修复工具 / vCXLGen异构缓存一致性协议桥的自动合成与验证（样本外补充）

20页作者Git稿，样本外补充，不计入固定100篇；仅收完整非实验F4/F6，不上传PDF，不声称与出版社文件字节一致。

F4（物理p5）追一次跨域事务 → 原文F5（物理p7，仅链接）看桥合成过程 → F6（物理p7）追 (S,S)+GetM 的状态分支。

读图练习：F4 中本地 GetM 为什么不能立即回复？到 F6 找出全局请求、响应和本地 Ack 对应的转换及动作；图中的状态对分别记录本地目录与全局缓存视角，不能把每个状态当作另一台机器。消息时序和转换分支提供不同视角，不替代形式验证。

[F5：合成流程与输入事务（原文物理p7，仅链接）](https://raw.githubusercontent.com/NicCarp11/niccarp11.github.io/7d759dda2b5628601d8338c563449a7fbd31edeb/papers/vcxlgen-asplos26-preprint.pdf#page=7)。它解释如何把本地和全局输入协议组合成桥，不把生成的 SLICC 模型称作运行生成器的宿主硬件。

来源：[精确作者Git文件](https://github.com/NicCarp11/niccarp11.github.io/blob/7d759dda2b5628601d8338c563449a7fbd31edeb/papers/vcxlgen-asplos26-preprint.pdf)。首页可见 CC BY 4.0、DOI 10.1145/3779212.3790245；20页作者稿，不推定与正式出版社文件字节相同。源PDF SHA-256：`7b94d57e9f5e67e92cf3acf554c45b77e9877838ada07aeaad484acf32228113`；Git blob：`155054ad656dec2d65d69f81d3c4b57b7660d60c`。已目视核对首页、图页、图注和最终裁图，未发现这两图的第三方署名或许可例外。PDF不随库分发。

## 图号导航

[F4](#f4) · [F6](#f6)

## F4

**非实验图 · 事务消息时序图**

![vCXLGen 图4，作者稿物理第5页：共享状态下的 store miss 先触发本地 GetM，再由桥发送全局 MemRd_A；沿另一主机的失效及响应路径返回，最后本地 Ack 才让请求完成。纵向位置示意消息先后，不是实测时间刻度；图中桥状态同时包含本地与全局协议状态。](../assets/asplos-2026-vcxlgen-F4-59777761ef8bdad6.png)

[原文物理页 5](https://raw.githubusercontent.com/NicCarp11/niccarp11.github.io/7d759dda2b5628601d8338c563449a7fbd31edeb/papers/vcxlgen-asplos26-preprint.pdf#page=5) · [许可证 CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

共享状态下的 store miss 先触发本地 GetM，再由桥发送全局 MemRd_A；沿另一主机的失效及响应路径返回，最后本地 Ack 才让请求完成。纵向位置示意消息先后，不是实测时间刻度；图中桥状态同时包含本地与全局协议状态。 样本外补充，不计入固定100篇样本或其分类覆盖完成量。

署名：Anatole Lefort, Julian Pritzi, Nicolò Carpentieri, David Schall, Simon Dittrich, Soham Chakraborty, Nicolai Oswald, Pramod Bhatotia. vCXLGen: Automated Synthesis and Verification of CXL Bridges for Heterogeneous Architectures. ASPLOS 2026. DOI: https://doi.org/10.1145/3779212.3790245. Copyright 2026 held by the owner/authors. Source: https://github.com/NicCarp11/niccarp11.github.io/blob/7d759dda2b5628601d8338c563449a7fbd31edeb/papers/vcxlgen-asplos26-preprint.pdf. Version: 20-page ASPLOS 2026 author preprint in Git commit 7d759dda2b5628601d8338c563449a7fbd31edeb, blob 155054ad656dec2d65d69f81d3c4b57b7660d60c; not asserted publisher-byte-identical. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Whole figure cropped from the exact author preprint and rasterized at 300 dpi; caption excluded, all protocol labels, states, message arrows and action annotations retained; no redrawing or recoloring. No endorsement implied.

修改说明：Whole figure cropped from the exact author preprint and rasterized at 300 dpi; caption excluded, all protocol labels, states, message arrows and action annotations retained; no redrawing or recoloring.

## F6

**非实验图 · 协议状态转换图**

![vCXLGen 图6，作者稿物理第7页：把 (S,S)+GetM 展开成桥的转换图，沿 Cmp-E、Data 以及可能到来的 BISnpInv 追踪不同分支；动作注释分别说明发出全局请求和向本地回复。该图展示合成结果的一部分，不是仅靠这张图就证明整个协议正确。](../assets/asplos-2026-vcxlgen-F6-098feee83088faff.png)

[原文物理页 7](https://raw.githubusercontent.com/NicCarp11/niccarp11.github.io/7d759dda2b5628601d8338c563449a7fbd31edeb/papers/vcxlgen-asplos26-preprint.pdf#page=7) · [许可证 CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

把 (S,S)+GetM 展开成桥的转换图，沿 Cmp-E、Data 以及可能到来的 BISnpInv 追踪不同分支；动作注释分别说明发出全局请求和向本地回复。该图展示合成结果的一部分，不是仅靠这张图就证明整个协议正确。 样本外补充，不计入固定100篇样本或其分类覆盖完成量。

署名：Anatole Lefort, Julian Pritzi, Nicolò Carpentieri, David Schall, Simon Dittrich, Soham Chakraborty, Nicolai Oswald, Pramod Bhatotia. vCXLGen: Automated Synthesis and Verification of CXL Bridges for Heterogeneous Architectures. ASPLOS 2026. DOI: https://doi.org/10.1145/3779212.3790245. Copyright 2026 held by the owner/authors. Source: https://github.com/NicCarp11/niccarp11.github.io/blob/7d759dda2b5628601d8338c563449a7fbd31edeb/papers/vcxlgen-asplos26-preprint.pdf. Version: 20-page ASPLOS 2026 author preprint in Git commit 7d759dda2b5628601d8338c563449a7fbd31edeb, blob 155054ad656dec2d65d69f81d3c4b57b7660d60c; not asserted publisher-byte-identical. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Whole figure cropped from the exact author preprint and rasterized at 300 dpi; caption excluded, all protocol labels, states, message arrows and action annotations retained; no redrawing or recoloring. No endorsement implied.

修改说明：Whole figure cropped from the exact author preprint and rasterized at 300 dpi; caption excluded, all protocol labels, states, message arrows and action annotations retained; no redrawing or recoloring.
