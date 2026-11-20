import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class FixTests(unittest.TestCase):
 def test_source_scope_and_pages(self):
  data=json.loads((R/'gallery/figures.json').read_text());pid='eurosys-2026-fix'
  fs=[f for f in data['items'] if f['paper_id']==pid]
  self.assertEqual([(f['figure_number'],f['pdf_page']) for f in fs],[(1,5),(6,7)])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100);self.assertNotIn(pid,{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  records={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   self.assertIn('样本外补充',f['paper_short']);self.assertIn('不计入固定100篇',f['source_note'])
   self.assertEqual(f['license_name'],'CC BY 4.0');r=records[f['id']]
   self.assertEqual(r['source_git_blob'],'e0850a798517208e74c585615359abaa15a5480c')
   self.assertEqual(r['source_pdf_sha256'],'e873108d7db61e45fbf9b2510e8aabdd8db100e23edb74645adfe09642486464')
   self.assertIn('a9ee71a85c58eb48c635725d2128188649144872',f['source_page_url'])
   self.assertTrue(r['license_evidence_url'].endswith('#page=1'))
  scope=json.loads((R/'gallery/scope.json').read_text())
  self.assertIn({'paper_id':pid,'fixed_100_sample':False,'figure_numbers':[1,6]},scope['supplemental_papers'])
