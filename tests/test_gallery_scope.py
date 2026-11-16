import hashlib,json,re,unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class ImageParser(HTMLParser):
 def __init__(self):super().__init__();self.images=[]
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.images.append(dict(attrs)['src'])
class GalleryScopeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((ROOT/'gallery/figures.json').read_text());cls.items=cls.data['items'];cls.ids={f['id'] for f in cls.items};cls.assets={f['asset'] for f in cls.items}
 def test_exact_coverage(self):
  self.assertEqual(len(self.items),172);self.assertEqual(len({f['paper_id'] for f in self.items}),36);self.assertEqual(sum(f['paper_id']=='dac-2026-sandwich' for f in self.items),3);self.assertTrue(all(f['category']=='非实验图' for f in self.items))
 def test_no_extra_assets(self):self.assertEqual({p.relative_to(ROOT/'gallery').as_posix() for p in (ROOT/'gallery/assets').glob('*')},self.assets)
 def test_inline_and_noscript(self):
  h=(ROOT/'gallery/index.html').read_text();m=re.search(r'<script id="gallery-data" type="application/json">(.*?)</script>',h,re.S);self.assertEqual(json.loads(m[1]),self.data)
  n=re.search(r'<noscript>(.*?)</noscript>',h,re.S)[1];p=ImageParser();p.feed(n);self.assertEqual(set(p.images),self.assets);self.assertEqual(len(p.images),172)
 def test_license_byte_bindings(self):
  ls=json.loads((ROOT/'gallery/licenses.json').read_text())['items'];self.assertEqual({f['id'] for f in ls},self.ids)
  for f in ls:self.assertEqual(hashlib.sha256((ROOT/'gallery'/f['asset']).read_bytes()).hexdigest(),f['sha256'])
 def test_catalog(self):
  c=json.loads((ROOT/'catalog/papers.json').read_text());self.assertEqual(len(c['papers']),100);self.assertEqual(sum(p['public_gallery']['figure_count'] for p in c['papers']),172)
  for p in c['papers']:self.assertEqual(set(p['public_gallery']['figure_numbers']),{f['figure_number'] for f in self.items if f['paper_id']==p['paper_id']})
 def test_paper_pages(self):
  pages=list((ROOT/'gallery/papers').glob('*.md'));self.assertEqual(len(pages),36)
  for p in pages:
   found=re.findall(r'!\[[^\]]*\]\(\.\./(assets/[^)]+)\)',p.read_text());self.assertEqual(set(found),{f['asset'] for f in self.items if f['paper_id']==p.stem})
 def test_guides_only_selected(self):
  available={(f['paper_id'],'F'+str(f['figure_number'])) for f in self.items}
  for g in self.data['reading_guides']:
   for e in g['source_examples']:self.assertIn((g['paper_id'],e['figure_id']),available)

 def test_curated_ids(self):
  s=json.loads((ROOT/'gallery/scope.json').read_text());self.assertEqual(len(s['retained_prior_figures']),154);self.assertEqual(len(s['new_figures']),16);self.assertEqual(set(s['retained_prior_figures']+s['new_figures']+[x['id'] for x in s['approved_subregions']]),self.ids)

 def test_current_display_notices(self):
  by={}
  for f in self.items:by.setdefault(f['paper_id'],[]).append(f['figure_number'])
  for f in self.items:
   if f.get('paper_notice'):
    ns=sorted(by[f['paper_id']]);expected='本图库当前收录'+str(len(ns))+'张非实验图：'+'、'.join('F'+str(n) for n in ns)+'。'
    self.assertIn(expected,f['paper_notice']);self.assertIn(f['paper_notice'],(ROOT/'gallery/papers'/str(f['paper_id']+'.md')).read_text())
  catalog=json.loads((ROOT/'catalog/papers.json').read_text())
  for p in catalog['papers']:
   note=p.get('source_note','')
   if '本图库当前收录' in note:
    ns=sorted(by[p['paper_id']]);self.assertIn('本图库当前收录'+str(len(ns))+'张非实验图：'+'、'.join('F'+str(n) for n in ns)+'。',note)
  u=next(p for p in catalog['papers'] if p['paper_id']=='ipdps2026-uctrace')['source_note']
  self.assertIn('本图库当前收录2张非实验图：F1、F2。',u);self.assertNotIn('当前显示8张',u);self.assertNotIn('图6采用',u)
  for fact in ['13页arXiv v1','11页','5位作者']:self.assertIn(fact,u)
  nugget=next(p for p in catalog['papers'] if p['paper_id']=='hpca-2026-nugget')
  self.assertIn('当前不收录',nugget['source_note']);self.assertNotIn('2–11',nugget['source_note'])
 def test_source_version_counts_preserved(self):
  q=next(f for f in self.items if f['paper_id']=='dac-2024-qpilot');self.assertIn('十页扩展稿（16图）',q['paper_notice'])
  u=next(f for f in self.items if f['paper_id']=='ipdps2026-uctrace');self.assertIn('13页arXiv v1',u['paper_notice']);self.assertNotIn('当前显示8张',u['paper_notice']);self.assertNotIn('图6采用',u['paper_notice'])
  dice=next(f for f in self.items if f['paper_id']=='isca-2026-dicephy');self.assertNotIn('22张',dice['paper_notice']);self.assertNotIn('图13以',dice['paper_notice']);self.assertIn('图7的密集网表',dice['paper_notice'])

class LicensePresentationTests(unittest.TestCase):
 def test_ncsa_per_image_and_license_counts(self):
  from collections import Counter
  data=json.loads((ROOT/'gallery/figures.json').read_text())['items']
  self.assertEqual(Counter(f['license_name'] for f in data),{'CC BY 4.0':161,'CC0 1.0':4,'CC BY 2.5':1,'CC BY-NC-SA 4.0':6})
  licenses={f['id']:f for f in json.loads((ROOT/'gallery/licenses.json').read_text())['items']}
  for f in data:
   if f['license_name']=='CC BY-NC-SA 4.0':
    self.assertEqual(f['adaptation_license_url'],f['license_url']);self.assertIn('非商业',f['reuse_notice']);self.assertIn('相同许可',f['reuse_notice'])
    self.assertEqual(licenses[f['id']]['reuse_notice'],f['reuse_notice'])
    self.assertIn(f['reuse_notice'],(ROOT/'gallery/papers'/f"{f['paper_id']}.md").read_text())
 def test_full_download_instruction(self):
  for n in ['README.md','gallery/README.md']:
   text=(ROOT/n).read_text();self.assertIn('完整下载仓库',text);self.assertIn('不能仅下载 HTML',text)
 def test_gallery_local_dependencies(self):
  from urllib.parse import urlsplit,unquote
  class Links(HTMLParser):
   def __init__(self):super().__init__();self.links=[]
   def handle_starttag(self,tag,attrs):
    for k,v in attrs:
     if k in ['href','src']:self.links.append(v)
  p=Links();p.feed((ROOT/'gallery/index.html').read_text())
  for u in p.links:
   if not urlsplit(u).scheme and u and not u.startswith('#'):
    self.assertTrue((ROOT/'gallery'/unquote(u.split('#')[0])).is_file(),u)
  for md in (ROOT/'gallery').rglob('*.md'):
   for u in re.findall(r'\]\(([^)]+)\)',md.read_text()):
    if not urlsplit(u).scheme and not u.startswith('#'):self.assertTrue((md.parent/u.split('#')[0]).is_file(),(md,u))

 def test_cxlnic_canonical_object_classification(self):
  data=json.loads((ROOT/'gallery/figures.json').read_text())
  catalog=json.loads((ROOT/'catalog/papers.json').read_text())
  canonical=next(p for p in catalog['papers'] if p['paper_id']=='micro-2025-cxlnic')
  obj=next(p for p in data['paper_objects'] if p['paper_id']==canonical['paper_id'])
  guide=next(p for p in data['reading_guides'] if p['paper_id']==canonical['paper_id'])
  for key in ['object_group','specific_object']:self.assertEqual(obj[key],canonical[key])
  self.assertEqual(guide['primary_object'],canonical['object_group']);self.assertEqual(guide['specific_object'],canonical['specific_object'])
  for name in ['gallery/README.md','gallery/papers/micro-2025-cxlnic.md','gallery/index.html']:
   text=(ROOT/name).read_text()
   for key in ['object_group','specific_object']:self.assertIn(canonical[key],text)
