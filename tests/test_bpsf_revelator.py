import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pipeline',R/'scripts/gallery_pipeline.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class NewPaperTests(unittest.TestCase):
 def test_selection_versions_licenses(self):
  d=json.loads((R/'gallery/figures.json').read_text());cat=json.loads((R/'catalog/papers.json').read_text())
  for pid,nums,ver,license in [('hpca-2026-bpsf',[1,4],'2507.00254v3','CC BY 4.0'),('isca-2026-revelator',[1,4,5,6,8,9],'2508.02007v2','CC0 1.0')]:
   fs=[f for f in d['items'] if f['paper_id']==pid];self.assertEqual([f['figure_number'] for f in fs],nums)
   obj=next(x for x in d['paper_objects'] if x['paper_id']==pid);guide=next(x for x in d['reading_guides'] if x['paper_id']==pid);paper=next(x for x in cat['papers'] if x['paper_id']==pid)
   self.assertEqual(obj['object_group'],guide['primary_object']);self.assertEqual(paper['object_group'],obj['object_group']);self.assertEqual(paper['specific_object'],guide['specific_object'])
   for f in fs:
    self.assertIn(ver,f['source_url']);self.assertIn(ver,f['source_version']);self.assertEqual(f['license_name'],license);self.assertIn('arXiv',f['paper_short'])
    for path in ['gallery/index.html','gallery/papers/'+pid+'.md']:
     text=(R/path).read_text();self.assertIn(f['attribution'],text);self.assertIn(f['source_note'],text)
    for key in ['decision','sha256','asset_sha256','crop_box_pdf_points','review_note','public_redistribution']:self.assertNotIn(key,f)
   if 'bpsf' in pid:self.assertIn('不是最新版',guide['source_ambiguity_or_scope'])
 def test_counts(self):
  d=json.loads((R/'gallery/figures.json').read_text());self.assertEqual(len(d['items']),189);self.assertEqual(len({x['paper_id'] for x in d['items']}),42)
  self.assertEqual(Counter(x['license_name'] for x in d['items']),{'CC BY 4.0':172,'CC0 1.0':10,'CC BY 2.5':1,'CC BY-NC-SA 4.0':6})
  for file in ['README.md','index.html','gallery/README.md','gallery/index.html','catalog/README.md']:
   text=(R/file).read_text();self.assertIn('189',text);self.assertIn('42',text)
class CC0GateTests(unittest.TestCase):
 def setUp(self):
  from PIL import Image
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'assets').mkdir();Image.new('RGB',(8,6),'white').save(self.root/'assets/a.png')
  self.figure=dict(id='test-F1',paper_id='test',paper_title='Synthetic fixture',asset='assets/a.png',figure_type='Mechanism',category='非实验图',attribution='Synthetic fixture, CC0 1.0',modifications='Synthetic test only',source_url='https://example.org/v1',source_page_url='https://example.org/v1.pdf#page=1',license_name='CC0 1.0',license_url='https://creativecommons.org/publicdomain/zero/1.0/',alt_text='Synthetic test',figure_number=1,pdf_page=1,width=8,height=6)
  self.approval=dict(id='test-F1',asset='assets/a.png',decision='approved',public_redistribution=True,third_party_clearance=True,nonexperimental_clearance=True,source_page_url=self.figure['source_page_url'],license_name=self.figure['license_name'],license_url=self.figure['license_url'],source_sha256='a'*64,sha256=hashlib.sha256((self.root/'assets/a.png').read_bytes()).hexdigest(),license_evidence_url='https://example.org/v1-rights',review_note='Synthetic validator fixture, not a real publication approval.')
 def tearDown(self):self.tmp.cleanup()
 def validate(self,f=None,a=None):return p.validate({'items':[f or self.figure]},self.root,{'items':[a or self.approval]})
 def test_canonical_cc0(self):self.assertEqual(len(self.validate()),1)
 def test_legacy_cc0(self):
  self.figure['license_name']=self.approval['license_name']='CC0';self.assertEqual(len(self.validate()),1)
 def test_wrong_license_url(self):
  self.figure['license_url']=self.approval['license_url']='https://creativecommons.org/licenses/by/4.0/'
  with self.assertRaises(ValueError):self.validate()
 def test_clearance_gate_matrix(self):
  for field,value in [('decision','hold'),('public_redistribution',False),('third_party_clearance',False),('nonexperimental_clearance',False),('sha256','0'*64),('source_sha256',''),('license_evidence_url',''),('review_note',''),('source_page_url','https://example.org/other.pdf#page=1')]:
   a=copy.deepcopy(self.approval);a[field]=value
   with self.subTest(field=field),self.assertRaises(ValueError):self.validate(a=a)
 def test_no_cc0_license_substitution(self):
  self.figure['license_name']='CC BY 4.0'
  with self.assertRaises(ValueError):self.validate()
 def test_cc0_export_exact_bytes(self):
  dst=self.root.parent/(self.root.name+'-export');p.export({'items':[self.figure]},self.root,{'items':[self.approval]},dst)
  try:self.assertEqual((dst/'assets/a.png').read_bytes(),(self.root/'assets/a.png').read_bytes());self.assertEqual(json.loads((dst/'figures.json').read_text())['items'][0]['license_name'],'CC0 1.0')
  finally:
   import shutil
   shutil.rmtree(dst)
