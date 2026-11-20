import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class HyPASTests(unittest.TestCase):
 def test_source_scope_and_pages(self):
  data=json.loads((R/'gallery/figures.json').read_text());pid='dac-2026-hypas'
  fs=[f for f in data['items'] if f['paper_id']==pid]
  self.assertEqual([(f['figure_number'],f['pdf_page']) for f in fs],[(1,1),(2,2),(3,3)])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100);self.assertNotIn(pid,{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  records={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   self.assertIn('样本外补充',f['paper_short']);self.assertIn('不计入固定100篇',f['source_note'])
   self.assertEqual(f['license_name'],'CC BY 4.0');r=records[f['id']]
   self.assertEqual(r['source_git_blob'],'f93e5c110325d6d0029b5e8542f5cf77fab633f0')
   self.assertEqual(r['source_pdf_sha256'],'d843ea04b2746e449c7ded65ab06bb5f5d9d11f969251962c6feec7bdb930ca0')
   self.assertIn('2338615840ae4671ca06729e955f175c700e68f2',f['source_page_url'])
   self.assertTrue(r['license_evidence_url'].endswith('#page=1'))
  scope=json.loads((R/'gallery/scope.json').read_text())
  self.assertIn({'paper_id':pid,'fixed_100_sample':False,'figure_numbers':[1,2,3]},scope['supplemental_papers'])
