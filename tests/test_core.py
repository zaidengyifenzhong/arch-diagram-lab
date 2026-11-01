import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from arch_diagram_lab.core import SpecError,render,validate
from arch_diagram_lab.cli import main

class DiagramTests(unittest.TestCase):
    def setUp(self): self.spec=json.loads((ROOT/'examples/01-overview.json').read_text())
    def bad(self,change,pattern):
        change(self.spec)
        with self.assertRaisesRegex(SpecError,pattern): validate(self.spec)
    def test_examples_and_template(self):
        for p in list((ROOT/'examples').glob('*.json'))+list((ROOT/'templates').glob('*.json')):
            s=json.loads(p.read_text()); validate(s); ET.fromstring(render(s))
    def test_duplicate_node(self): self.bad(lambda s:s['nodes'].append(copy.deepcopy(s['nodes'][0])),'duplicate node')
    def test_missing_reference(self): self.bad(lambda s:s['edges'][0].update(to='missing'),'unknown endpoint')
    def test_invalid_endpoint_type(self): self.bad(lambda s:s['edges'][0].update(to=[]),'unknown endpoint')
    def test_duplicate_edge(self): self.bad(lambda s:s['edges'].append(copy.deepcopy(s['edges'][0])),'duplicate edge')
    def test_invalid_role(self): self.bad(lambda s:s['edges'][0].update(role='magic'),'role must')
    def test_explicit_direction(self): self.bad(lambda s:s['edges'][0].update(direction='backward'),'direction must')
    def test_bad_port(self): self.bad(lambda s:s['edges'][0].update(to_side='center'),'invalid to_side')
    def test_bad_geometry(self): self.bad(lambda s:s['nodes'][0].update(x=-5),'outside diagram')
    def test_nonfinite(self): self.bad(lambda s:s['nodes'][0].update(x=float('nan')),'finite numbers')
    def test_overlap(self): self.bad(lambda s:s['nodes'][1].update(x=50),'overlapping')
    def test_text_fit(self): self.bad(lambda s:s['nodes'][0].update(label='x'*80),'label too wide')
    def test_label_position(self): self.bad(lambda s:s['edges'][0].pop('label_at'),'need label_at')
    def test_bad_waypoint(self): self.bad(lambda s:s['edges'][0].update(via=[[1,2,3]]),'invalid waypoint')
    def test_arrow_inside_target_rejected(self):
        self.bad(lambda s:s['edges'][-2].update(via=[[975,470],[575,470]]),'approach target port')
    def test_bad_panel(self): self.bad(lambda s:s.update(panels=[{}]),'invalid geometry')
    def test_monochrome_keeps_roles(self):
        import re
        svg=render(self.spec,monochrome=True)
        colors=re.findall(r'#[0-9a-f]{6}\b',svg)
        self.assertTrue(colors)
        self.assertTrue(all(c[1:3]==c[3:5]==c[5:7] for c in colors))
        self.assertIn('stroke-dasharray="7 4"',svg)
        self.assertIn('stroke-dasharray="3 4"',svg)
    def test_deterministic(self): self.assertEqual(render(self.spec),render(self.spec))
    def test_svg_accessible_and_editable(self):
        svg=render(self.spec); self.assertIn('id="node-scheduler"',svg); self.assertIn('<title',svg); self.assertIn('<text',svg)
    def test_xml_escaping(self):
        self.spec['title']='<script>& "test"'; svg=render(self.spec); ET.fromstring(svg); self.assertNotIn('<script>',svg)
    def test_edit_preserves_structure(self):
        with tempfile.TemporaryDirectory() as t:
            out=Path(t)/'edited.json'
            self.assertEqual(main(['edit',str(ROOT/'examples/01-overview.json'),'--node','scheduler','--label','Epoch arbiter','-o',str(out)]),0)
            after=json.loads(out.read_text()); self.assertEqual(after['edges'],self.spec['edges'])
            self.assertEqual(next(n for n in after['nodes'] if n['id']=='scheduler')['label'],'Epoch arbiter')
    def test_invalid_cli_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as t:
            source=Path(t)/'broken.json'; source.write_text('{}')
            self.assertEqual(main(['validate',str(source)]),2)
    def test_mutation_generated_valid(self):
        p=ROOT/'generated/04-edited-overview.json'
        if p.exists(): validate(json.loads(p.read_text()))

if __name__=='__main__': unittest.main()
