# 离线图库管线

小工具用于候选提取、技术校验和显式白名单导出。不会联网取论文、判断法律权利、批准候选、上传文件或发布站点。技术校验不是许可审查，也不证明论文实验结论。

## 环境与技术校验

Python 3.10+、Pillow；可选 PDF 提取依赖 PyMuPDF。筛选测试使用 Node.js，无 npm 依赖。

```sh
python -m pip install Pillow
# 仅在需要本地 PDF 提取时：
python -m pip install PyMuPDF
python -m unittest discover -s tests -p 'test_gallery_pipeline.py'
node tests/test_gallery_filters.cjs
python scripts/gallery_pipeline.py validate --metadata gallery/figures.json --asset-root gallery
```

`validate` 解码每张 PNG，核对尺寸、必需元数据、唯一身份、物理页链接及相对路径，返回实际 SHA256。未传 `--approvals` 时仅作技术检查，不能据此公开图片。文件名的历史身份后缀不一定是摘要。JavaScript 测试覆盖筛选、对象映射与图号引用，不是浏览器或 DOM 测试。

## 本地候选提取（可选）

只用已合法持有且允许当前用途的本地 PDF，先核对固定版本与 SHA256。页号为从 1 起的 PDF 物理页，矩形坐标单位为 PDF 点。

```sh
python scripts/gallery_pipeline.py extract \
  --pdf /path/to/local-paper.pdf --sha256 <源PDF的64位SHA256> \
  --source-url https://example.org/paper-v1.pdf \
  --rights-note '该固定版本的合法访问依据及本地研究用途' \
  --page 3 --rect 40 80 300 240 --dpi 240 --output /path/to/new-candidate.png
```

输出 PNG 和 `.candidate.json`，状态为 `unreviewed`、`public_redistribution=false`。摘要不符、页/裁剪越界、已有输出会停止。工具不改图中文字、颜色或数值，不能解决原图重叠或缺失信息。

## 独立审核门槛

对照同一固定版本整页、图注与正文核对裁剪、图号/页号、实验分类、基线/单位、版本专属许可、第三方子图、署名与修改说明。可访问不等于可再分发；别的版本许可不能移用。未知、禁止、仅私有或第三方权利未清的图不加入公开白名单。

批准条目绑定实际 PNG 字节和确切源 PDF。以下是输入格式，不是自动生成的权利声明；占位值不能直接使用：

```json
{"items":[{
  "id":"paper-F1",
  "asset":"assets/paper-F1.png",
  "decision":"approved",
  "public_redistribution":true,
  "third_party_clearance":true,
  "nonexperimental_clearance":true,
  "sha256":"<实际PNG的64位SHA256>",
  "source_sha256":"<确切来源PDF的64位SHA256>",
  "source_page_url":"https://example.org/paper-v1.pdf#page=3",
  "license_name":"CC BY 4.0",
  "license_url":"https://creativecommons.org/licenses/by/4.0/",
  "license_evidence_url":"https://example.org/paper-v1-rights",
  "review_note":"固定版本授权及逐图第三方内容核查依据。"
}]}
```

当前策略接受 CC BY 4.0、CC BY 2.5、CC0 及对应标准链接；唯一新增条件支持 CC BY-NC-SA 4.0，须通过下述逐图非商业与相同方式共享门控。其他 ND、NC、SA 许可或版本不自动推断支持。CC BY 仍须保留作者、作品名、来源、许可、修改说明与源内适用权利声明。

## 显式白名单导出

```sh
python scripts/gallery_pipeline.py export \
  --metadata gallery/figures.json --asset-root gallery \
  --approvals /path/to/reviewed-approvals.json --output /path/to/new-export
```

先检查全部元数据与图片，再复制批准图片原始字节。只输出所选 PNG、过滤后的 `figures.json` 和实际摘要/尺寸 `asset-manifest.json`，不复制 PDF、审核文件、网站访问设置、凭据、内部研究草稿或 Git 数据。公开文本字段只接受字符串，图例页号只接受正整数数组，不接受嵌套内部记录；未列入公开字段白名单的字段直接舍弃。阅读建议中指向未导出图片的跳转会移除。导出不继承原始 `coverage_note`，避免把完整图库的数量说明用于子集。目标目录须不存在且不在源目录内。

资产必须是 `assets/` 下规范相对 PNG 路径。绝对路径、`..`、反斜线、百分号编码、空段和符号链接均拒绝。校验失败不会开始导出；I/O 故障仍可能留下部分目录，不能把目录存在当作成功。请在不被其他进程修改的工作副本运行。

发布前还需检查页面链接、署名/许可、远端分支现状和隐私信息，并遵循平台上传审批。工具没有发布功能或绕过审批的能力。

## 非实验范围门控

本项目只接受 `category="非实验图"`，结果图及混合图验证失败。公开批准还须显式 `nonexperimental_clearance=true`，表示独立确认图的解释性作用和混合子图边界；仅改标签不能代替目视审查。暂缓混合图须分离机制子图、重新核对像素/署名/许可后才可加入。

## CC BY-NC-SA 4.0 单图门控

仅支持精确标签及 https://creativecommons.org/licenses/by-nc-sa/4.0/，不推断其他NC或SA版本。保留既有来源PDF SHA、图像SHA、版本专属许可证据URL、第三方内容与非实验图独审要求。新增逐图审批必须显式设置 `noncommercial_use: true`、`sharealike_compliance: true`、`source_version_license_verified: true` 和 `adaptation_license_url` 为上述相同许可URL。缺失、字符串形式true或false均拒绝。

公开元数据须带 `reuse_notice` 精确文本“仅限非商业使用；改编作品须以 CC BY-NC-SA 4.0 相同许可共享。”及 `adaptation_license_url`；导出保留二者。署名、原始许可和修改说明不能删除。该门控不是法律意见，不自动判断用途是否商业，不为未审图片授权，也不将整个集合或代码改为NC-SA。实际商业使用应另向权利人取得许可。
