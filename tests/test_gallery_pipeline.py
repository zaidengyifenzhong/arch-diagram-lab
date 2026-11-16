import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image

spec = importlib.util.spec_from_file_location('pipeline', Path(__file__).resolve().parents[1] / 'scripts/gallery_pipeline.py')
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.base = Path(self.tmp.name)
        self.root = self.base / 'source'; (self.root / 'assets').mkdir(parents=True)
        Image.new('RGB', (8, 6), 'white').save(self.root / 'assets/a.png')
        self.figure = dict(id='p-F1', paper_id='p', paper_title='Example', asset='assets/a.png', figure_type='Mechanism', category='非实验图', attribution='Example Authors, Example, CC BY 4.0.', modifications='Cropped and rasterized.', source_url='https://example.org/paper-v1.pdf', source_page_url='https://example.org/paper-v1.pdf#page=2', license_name='CC BY 4.0', license_url=p.LICENSES['CC BY 4.0'], alt_text='Mechanism figure', figure_number=1, pdf_page=2, width=8, height=6)
        self.data = {'items': [self.figure]}
        self.approval = dict(id='p-F1', asset='assets/a.png', decision='approved', public_redistribution=True, third_party_clearance=True, nonexperimental_clearance=True, source_page_url=self.figure['source_page_url'], license_name=self.figure['license_name'], license_url=self.figure['license_url'], source_sha256='a' * 64, sha256=p.png_info(self.root / 'assets/a.png')['sha256'], license_evidence_url='https://example.org/paper-v1-rights', review_note='Exact v1 figure reviewed; no separately credited third-party content.')
        self.approvals = {'items': [self.approval]}
    def tearDown(self): self.tmp.cleanup()
    def test_validate(self): self.assertEqual(len(p.validate(self.data, self.root, self.approvals)), 1)
    def test_export_preserves_bytes(self):
        target = self.base / 'out'; p.export(self.data, self.root, self.approvals, target)
        self.assertEqual((target / 'assets/a.png').read_bytes(), (self.root / 'assets/a.png').read_bytes())
    def test_unknown_approval(self):
        self.approval['id'] = 'unknown'
        with self.assertRaises(ValueError): p.validate(self.data, self.root, self.approvals)
    def test_approval_digest(self):
        self.approval['sha256'] = '0' * 64
        with self.assertRaises(ValueError): p.validate(self.data, self.root, self.approvals)
    def test_approval_source_binding(self):
        self.approval['source_page_url'] = 'https://example.org/other#page=2'
        with self.assertRaises(ValueError): p.validate(self.data, self.root, self.approvals)
    def test_third_party_gate(self):
        self.approval['third_party_clearance'] = False
        with self.assertRaises(ValueError): p.validate(self.data, self.root, self.approvals)
    def test_decision_gate(self):
        self.approval['decision'] = 'hold'
        with self.assertRaises(ValueError): p.validate(self.data, self.root, self.approvals)
    def test_public_gate(self):
        self.approval['public_redistribution'] = False
        with self.assertRaises(ValueError): p.validate(self.data, self.root, self.approvals)
    def test_license_gate(self):
        self.figure['license_name'] = self.approval['license_name'] = 'unknown'
        with self.assertRaises(ValueError): p.validate(self.data, self.root, self.approvals)
    def test_source_hash_gate(self):
        self.approval['source_sha256'] = ''
        with self.assertRaises(ValueError): p.validate(self.data, self.root, self.approvals)
    def test_duplicate_id(self):
        self.data['items'].append(copy.deepcopy(self.figure))
        with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_dimension_mismatch(self):
        self.figure['width'] = 9
        with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_page_mismatch(self):
        self.figure['pdf_page'] = 3
        with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_required_attribution(self):
        self.figure['attribution'] = ''
        with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_paths(self):
        for path in ('../a.png', '/tmp/a.png', 'assets/../a.png', 'assets//a.png', 'assets/./a.png', 'assets\\a.png', 'assets/%2e%2e/a.png', 'assets/a.png\x00'):
            with self.subTest(path=path), self.assertRaises(ValueError): p.asset_path(self.root, path)
    def test_symlink_file(self):
        (self.root / 'assets/link.png').symlink_to(self.root / 'assets/a.png')
        with self.assertRaises(ValueError): p.asset_path(self.root, 'assets/link.png')
    def test_symlink_directory(self):
        (self.root / 'assets/link').symlink_to(self.root / 'assets', target_is_directory=True)
        with self.assertRaises(ValueError): p.asset_path(self.root, 'assets/link/a.png')
    def test_existing_destination(self):
        with self.assertRaises(ValueError): p.export(self.data, self.root, self.approvals, self.root)
    def test_nested_destination(self):
        with self.assertRaises(ValueError): p.export(self.data, self.root, self.approvals, self.root / 'out')
    def test_empty_export(self):
        with self.assertRaises(ValueError): p.export(self.data, self.root, {'items': []}, self.base / 'out')
    def test_corrupt_png(self):
        (self.root / 'assets/a.png').write_bytes(b'not PNG')
        with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_no_partial_export_on_validation_failure(self):
        self.approval['sha256'] = 'bad'; target = self.base / 'out'
        with self.assertRaises(ValueError): p.export(self.data, self.root, self.approvals, target)
        self.assertFalse(target.exists())
    def test_guide_pruning(self):
        self.data['reading_guides'] = [{'paper_id': 'p', 'source_examples': [{'figure_id': 'F1'}, {'figure_id': 'F2'}]}]
        target = self.base / 'out'; p.export(self.data, self.root, self.approvals, target)
        saved = json.loads((target / 'figures.json').read_text())
        self.assertEqual(saved['reading_guides'][0]['source_examples'], [{'figure_id': 'F1'}])
    def test_nonpublic_fields_not_exported(self):
        self.data['private_note'] = 'secret'
        self.figure['reviewer_email'] = 'secret'
        target = self.base / 'out'; p.export(self.data, self.root, self.approvals, target)
        self.assertNotIn('secret', (target / 'figures.json').read_text())
    def test_nested_optional_public_figure_fields_rejected(self):
        for key in ('source_note', 'paper_notice', 'paper_short', 'figure_title'):
            with self.subTest(key=key):
                self.figure[key] = {'reviewer_email': 'PRIVATE_SENTINEL'}
                target = self.base / 'out'
                with self.assertRaises(ValueError): p.export(self.data, self.root, self.approvals, target)
                self.assertFalse(target.exists())
                del self.figure[key]
    def test_nested_envelope_fields_rejected(self):
        for key in ('title', 'coverage_note'):
            with self.subTest(key=key):
                self.data[key] = {'private_internal_note': 'PRIVATE_SENTINEL'}
                with self.assertRaises(ValueError): p.validate(self.data, self.root)
                del self.data[key]
    def test_nested_object_fields_rejected(self):
        for key in ('paper_id', 'object_group', 'specific_object'):
            with self.subTest(key=key):
                obj = {'paper_id': 'p', key: {'reviewer_email': 'PRIVATE_SENTINEL'}}
                self.data['paper_objects'] = [obj]
                with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_nested_guide_fields_rejected(self):
        for key in ('paper_id', 'primary_object', 'specific_object', 'conditional_design_advice', 'this_paper_figure_sequence', 'source_ambiguity_or_scope'):
            with self.subTest(key=key):
                self.data['reading_guides'] = [{'paper_id': 'p', key: {'reviewer_email': 'PRIVATE_SENTINEL'}}]
                with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_example_types_rejected(self):
        for field, value in [('figure_id', {}), ('url', {}), ('pdf_pages', {}), ('pdf_pages', [True]), ('pdf_pages', [0]), ('pdf_pages', ['2']), ('pdf_pages', [{'reviewer_email': 'PRIVATE_SENTINEL'}])]:
            with self.subTest(field=field, value=value):
                self.data['reading_guides'] = [{'paper_id': 'p', 'source_examples': [{'figure_id': 'F1', field: value}]}]
                with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_public_list_types_rejected(self):
        for field in ('reading_guides', 'paper_objects'):
            with self.subTest(field=field):
                self.data[field] = {'private_internal_note': 'PRIVATE_SENTINEL'}
                with self.assertRaises(ValueError): p.validate(self.data, self.root)
                del self.data[field]
        self.data['reading_guides'] = [{'paper_id': 'p', 'source_examples': {}}]
        with self.assertRaises(ValueError): p.validate(self.data, self.root)
    def test_subset_drops_inherited_coverage(self):
        self.data['coverage_note'] = '390 figures, 32 papers'
        target = self.base / 'out'; p.export(self.data, self.root, self.approvals, target)
        saved = json.loads((target / 'figures.json').read_text())
        self.assertNotIn('coverage_note', saved)
        self.assertNotIn('390 figures', (target / 'figures.json').read_text())
    def test_extract_digest_before_render(self):
        source = self.base / 'fake.pdf'; source.write_bytes(b'not PDF')
        with self.assertRaises(ValueError): p.extract_candidate(source, '0' * 64, 1, [0, 0, 5, 5], 240, self.base / 'candidate.png', 'https://example.org/v1.pdf', 'Lawfully held local copy')

if __name__ == '__main__': unittest.main()

class NonexperimentalGates(unittest.TestCase):
    setUp = PipelineTests.setUp
    tearDown = PipelineTests.tearDown
    def test_results_rejected(self):
        self.figure['category'] = '实验／实证图'
        with self.assertRaises(ValueError): p.export(self.data,self.root,self.approvals,self.base/'out')
        self.assertFalse((self.base/'out').exists())
    def test_mixed_rejected(self):
        self.figure['category'] = '混合图'
        with self.assertRaises(ValueError): p.validate(self.data,self.root)
    def test_scope_clearance_required(self):
        self.approval.pop('nonexperimental_clearance')
        with self.assertRaises(ValueError): p.export(self.data,self.root,self.approvals,self.base/'out')
        self.assertFalse((self.base/'out').exists())

class NoncommercialShareAlikeTests(unittest.TestCase):
    setUp = PipelineTests.setUp
    tearDown = PipelineTests.tearDown
    def nc(self):
        self.figure.update(license_name=p.NC_SA, license_url=p.LICENSES[p.NC_SA], reuse_notice=p.NC_NOTICE, adaptation_license_url=p.LICENSES[p.NC_SA])
        self.approval.update(license_name=p.NC_SA, license_url=p.LICENSES[p.NC_SA], noncommercial_use=True, sharealike_compliance=True, source_version_license_verified=True, adaptation_license_url=p.LICENSES[p.NC_SA])
    def test_nc_export_retains_notice(self):
        self.nc();target=self.base/'nc';p.export(self.data,self.root,self.approvals,target)
        out=json.loads((target/'figures.json').read_text())['items'][0]
        self.assertEqual(out['reuse_notice'],p.NC_NOTICE)
        self.assertEqual(out['adaptation_license_url'],p.LICENSES[p.NC_SA])
    def test_nc_each_approval_gate(self):
        for key in ['noncommercial_use','sharealike_compliance','source_version_license_verified']:
            for value in [None,False,'true']:
                with self.subTest(key=key,value=value):
                    self.nc();self.approval[key]=value
                    with self.assertRaises(ValueError):p.validate(self.data,self.root,self.approvals)
    def test_nc_public_notice_required(self):
        self.nc();self.figure.pop('reuse_notice')
        with self.assertRaises(ValueError):p.validate(self.data,self.root,self.approvals)
    def test_nc_no_weaker_adaptation_license(self):
        for record in [self.figure,self.approval]:
            self.nc();record['adaptation_license_url']=p.LICENSES['CC BY 4.0']
            with self.assertRaises(ValueError):p.validate(self.data,self.root,self.approvals)
    def test_nc_source_evidence_required(self):
        self.nc();self.approval['license_evidence_url']=''
        with self.assertRaises(ValueError):p.validate(self.data,self.root,self.approvals)
