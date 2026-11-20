import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class HMFSTests(unittest.TestCase):
 def test_source_scope_and_pages(self):
  data=json.loads((R/'gallery/figures.json').read_text());pid='socc-2025-hmfs'
  fs=[f for f in data['items'] if f['paper_id']==pid]
  self.assertEqual([(f['figure_number'],f['pdf_page']) for f in fs],[(1,3),(3,4)])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100);self.assertNotIn(pid,{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  records={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   self.assertIn('样本外补充',f['paper_short']);self.assertIn('不计入固定100篇',f['source_note'])
   self.assertEqual(f['license_name'],'CC BY 4.0');r=records[f['id']]
   self.assertEqual(r['source_git_blob'],'a49547cfe340c49fc6ad139a4c152bf3d96ab138')
   self.assertEqual(r['source_pdf_sha256'],'8ad56c6daa64712f821649fb456ac6c4a371aa8b83dceb910f5112a9b96260b5')
   self.assertIn('f9b0759f32aaa4b0f64c3667eb25a4134c754492',f['source_page_url'])
   self.assertTrue(r['license_evidence_url'].endswith('#page=1'))
  scope=json.loads((R/'gallery/scope.json').read_text())
  self.assertIn({'paper_id':pid,'fixed_100_sample':False,'figure_numbers':[1,3]},scope['supplemental_papers'])
