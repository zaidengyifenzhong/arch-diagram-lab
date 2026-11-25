import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fallback', ROOT / 'scripts/build_gallery_fallback.py')
fallback = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fallback)


class FallbackTests(unittest.TestCase):
    def test_generated_block_is_current(self):
        path, generated = fallback.build()
        self.assertEqual(path.read_text(), generated)
        self.assertIsNone(re.search(r'\d', fallback.NOTICE))

    def test_text_is_escaped_and_reuse_notice_retained(self):
        item = dict(id='test', paper_id='test', paper_short='<paper>', figure_title='F1',
                    figure_type='diagram', asset='assets/test.png', alt_text='a"<b',
                    reuse_notice='仅限非商业 & 相同许可', license_url='https://example.com/license',
                    license_name='CC BY-NC-SA 4.0')
        output = fallback.render([item])
        self.assertIn('&lt;paper&gt;', output)
        self.assertIn('a&quot;&lt;b', output)
        self.assertIn('仅限非商业 &amp; 相同许可', output)
        self.assertIn('papers/test.md', output)
