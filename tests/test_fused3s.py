import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class Fused3STests(unittest.TestCase):
 def test_source_scope_and_pages(self):
  data=json.loads((R/'gallery/figures.json').read_text());pid='ics-2025-fused3s'
  fs=[f for f in data['items'] if f['paper_id']==pid]
  self.assertEqual([(f['figure_number'],f['pdf_page']) for f in fs],[(3,7),(4,8)])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100);self.assertNotIn(pid,{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  records={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   self.assertIn('样本外补充',f['paper_short']);self.assertIn('不计入固定100篇',f['source_note'])
   self.assertEqual(f['license_name'],'CC BY 4.0');r=records[f['id']]
   self.assertEqual(r['source_git_blob'],'1ba1d4710ea0c6500912e8eecba36230b1880e72')
   self.assertEqual(r['source_pdf_sha256'],'ae75894a4490a20d41a5d3d6132bb55c20c5dc798acf7ffafffc4dc7796c0ef8')
   self.assertIn('94c712ec96716e25cdea168e8e1a6e81a16dc547',f['source_page_url'])
   self.assertTrue(r['license_evidence_url'].endswith('#page=1'))
  scope=json.loads((R/'gallery/scope.json').read_text())
  self.assertIn({'paper_id':pid,'fixed_100_sample':False,'figure_numbers':[3,4]},scope['supplemental_papers'])
