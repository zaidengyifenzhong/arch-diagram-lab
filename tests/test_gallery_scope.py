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
  self.assertEqual(len(self.items),157);self.assertEqual(len({f['paper_id'] for f in self.items}),32);self.assertEqual(sum(f['paper_id']=='dac-2026-sandwich' for f in self.items),3);self.assertTrue(all(f['category']=='非实验图' for f in self.items))
 def test_no_extra_assets(self):self.assertEqual({p.relative_to(ROOT/'gallery').as_posix() for p in (ROOT/'gallery/assets').glob('*')},self.assets)
 def test_inline_and_noscript(self):
  h=(ROOT/'gallery/index.html').read_text();m=re.search(r'<script id="gallery-data" type="application/json">(.*?)</script>',h,re.S);self.assertEqual(json.loads(m[1]),self.data)
  n=re.search(r'<noscript>(.*?)</noscript>',h,re.S)[1];p=ImageParser();p.feed(n);self.assertEqual(set(p.images),self.assets);self.assertEqual(len(p.images),157)
 def test_license_byte_bindings(self):
  ls=json.loads((ROOT/'gallery/licenses.json').read_text())['items'];self.assertEqual({f['id'] for f in ls},self.ids)
  for f in ls:self.assertEqual(hashlib.sha256((ROOT/'gallery'/f['asset']).read_bytes()).hexdigest(),f['sha256'])
 def test_catalog(self):
  c=json.loads((ROOT/'catalog/papers.json').read_text());self.assertEqual(len(c['papers']),100);self.assertEqual(sum(p['public_gallery']['figure_count'] for p in c['papers']),157)
  for p in c['papers']:self.assertEqual(set(p['public_gallery']['figure_numbers']),{f['figure_number'] for f in self.items if f['paper_id']==p['paper_id']})
 def test_paper_pages(self):
  pages=list((ROOT/'gallery/papers').glob('*.md'));self.assertEqual(len(pages),32)
  for p in pages:
   found=re.findall(r'!\[[^\]]*\]\(\.\./(assets/[^)]+)\)',p.read_text());self.assertEqual(set(found),{f['asset'] for f in self.items if f['paper_id']==p.stem})
 def test_guides_only_selected(self):
  available={(f['paper_id'],'F'+str(f['figure_number'])) for f in self.items}
  for g in self.data['reading_guides']:
   for e in g['source_examples']:self.assertIn((g['paper_id'],e['figure_id']),available)

 def test_curated_ids(self):
  s=json.loads((ROOT/'gallery/scope.json').read_text());self.assertEqual(len(s['retained_prior_figures']),154);self.assertEqual(len(s['new_figures']),3);self.assertEqual(set(s['retained_prior_figures']+s['new_figures']),self.ids)

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
