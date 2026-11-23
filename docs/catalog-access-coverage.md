# 固定100篇：原图与图号级导读入口盘点

由 `python scripts/report_catalog_access.py` 按唯一 paper_id 生成；可用 `--check` 检查。

原图口径：gallery/figures.json 中至少有一个已发布条目（沿用项目条目口径，含明确标注的机制子区域）。导读口径：有图号及物理页／官方图锚点的专门原文指南，或下表明确登记的独立／跨论文练习。原图页自身的常规图注不重复算成专门导读。仅有论文首页链接、初读数量或题名不算导读。

这些都是入口覆盖，不是全篇深读、完整视觉审核、科学复现或授权完成率；混合／实验图在导读中仅作证据不计入原图库。样本外补充论文不进入分母。

| 口径 | 篇数 |
|---|---:|
| 至少一个原图条目 A | 39 |
| 至少一个图号级专门导读 B | 61 |
| 两者重叠 A∩B | 4 |
| 只有原图 | 35 |
| 只有导读 | 57 |
| 至少一种入口 A∪B | 96 |
| 两者均无 | 4 |

## 本批变化

本批从22篇缺口补入18篇：Asterinas、FastPath、ReChisel、LMI、Mascot、PIMnet、ROW、VR-Pipe、DSAssassin、SALT、FALCON、Move the Brain、Bumper、DICE、HARTBREAKER、IroKnight、Drishti、SMX。每篇仅新增一个非实验图号、物理页及作用说明，详见下表的专门导读链接。依据可读图注与正文核对，未完成新视觉审核，不上传图片或PDF。

批前：A=39、B=43、交集4、并集78、两者均无22。批后数字见上表。既有跨论文指南、独立案例及上一批 FiDe／μShell／DARTH-PUM 均计入批前，不冒充本批新增覆盖。原图库保持整体45篇196条、固定样本39篇183条；样本外6篇13条不计入固定100篇覆盖。

## 仍无两类入口：精确缺口

以下只表示仓库尚无所定义的入口，不表示论文没有非实验图或禁止转载；未核实的仍留作未完成。以下分别记录本轮读取阻碍与沿用的既有缺口，未重试此前被拒绝的下载。

- `dac-2025-chord` — CHORD: Composable Hybrid Optical Reconfigurable Diffractive Framework For Optical Neural Network：既有链接是 MDR-HDONN 前身稿，尚不能核定为 CHORD 的相应图；本轮未请求，不转用前身图号。
- `hpca-2026-nugget` — Nugget: Portable Program Snippets：精确 arXiv v2 的先前下载已返回403；本轮未重试，也无新增可核验素材。
- `isca-2026-dejavu` — DejaVu: Why You Should Write to Your DRAM Rows Twice, Carefully：本轮正常网页读取失败：文件长度16087357字节，超过工具大小上限；未换路线获取。
- `micro-2025-modern-gpu` — Dissecting and Modeling the Architecture of Modern GPU Cores：本轮既有机构来源返回403 Forbidden；已停止该路线，未找替代地址。

## 逐 ID 明细

| 固定样本 ID | 原图入口 | 专门导读入口 |
|---|---|---|
| `asplos-2025-chassis` | [已发布](../gallery/papers/asplos-2025-chassis.md) | — |
| `asplos-2025-fusion` | [已发布](../gallery/papers/asplos-2025-fusion.md) | — |
| `asplos-2025-pccheck` | [已发布](../gallery/papers/asplos-2025-pccheck.md) | — |
| `asplos-2025-tally` | [已发布](../gallery/papers/asplos-2025-tally.md) | — |
| `asplos-2025-virtuoso` | [已发布](../gallery/papers/asplos-2025-virtuoso.md) | [图号级导读](../docs/reading-virtuoso-figures.md) |
| `asplos-2026-compass` | [已发布](../gallery/papers/asplos-2026-compass.md) | — |
| `asplos-2026-cxlalloc` | [已发布](../gallery/papers/asplos-2026-cxlalloc.md) | — |
| `asplos-2026-cxlmodel` | [已发布](../gallery/papers/asplos-2026-cxlmodel.md) | — |
| `asplos-2026-darth` | — | [图号级导读](../catalog/README.md#reading-guide-asplos-2026-darth) |
| `asplos-2026-lilac` | — | [图号级导读](../catalog/README.md#reading-guide-asplos-2026-lilac) |
| `asplos-2026-naylor` | [已发布](../gallery/papers/asplos-2026-naylor.md) | — |
| `asplos-2026-radshield` | [已发布](../gallery/papers/asplos-2026-radshield.md) | — |
| `asplos-2026-rteaal` | [已发布](../gallery/papers/asplos-2026-rteaal.md) | [图号级导读](../docs/tracing-data-across-figures.md) |
| `asplos-2026-step` | [已发布](../gallery/papers/asplos-2026-step.md) | — |
| `asplos-2026-xpdl` | — | [图号级导读](../catalog/README.md#reading-guide-asplos-2026-xpdl) |
| `atc2025-asterinas` | — | [图号级导读](../catalog/README.md#reading-guide-atc2025-asterinas) |
| `atc2025-fide` | — | [图号级导读](../catalog/README.md#reading-guide-atc2025-fide) |
| `atc2025-hotrap` | — | [图号级导读](../docs/reading-storage-figures.md) |
| `atc2025-leocraft` | — | [图号级导读](../catalog/README.md#reading-guide-atc2025-leocraft) |
| `atc2025-rhone` | — | [图号级导读](../catalog/README.md#reading-guide-atc2025-rhone) |
| `atc2025-solfs` | — | [图号级导读](../docs/reading-storage-figures.md) |
| `atc2025-voltrix` | — | [图号级导读](../catalog/README.md#reading-guide-atc2025-voltrix) |
| `atc2025-xrt` | — | [图号级导读](../catalog/README.md#reading-guide-atc2025-xrt) |
| `dac-2024-qpilot` | [已发布](../gallery/papers/dac-2024-qpilot.md) | — |
| `dac-2025-chord` | — | — |
| `dac-2025-dco` | — | [图号级导读](../catalog/README.md#reading-guide-dac-2025-dco) |
| `dac-2025-fastpath` | — | [图号级导读](../catalog/README.md#reading-guide-dac-2025-fastpath) |
| `dac-2025-gem` | — | [图号级导读](../catalog/README.md#reading-guide-dac-2025-gem) |
| `dac-2025-mage` | [已发布](../gallery/papers/dac-2025-mage.md) | — |
| `dac-2025-pacq` | — | [图号级导读](../catalog/README.md#reading-guide-dac-2025-pacq) |
| `dac-2025-rechisel` | — | [图号级导读](../catalog/README.md#reading-guide-dac-2025-rechisel) |
| `dac-2025-rights` | [已发布](../gallery/papers/dac-2025-rights.md) | — |
| `dac-2025-ruplace` | — | [图号级导读](../catalog/README.md#reading-guide-dac-2025-ruplace) |
| `dac-2025-simphony` | — | [图号级导读](../catalog/README.md#reading-guide-dac-2025-simphony) |
| `dac-2026-sandwich` | [已发布](../gallery/papers/dac-2026-sandwich.md) | — |
| `dac-2026-sp2rint` | — | [图号级导读](../catalog/README.md#reading-guide-dac-2026-sp2rint) |
| `dac-2026-trace` | [已发布](../gallery/papers/dac-2026-trace.md) | — |
| `dac-2026-zkflex` | [已发布](../gallery/papers/dac-2026-zkflex.md) | — |
| `hpca-2025-concord` | — | [图号级导读](../docs/reading-storage-figures.md) |
| `hpca-2025-lmi` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2025-lmi) |
| `hpca-2025-mascot` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2025-mascot) |
| `hpca-2025-pimnet` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2025-pimnet) |
| `hpca-2025-quclear` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2025-quclear) |
| `hpca-2025-row` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2025-row) |
| `hpca-2025-vrpipe` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2025-vrpipe) |
| `hpca-2026-accelflow` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2026-accelflow) |
| `hpca-2026-bard` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2026-bard) |
| `hpca-2026-bpsf` | [已发布](../gallery/papers/hpca-2026-bpsf.md) | — |
| `hpca-2026-dsassassin` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2026-dsassassin) |
| `hpca-2026-nugget` | — | — |
| `hpca-2026-sage` | [已发布](../gallery/papers/hpca-2026-sage.md) | — |
| `hpca-2026-salt` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2026-salt) |
| `hpca-2026-tracertl` | — | [图号级导读](../catalog/README.md#reading-guide-hpca-2026-tracertl) |
| `ipdps2025-citroen` | — | [图号级导读](../catalog/README.md#reading-guide-ipdps2025-citroen) |
| `ipdps2025-falcon` | — | [图号级导读](../catalog/README.md#reading-guide-ipdps2025-falcon) |
| `ipdps2025-xtask` | — | [图号级导读](../catalog/README.md#reading-guide-ipdps2025-xtask) |
| `ipdps2026-evalnet` | — | [图号级导读](../catalog/README.md#reading-guide-ipdps2026-evalnet) |
| `ipdps2026-move-brain` | — | [图号级导读](../catalog/README.md#reading-guide-ipdps2026-move-brain) |
| `ipdps2026-uctrace` | [已发布](../gallery/papers/ipdps2026-uctrace.md) | — |
| `ipdps2026-vla-quantum` | [已发布](../gallery/papers/ipdps2026-vla-quantum.md) | [图号级导读](../docs/tracing-data-across-figures.md) |
| `isca-2026-bullettime` | — | [图号级导读](../catalog/README.md#reading-guide-isca-2026-bullettime) |
| `isca-2026-bumper` | — | [图号级导读](../catalog/README.md#reading-guide-isca-2026-bumper) |
| `isca-2026-chime` | [已发布](../gallery/papers/isca-2026-chime.md) | — |
| `isca-2026-dcc` | [已发布](../gallery/papers/isca-2026-dcc.md) | — |
| `isca-2026-dejavu` | — | — |
| `isca-2026-dice` | — | [图号级导读](../catalog/README.md#reading-guide-isca-2026-dice) |
| `isca-2026-dicephy` | [已发布](../gallery/papers/isca-2026-dicephy.md) | — |
| `isca-2026-grains` | [已发布](../gallery/papers/isca-2026-grains.md) | — |
| `isca-2026-hartbreaker` | — | [图号级导读](../catalog/README.md#reading-guide-isca-2026-hartbreaker) |
| `isca-2026-iroknight` | — | [图号级导读](../catalog/README.md#reading-guide-isca-2026-iroknight) |
| `isca-2026-loadeddice` | [已发布](../gallery/papers/isca-2026-loadeddice.md) | — |
| `isca-2026-lotus` | — | [图号级导读](../catalog/README.md#reading-guide-isca-2026-lotus) |
| `isca-2026-revelator` | [已发布](../gallery/papers/isca-2026-revelator.md) | — |
| `isca-2026-rhodes` | — | [图号级导读](../catalog/README.md#reading-guide-isca-2026-rhodes) |
| `isca-2026-tusq` | — | [图号级导读](../catalog/README.md#reading-guide-isca-2026-tusq) |
| `micro-2025-atr` | [已发布](../gallery/papers/micro-2025-atr.md) | — |
| `micro-2025-columndisturb` | [已发布](../gallery/papers/micro-2025-columndisturb.md) | — |
| `micro-2025-cxlnic` | [已发布](../gallery/papers/micro-2025-cxlnic.md) | — |
| `micro-2025-drishti` | — | [图号级导读](../catalog/README.md#reading-guide-micro-2025-drishti) |
| `micro-2025-leakyhammer` | [已发布](../gallery/papers/micro-2025-leakyhammer.md) | — |
| `micro-2025-loopfrog` | [已发布](../gallery/papers/micro-2025-loopfrog.md) | — |
| `micro-2025-lvm` | [已发布](../gallery/papers/micro-2025-lvm.md) | — |
| `micro-2025-modern-gpu` | — | — |
| `micro-2025-netsparse` | [已发布](../gallery/papers/micro-2025-netsparse.md) | — |
| `micro-2025-omnisim` | [已发布](../gallery/papers/micro-2025-omnisim.md) | [图号级导读](../catalog/README.md#reading-guide-micro-2025-omnisim) |
| `micro-2025-quartz` | [已发布](../gallery/papers/micro-2025-quartz.md) | — |
| `micro-2025-shadow` | — | [图号级导读](../catalog/README.md#reading-guide-micro-2025-shadow) |
| `micro-2025-smx` | — | [图号级导读](../catalog/README.md#reading-guide-micro-2025-smx) |
| `micro-2025-stackengine` | [已发布](../gallery/papers/micro-2025-stackengine.md) | — |
| `micro-2025-streamtensor` | [已发布](../gallery/papers/micro-2025-streamtensor.md) | — |
| `osdi2026-arca` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-arca) |
| `osdi2026-balboa` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-balboa) |
| `osdi2026-bodega` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-bodega) |
| `osdi2026-delfs` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-delfs) |
| `osdi2026-farlock` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-farlock) |
| `osdi2026-hs` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-hs) |
| `osdi2026-mimesys` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-mimesys) |
| `osdi2026-mushell` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-mushell) |
| `osdi2026-sbb` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-sbb) |
| `osdi2026-vtc` | — | [图号级导读](../catalog/README.md#reading-guide-osdi2026-vtc) |
