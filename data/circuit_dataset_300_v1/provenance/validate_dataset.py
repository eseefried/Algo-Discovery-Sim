"""Check artifact structure and integrity; does not validate scientific claims."""
from pathlib import Path
import bisect,collections,csv,datetime,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(condition,message):
 if not condition:raise ValueError(message)
def main():
 rows=[json.loads(l) for l in (ROOT/'manifest.jsonl').read_text().splitlines()];errors=[];warnings=[];equations=0;display=0
 check(len(rows)==300,'Expected exactly 300 manifest rows')
 check(len({r['id'] for r in rows})==300,'Duplicate paper IDs')
 check(len({re.sub(r'\W+','',r['title']).lower() for r in rows})==300,'Duplicate normalized titles')
 for r in rows:
  aid=r['arxiv_id']
  try:
   for kind,rel in r['files'].items():
    p=ROOT/rel;check(p.is_file(),f'missing {p}');check(sha(p)==r['sha256'][kind],f'{kind} checksum')
   abstract=(ROOT/r['files']['abstract']).read_text();body=(ROOT/r['files']['paper']).read_text()
   check(len(abstract.split())>=25,'abstract too short');check(len(abstract.split())<=600,'abstract too long');check(len(body)>3000,'body too short')
   check(abstract.strip() not in body,'abstract repeated in body')
   check(not re.search(r'^#{1,6}|^\||^\s*(?:PACS|Keywords|Errata:|Program summary)',abstract,re.M),'abstract contains heading/table/classification metadata')
   check(len(re.findall(r'^[ \t]*\$\$[ \t]*$',body,re.M))%2==0,'unbalanced displayed math')
   check(not re.search(r'(?<!\\)!\[[^\n]*\]\([^\n]*\)|<img\b|<figure\b|^\s*(?:Figure|Fig\.|FIG\.)\s*\d+[a-z]?\s*:',body,re.M|re.I),'image markup or figure caption remains')
   eq=[json.loads(l) for l in (ROOT/r['files']['equations']).read_text().splitlines()]
   check(len({e['id'] for e in eq})==len(eq),'duplicate equation ids');nl=[m.start() for m in re.finditer('\n',body)]
   for e in eq:
    start,end=e['paper_text_start'],e['paper_text_end'];check(0<=start<end<=len(body),'invalid math offsets');check(e['paper_id']==r['id'],'wrong math owner')
    raw=body[start:end];delimiter='$$' if e['kind']=='display' else '$';n=len(delimiter)
    check(raw.startswith(delimiter) and raw.endswith(delimiter),'math delimiters mismatch');check(raw[n:-n].strip()==e['latex'],'math content mismatch');check(e['paper_text_line']==bisect.bisect_left(nl,start)+1,'math line mismatch')
    check(e['context_before']==body[max(0,start-250):start] and e['context_after']==body[end:end+250],'math context mismatch')
   d=sum(e['kind']=='display' for e in eq);check(d>=1,'no display equations');check(d==r['counts']['display_equations'],'display count mismatch');check(len(eq)-d==r['counts']['inline_math'],'inline count mismatch');check(bool(r['screening']['algorithm_evidence']),'no algorithm/circuit evidence')
   check(not r['status']['simulation_validated'] and not r['status']['algorithm_implemented'],'unearned implementation status')
   display+=d;equations+=len(eq)
   alignment=r['screening']['abstract_alignment'].get('local_abstract_similarity')
   if alignment is not None and alignment<.8:warnings.append({'arxiv_id':aid,'issue':'metadata_abstract_differs_from_local_paper','similarity':alignment,'resolution':'export uses local-paper abstract; metadata retained for provenance'})
  except Exception as e:errors.append({'arxiv_id':aid,'error':str(e)})
 seed=ROOT.parent/'mvp_circuit_dataset_v1';seedrows=list(map(json.loads,(seed/'manifest.jsonl').read_text().splitlines()));lookup={r['id']:r for r in rows}
 for r in seedrows:
  for kind,rel in r['files'].items():check(sha(seed/rel)==sha(ROOT/lookup[r['id']]['files'][kind]),'approved seed export changed')
 book=list(map(json.loads,(ROOT/'qiskit_textbooks/index.jsonl').read_text().splitlines()))
 for b in book:check(sha(ROOT/b['output'])==b['output_sha256'],'textbook checksum')
 check(sum(b['source_type']=='ipynb' for b in book)==84,'expected 84 notebooks')
 check(len(list(csv.DictReader((ROOT/'catalog.csv').open())))==300,'catalog row count')
 for folder in ['abstracts','papers','equations']:check(len(list((ROOT/folder).iterdir()))==300,f'{folder} file count')
 check(not any(p.suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.gif','.svg','.webp','.ipynb'} for p in ROOT.rglob('*') if p.is_file()),'binary/notebook source copied')
 report={'validated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':not errors,'papers':len(rows),'math_records':equations,'display_equations':display,'inline_math':equations-display,'textbook_exports':len(book),'approved_seed_byte_identical':True,'manifest_sha256':sha(ROOT/'manifest.jsonl'),'checks':['300 unique IDs and normalized titles','300 abstracts, bodies, and equation files','manifest and textbook checksums','abstract/body separation and abstract boilerplate screening','balanced display delimiters','all equation offsets, content, line numbers, contexts, and counts','no paper image markup or figure-caption prefixes','algorithm/circuit evidence present','approved seed byte preservation','no binary image/PDF/notebook source exports','300 catalog rows'],'errors':errors,'warnings':warnings,'not_validated':['mathematical transcription accuracy against PDFs','whether every extracted expression is valid compilable LaTeX','paper-specific algorithm completeness','whether proposed reductions fit the qubit cap','runtime or scientific reproduction results','current Qiskit compatibility of archival textbook code']}
 (ROOT/'provenance/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':not errors,'errors':errors,'warnings':len(warnings),'papers':len(rows),'math_records':equations},indent=2));check(not errors,'Dataset validation failed; see validation.json')
if __name__=='__main__':main()
