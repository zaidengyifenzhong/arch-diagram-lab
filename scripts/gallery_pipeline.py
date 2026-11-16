#!/usr/bin/env python3
"""Local-only figure validation and explicitly approved export. No network calls."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

NC_SA = 'CC BY-NC-SA 4.0'
NC_NOTICE = '仅限非商业使用；改编作品须以 CC BY-NC-SA 4.0 相同许可共享。'
LICENSES = {
    NC_SA: 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/',
    'CC BY 2.5': 'https://creativecommons.org/licenses/by/2.5/',
    'CC0': 'https://creativecommons.org/publicdomain/zero/1.0/',
}
REQUIRED = ('id', 'paper_id', 'paper_title', 'asset', 'figure_type', 'category',
            'attribution', 'modifications', 'source_url', 'source_page_url',
            'license_name', 'license_url', 'alt_text')


def fail(message):
    raise ValueError(message)


def https_url(value):
    if not isinstance(value, str):
        return False
    p = urlsplit(value)
    return p.scheme == 'https' and bool(p.hostname) and not p.username and not p.password


def asset_path(root, name):
    """Only literal, rooted, nonsymlink POSIX asset paths are accepted."""
    if not isinstance(name, str) or not name or '\\' in name or '%' in name or '\x00' in name:
        fail('invalid asset path')
    parts = name.split('/')
    if any(p in ('', '.', '..') for p in parts) or PurePosixPath(name).is_absolute():
        fail('asset path traversal or noncanonical path')
    if parts[0] != 'assets' or not name.endswith('.png'):
        fail('asset must be a PNG below assets/')
    root = Path(root).resolve(strict=True)
    p = root
    for part in parts:
        p = p / part
        if p.is_symlink():
            fail('symlinks are not permitted in asset paths')
    resolved = p.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        fail('asset escapes root or is not a file')
    return resolved


def png_info(path):
    from PIL import Image
    data = Path(path).read_bytes()
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        fail('not a PNG')
    with Image.open(path) as im:
        if im.format != 'PNG':
            fail('not a PNG')
        im.verify()
    with Image.open(path) as im:
        im.load()
        width, height = im.size
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
            'width': width, 'height': height}



def validate_public_text(data):
    """Public fields are scalar text, never arbitrary nested research records."""
    def strings(record, keys):
        if not isinstance(record, dict):
            fail('public metadata record must be an object')
        for key in keys:
            if key in record and not isinstance(record[key], str):
                fail('public text must be a string: ' + key)

    strings(data, ('title', 'coverage_note'))
    for field in ('paper_objects', 'reading_guides'):
        if field in data and not isinstance(data[field], list):
            fail(field + ' must be an array')
    for obj in data.get('paper_objects', []):
        strings(obj, ('paper_id', 'object_group', 'specific_object'))
        if not obj.get('paper_id'):
            fail('paper object identity required')
    for guide in data.get('reading_guides', []):
        strings(guide, ('paper_id', 'primary_object', 'specific_object',
                       'conditional_design_advice', 'this_paper_figure_sequence',
                       'source_ambiguity_or_scope'))
        if not guide.get('paper_id'):
            fail('guide paper identity required')
        examples = guide.get('source_examples', [])
        if not isinstance(examples, list):
            fail('source_examples must be an array')
        for example in examples:
            strings(example, ('figure_id', 'url'))
            if not re.fullmatch(r'F[1-9][0-9]*', example.get('figure_id', '')):
                fail('invalid guide figure identity')
            if 'url' in example and not https_url(example['url']):
                fail('guide example URL must be HTTPS')
            if 'pdf_pages' in example:
                pages = example['pdf_pages']
                if not isinstance(pages, list) or not pages or any(type(n) is not int or n < 1 for n in pages):
                    fail('guide PDF pages must be a nonempty positive integer array')
    for figure in data['items']:
        strings(figure, ('paper_short', 'paper_notice', 'source_note', 'figure_title', 'reuse_notice', 'adaptation_license_url'))


def validate(data, root, approvals=None):
    if not isinstance(data, dict) or not isinstance(data.get('items'), list):
        fail('metadata must contain items array')
    validate_public_text(data)
    seen, assets, pairs, results = set(), set(), set(), []
    allowed = None
    if approvals is not None:
        if not isinstance(approvals, dict) or not isinstance(approvals.get('items'), list):
            fail('approvals must contain items array')
        allowed = {}
        for a in approvals['items']:
            if not isinstance(a, dict) or a.get('id') in allowed or not a.get('id'):
                fail('invalid or duplicate approval id')
            allowed[a['id']] = a
    for f in data['items']:
        if not isinstance(f, dict) or any(not isinstance(f.get(k), str) or not f[k].strip() for k in REQUIRED):
            fail('required figure metadata missing')
        if f['id'] in seen or f['asset'] in assets:
            fail('duplicate figure id or asset')
        seen.add(f['id']); assets.add(f['asset'])
        for k in ('figure_number', 'pdf_page', 'width', 'height'):
            if type(f.get(k)) is not int or f[k] < 1:
                fail('invalid positive integer: ' + k)
        pair = (f['paper_id'], f['figure_number'])
        if pair in pairs:
            fail('duplicate paper/figure number')
        pairs.add(pair)
        if f['category'] != '非实验图':
            fail('only nonexperimental figures are in project scope')
        for k in ('source_url', 'source_page_url', 'license_url'):
            if not https_url(f[k]):
                fail('invalid HTTPS URL: ' + k)
        if urlsplit(f['source_page_url']).fragment != 'page=' + str(f['pdf_page']):
            fail('source page URL does not match physical PDF page')
        if f['license_name'] == NC_SA:
            if f['license_url'] != LICENSES[NC_SA] or f.get('reuse_notice') != NC_NOTICE:
                fail('NC-SA license URL and explicit public reuse notice required')
            if f.get('adaptation_license_url') != LICENSES[NC_SA]:
                fail('NC-SA same-license adaptation statement required')
        info = png_info(asset_path(root, f['asset']))
        if (info['width'], info['height']) != (f['width'], f['height']):
            fail('PNG dimensions do not match metadata')
        if allowed is not None and f['id'] in allowed:
            a = allowed[f['id']]
            if a.get('decision') != 'approved' or a.get('public_redistribution') is not True:
                fail('approval does not permit public redistribution')
            if a.get('nonexperimental_clearance') is not True:
                fail('independent nonexperimental scope clearance required')
            if a.get('third_party_clearance') is not True:
                fail('third-party content has not been cleared')
            for k in ('asset', 'source_page_url', 'license_name', 'license_url'):
                if a.get(k) != f[k]:
                    fail('approval/metadata binding mismatch: ' + k)
            if a.get('sha256') != info['sha256']:
                fail('approved image digest mismatch')
            if not re.fullmatch(r'[0-9a-f]{64}', a.get('source_sha256', '')):
                fail('exact source PDF digest required')
            if not https_url(a.get('license_evidence_url', '')):
                fail('version-specific license evidence URL required')
            if not isinstance(a.get('review_note'), str) or not a['review_note'].strip():
                fail('review note required')
            if f['license_name'] == NC_SA:
                if a.get('noncommercial_use') is not True or a.get('sharealike_compliance') is not True:
                    fail('explicit noncommercial use and share-alike approval required')
                if a.get('adaptation_license_url') != LICENSES[NC_SA]:
                    fail('NC-SA approval must bind same-license adaptations')
                if a.get('source_version_license_verified') is not True:
                    fail('exact source version NC-SA license verification required')
            if LICENSES.get(f['license_name']) != f['license_url']:
                fail('license is not in this conservative export policy')
        results.append({'id': f['id'], 'asset': f['asset'], **info})
    if allowed is not None and set(allowed) - seen:
        fail('approval references unknown figure')
    return results


def export(data, root, approvals, destination):
    """Validate everything first. Export only exact approved bytes into a new dir."""
    results = validate(data, root, approvals)
    ids = {a['id'] for a in approvals['items']}
    if not ids:
        fail('empty approval list')
    target = Path(destination)
    if target.exists() or target.is_symlink():
        fail('export destination must not already exist')
    if target.resolve().is_relative_to(Path(root).resolve()):
        fail('export destination must be outside the source root')
    public_fields = set(REQUIRED) | {'figure_number', 'pdf_page', 'width', 'height',
                                     'paper_short', 'paper_notice', 'source_note', 'figure_title',
                                     'reuse_notice', 'adaptation_license_url'}
    selected = [{k: v for k, v in f.items() if k in public_fields}
                for f in data['items'] if f['id'] in ids]
    papers = {f['paper_id'] for f in selected}
    # Original coverage prose may describe a larger set; never inherit it.
    out = {k: data[k] for k in ('title',) if k in data}
    out['items'] = selected
    out['paper_objects'] = [{k: p[k] for k in ('paper_id', 'object_group', 'specific_object') if k in p}
                            for p in data.get('paper_objects', []) if p['paper_id'] in papers]
    out['reading_guides'] = []
    available = {(f['paper_id'], 'F' + str(f['figure_number'])) for f in selected}
    for guide in data.get('reading_guides', []):
        if guide['paper_id'] in papers:
            g = {k: guide[k] for k in ('paper_id', 'primary_object', 'specific_object',
                 'conditional_design_advice', 'this_paper_figure_sequence',
                 'source_ambiguity_or_scope') if k in guide}
            g['source_examples'] = [{k: e[k] for k in ('figure_id', 'pdf_pages', 'url') if k in e}
                                    for e in guide.get('source_examples', [])
                                    if (g['paper_id'], e['figure_id']) in available]
            out['reading_guides'].append(g)
    target.mkdir(parents=True)
    for f in selected:
        dest = target / f['asset']
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(asset_path(root, f['asset']), dest)
    (target / 'figures.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    manifest = [r for r in results if r['id'] in ids]
    (target / 'asset-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


def extract_candidate(source, expected_sha, page, rect, dpi, destination, source_url, rights_note):
    """Optional PyMuPDF operation; produces a local unapproved candidate only."""
    if not https_url(source_url) or not rights_note.strip():
        fail('source URL and lawful-access rights note required')
    if not re.fullmatch(r'[0-9a-f]{64}', expected_sha):
        fail('expected source SHA256 required')
    source = Path(source)
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected_sha:
        fail('source digest mismatch')
    if type(page) is not int or page < 1 or not (72 <= dpi <= 600):
        fail('invalid page or DPI')
    dest = Path(destination)
    if dest.exists() or dest.is_symlink() or dest.suffix != '.png' or dest.with_suffix('.candidate.json').exists():
        fail('candidate output must be a new PNG path')
    import fitz
    with fitz.open(source) as doc:
        if page > len(doc):
            fail('page exceeds PDF length')
        p = doc[page - 1]; clip = fitz.Rect(rect)
        if clip.is_empty or clip.is_infinite or not p.rect.contains(clip):
            fail('crop must be nonempty and inside the physical PDF page')
        pix = p.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), clip=clip, colorspace=fitz.csRGB, alpha=False, annots=True)
        dest.parent.mkdir(parents=True, exist_ok=True)
        pix.save(str(dest))
    record = {'decision': 'unreviewed', 'public_redistribution': False,
              'source_url': source_url, 'source_sha256': expected_sha, 'pdf_page': page,
              'rect_pdf_points': list(rect), 'dpi': dpi, 'rights_note': rights_note,
              **png_info(dest)}
    dest.with_suffix('.candidate.json').write_text(json.dumps(record, indent=2) + '\n')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('validate', 'export'):
        p = sub.add_parser(name)
        p.add_argument('--metadata', required=True); p.add_argument('--asset-root', required=True)
        p.add_argument('--approvals', required=name == 'export')
        if name == 'export': p.add_argument('--output', required=True)
    p = sub.add_parser('extract')
    p.add_argument('--pdf', required=True); p.add_argument('--sha256', required=True)
    p.add_argument('--page', type=int, required=True); p.add_argument('--rect', type=float, nargs=4, required=True)
    p.add_argument('--dpi', type=int, default=240); p.add_argument('--output', required=True)
    p.add_argument('--source-url', required=True); p.add_argument('--rights-note', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'extract':
            result = extract_candidate(args.pdf, args.sha256, args.page, args.rect, args.dpi, args.output, args.source_url, args.rights_note)
        else:
            data = json.loads(Path(args.metadata).read_text(encoding='utf-8'))
            approvals = json.loads(Path(args.approvals).read_text(encoding='utf-8')) if args.approvals else None
            result = export(data, args.asset_root, approvals, args.output) if args.command == 'export' else validate(data, args.asset_root, approvals)
        print(json.dumps({'result': result, 'scope': 'local checks; not a legal opinion or scientific replication'}, ensure_ascii=False))
    except (ValueError, OSError, KeyError, ImportError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
