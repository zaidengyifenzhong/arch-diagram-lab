"""Offline corpus integrity checks. Does not verify truth or fetch source papers."""
import re
from urllib.parse import urlparse
from .core import SpecError

def validate_corpus(papers,figures):
    errors=[]
    for name,doc in [('papers',papers),('figures',figures)]:
        if not isinstance(doc,dict): errors.append(f'{name}: expected object'); continue
        if doc.get('schema_version')!='0.1.0': errors.append(f'{name}: unsupported schema_version')
        if not isinstance(doc.get('corpus_status'),str) or not doc['corpus_status']: errors.append(f'{name}: missing corpus_status')
        if not isinstance(doc.get('records'),list): errors.append(f'{name}: records must be list')
    if errors: raise SpecError('\n'.join(errors))
    def indexed(records,name):
        result={}
        for rec in records:
            if not isinstance(rec,dict) or not isinstance(rec.get('id'),str) or not rec['id']:
                errors.append(f'{name}: invalid record/id'); continue
            if rec['id'] in result: errors.append(f'{name}: duplicate id {rec["id"]}')
            result[rec['id']]=rec
        return result
    ps=indexed(papers['records'],'papers'); fs=indexed(figures['records'],'figures')
    def url(value):
        return isinstance(value,str) and urlparse(value).scheme=='https' and bool(urlparse(value).netloc)
    for ident,p in ps.items():
        for k in ('title','venue','metadata_verification','selection_reason'):
            if not isinstance(p.get(k),str) or not p[k].strip(): errors.append(f'{ident}: missing {k}')
        for k in ('official_url','pdf_url'):
            if not url(p.get(k)): errors.append(f'{ident}: invalid {k}')
        if not re.fullmatch(r'[a-f0-9]{64}',str(p.get('pdf_sha256',''))): errors.append(f'{ident}: invalid PDF hash')
        if type(p.get('pdf_page_count')) is not int or p['pdf_page_count']<1: errors.append(f'{ident}: invalid page count')
        nums=p.get('inspected_figure_numbers')
        if not isinstance(nums,list) or not all(type(v) is int and v>0 for v in nums): errors.append(f'{ident}: invalid inspected figure numbers')
    if errors: raise SpecError('\n'.join(errors))
    seen=set()
    for ident,f in fs.items():
        pid=f.get('paper_id')
        if not isinstance(pid,str) or pid not in ps: errors.append(f'{ident}: unknown paper_id'); continue
        p=ps[pid]; num=f.get('figure_number'); page=f.get('pdf_page_1based')
        if not isinstance(num,str) or not num.isdigit(): errors.append(f'{ident}: invalid figure number')
        else:
            pair=(pid,num)
            if pair in seen: errors.append(f'{ident}: duplicate paper/figure pair')
            seen.add(pair)
            if int(num) not in p.get('inspected_figure_numbers',[]): errors.append(f'{ident}: figure not in paper inspection list')
        if type(page) is not int or not 1<=page<=p.get('pdf_page_count',0): errors.append(f'{ident}: page out of range')
        if not url(f.get('source_url')): errors.append(f'{ident}: invalid source_url')
        for k in ('kind','main_object','reader_question','caption_paraphrase_zh','relevant_text','design_lesson','inspection_method'):
            if not isinstance(f.get(k),str) or not f[k].strip(): errors.append(f'{ident}: missing {k}')
        for k in ('explicit_semantic_mappings','local_style_observations','inferred_design_reading','pattern_applicability','ambiguities'):
            if not isinstance(f.get(k),list) or not all(isinstance(v,str) and v.strip() for v in f[k]): errors.append(f'{ident}: invalid {k}')
        evidence=f.get('evidence_status')
        if not isinstance(evidence,dict): errors.append(f'{ident}: missing evidence_status')
        elif evidence.get('experimental_result_chart') is not False: errors.append(f'{ident}: result charts excluded')
    if errors: raise SpecError('\n'.join(errors))
    return {'papers':len(ps),'figures':len(fs)}

def validate_expert_corpus(doc, existing_paper_ids=()):
    """Validate expert-papers.json schema 1 separately from pilot schema 0.1.0.

    Pixel-inspection booleans and hashes are recorded claims, not reverified here.
    No upper page bound is checked: this schema has no PDF page-count field.
    """
    errors=[]
    if not isinstance(doc,dict) or type(doc.get('schema_version')) is not int or doc.get('schema_version')!=1:
        raise SpecError('expert corpus: expected schema_version 1 object')
    if not isinstance(doc.get('scope_note'),str) or not doc['scope_note'].strip(): errors.append('expert corpus: missing scope_note')
    if not isinstance(doc.get('papers'),list): raise SpecError('expert corpus: papers must be a list')
    seen=set(existing_paper_ids); count=0
    for p in doc['papers']:
        if not isinstance(p,dict) or not isinstance(p.get('id'),str) or not p['id']:
            errors.append('expert corpus: invalid paper/id'); continue
        ident=p['id']
        if ident in seen: errors.append(f'{ident}: duplicate paper id across corpora')
        seen.add(ident)
        for k in ('title','venue'):
            if not isinstance(p.get(k),str) or not p[k].strip(): errors.append(f'{ident}: missing {k}')
        if type(p.get('year')) is not int: errors.append(f'{ident}: invalid year')
        for k in ('authors','affiliations_as_printed'):
            values=p.get(k)
            if not isinstance(values,list) or not values or not all(isinstance(v,str) and v.strip() for v in values): errors.append(f'{ident}: invalid {k}')
        for k in ('source_url','record_url'):
            u=p.get(k)
            if not isinstance(u,str) or urlparse(u).scheme!='https' or not urlparse(u).netloc: errors.append(f'{ident}: invalid {k}')
        if not re.fullmatch(r'[a-f0-9]{64}',str(p.get('pdf_sha256',''))): errors.append(f'{ident}: invalid PDF hash')
        inspection=p.get('inspection')
        if not isinstance(inspection,dict): errors.append(f'{ident}: missing inspection')
        else:
            for k in ('date','method','page_convention','raw_material_policy','scope'):
                if not isinstance(inspection.get(k),str) or not inspection[k].strip(): errors.append(f'{ident}: missing inspection {k}')
        figures=p.get('figures')
        if not isinstance(figures,list) or not figures: errors.append(f'{ident}: figures must be nonempty list'); continue
        nums=set()
        for f in figures:
            if not isinstance(f,dict): errors.append(f'{ident}: invalid figure'); continue
            num=f.get('number'); page=f.get('pdf_page')
            if type(num) is not int or num<1: errors.append(f'{ident}: invalid figure number')
            elif num in nums: errors.append(f'{ident}: duplicate figure number')
            else: nums.add(num)
            if type(page) is not int or page<1: errors.append(f'{ident}: invalid PDF page')
            if type(f.get('pixel_inspected')) is not bool: errors.append(f'{ident}: missing pixel_inspected boolean')
            for k in ('type','context','observation','hierarchy','not_shown','baseline_vs_novelty','encoding','revision_advice'):
                if not isinstance(f.get(k),str) or not f[k].strip(): errors.append(f'{ident}: missing figure {k}')
            if f.get('source_anchor')!=str(p.get('source_url'))+'#page='+str(page): errors.append(f'{ident}: source anchor must match PDF URL and page')
            count+=1
    if errors: raise SpecError('\n'.join(errors))
    return {'papers':len(doc['papers']),'figures':count}
