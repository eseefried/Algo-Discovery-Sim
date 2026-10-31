"""Rebuild text artifacts from a frozen local-source selection; runs no models."""
from pathlib import Path
import collections,csv,datetime,hashlib,html,json,re,shutil,sys,bisect
sys.path.insert(0,str(Path(__file__).resolve().parent))
from extraction import split_paper
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT.parent/'mvp_circuit_dataset_v1'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def jsonl(p,rows):p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
def jsonfile(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def clean(text):
 text=re.sub(r'<figure\b[^>]*>.*?</figure>','',text,flags=re.I|re.S)
 text=re.sub(r'!\[[^\]]*\]\([^\n]*?\)','',text)
 text=re.sub(r'<img\b[^>]*>','',text,flags=re.I)
 text=re.sub(r'(?mi)^[ \t]*(?:Figure|Fig\.|FIG\.)[ \t]*\d+[a-z]?[ \t]*[:.][^\n]*(?:\n(?![ \t]*\n)[^\n]+)*','',text)
 text=re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)',r'\1',text)
 return re.sub(r'\n{3,}','\n\n',html.unescape(text)).strip()+'\n'

def normalize_adjacent_math(text):
 # Separate adjacent inline expressions ($a$$b$) without changing their content.
 # Protect genuine display blocks and fenced code before scanning the remainder.
 protected=re.compile(r"(?ms)^[ \t]*\$\$[ \t]*\n.*?^[ \t]*\$\$[ \t]*$|^```[^\n]*\n.*?^```[^\n]*$")
 def separate(part):
  result=[];i=0;inline=False
  while i<len(part):
   if part[i]=='$' and (i==0 or part[i-1]!='\\'):
    if part[i:i+2]=='$$':
     if inline:result.append('$ $');i+=2;continue
     end=part.find('$$',i+2)
     if end>=0 and '\n' not in part[i:end]:result.append(part[i:end+2]);i=end+2;continue
    inline=not inline
   result.append(part[i]);i+=1
  return ''.join(result)
 pieces=[];cursor=0
 for m in protected.finditer(text):pieces.extend([separate(text[cursor:m.start()]),m.group()]);cursor=m.end()
 pieces.append(separate(text[cursor:]));return ''.join(pieces)

FAMILIES=[
 ('qaoa',r'approximate optimization|qaoa', 'Use p=1 or p=2 on a fixed 3–8 variable instance; enumerate the objective on every bitstring and compare the circuit expectation with direct matrix evolution.'),
 ('variational_learning',r'variational|neural|learning|perceptron|classif|born machine|fisher information|warm start|quantum geometry|QVECTOR', 'Use a shallow 2–6 qubit instance of the stated ansatz and objective; record initialization and optimizer, and compare measured costs/gradients with exact statevector values.'),
 ('search_amplification',r'grover|quantum search|search algorithm|amplitude amplification|search via|unstructured search', 'Use an explicit 2–4 input-qubit marked set and the paper-specific iterate or phase schedule; compare marked-state probability with exact evolution and a conventional Grover baseline.'),
 ('quantum_walk_search',r'quantum.*walk.*search|search.*quantum.*walk|spatial search|marked vert|backtracking', 'Choose a small graph/tree from the stated family and an explicit marked set; implement the actual walk/query construction and compare success probability against a direct walk-operator reference.'),
 ('fourier_arithmetic',r'fourier|arithmeti|adder|multiplier|numerical analysis', 'Start with 1–3 bit inputs or a small Fourier register; implement the stated gate decomposition and compare outputs against a classical arithmetic or discrete-Fourier reference.'),
 ('phase_spectral_estimation',r'phase.estimat|eigenvalue|eigenstate|spectral estimation', 'Use a one- or two-system-qubit unitary/Hamiltonian with known spectrum and a short estimation schedule; compare inferred phases/eigenvalues or output fidelity with exact diagonalization.'),
 ('linear_algebra',r'linear system|systems of linear|singular value|toeplitz|hankel|finite element|non.unitary|dense.*operator|IsoRank', 'Choose a 2x2 or 4x4 instance satisfying the stated promises; explicitly implement any required encoding and postselection and compare the normalized result with a classical matrix calculation.'),
 ('state_preparation_channels',r'prepar|initializ|channel|isometr|bell.like|graph states|w.state|state.transfer|state.engineer|qubit.state.transfer|open quantum systems|quantum measurements', 'Select a 2–4 system-qubit example of the actual construction; compare prepared-state fidelity or the reduced output density matrix with an independent state/Kraus-map reference.'),
 ('hamiltonian_simulation',r'hamiltonian simulation|quantum simulat|digital.*simulat|trotter|quantum evolution|pairing hamiltonian|fermionic|ground states|simulat.*fermi.hubbard|quantum chemistry simul|dirac equation|Gibbs sampling', 'Use a 2–6 qubit Hamiltonian or a bounded finite discretization; implement the paper-specific simulation/preparation procedure and compare against matrix-exponential or diagonalization results at fixed parameters.'),
 ('quantum_walk_construction',r'quantum walk|quantum routing|coinless|staggered|szegedy', 'Use a finite cycle/graph or a bounded position register appropriate to the paper; synthesize its coin/shift or evolution construction, document boundaries/encoding, and compare with direct operator evolution. An infinite-line reduction is a new bounded instance, not an exact reproduction of asymptotic claims.'),
 ('boolean_oracles_constraints',r'boolean|oracle|nand|formula|polynomial|triangle|viterbi|bisection|satisf|2.sat|ec3|shortest path|group testing|junta|permutation|bernstein|deutsch|shor|factoring|association rules|monotonicity|bipartiteness|connectivity|cycles and testing|simon', 'Choose a fully specified tiny promised input; synthesize the stated oracle and all work registers, then compare the decision/output distribution with exhaustive classical evaluation. Include oracle synthesis in the resource count.'),
 ('circuit_synthesis_compilation',r'circuit|gate|unitar|compil|synthes|decompos|reversible', 'Apply the stated construction to a 1–3 qubit target unitary/circuit; verify unitary equivalence up to global phase and report gate count, ancillas, and any probabilistic success rate.'),
 ('classical_circuit_simulation',r'Pauli Propagation|classical simulation|classical.*simulation|quantum.enhanced classical simulation','Use a fixed 2–6 qubit circuit and observable; implement the actual surrogate or propagation algorithm and compare with an exact statevector/density-matrix reference.'),
 ('quantum_algorithm_other',r'.*','Choose the smallest fully specified valid instance in the paper; implement its stated circuit procedure and define an independent exact reference before claiming reproduction.'),
]

def family_for(title):
 for name,pattern,target in FAMILIES:
  if re.search(pattern,title,re.I):return name,target

def route_for(title,body,family):
 flags=[]
 if re.search(r'qudit|qutrit|ternary|multivalued|higher.dimensional',title,re.I):flags.append('qudit_to_qubit_encoding')
 if family=='boolean_oracles_constraints' or re.search(r'black.box|oracle access|query access',body[:16000],re.I):flags.append('explicit_oracle_and_work_registers')
 if family=='quantum_walk_construction':flags.append('finite_graph_and_gate_mapping')
 if re.search(r'non.unitary|non.hermitian|PT.symmetric',title,re.I):flags.append('physical_channel_or_postselection_dilation')
 if re.search(r'repeat.until|fallback|adaptive|measurement|channel|error correction|error detection',title,re.I):flags.append('measurement_feedforward_or_noise_model')
 if re.search(r'analog|bos[eon]|infinite|continuous',title,re.I):flags.append('finite_encoding_or_gate_level_reduction')
 return ('requires_encoding_or_protocol_design' if flags else 'direct_circuit_or_algorithm_candidate'),flags

def main():
 selected=json.loads((ROOT/'provenance/selection.json').read_text())
 seeds={r['arxiv_id']:r for r in map(json.loads,(SEED/'manifest.jsonl').read_text().splitlines())}
 selected.sort(key=lambda x:(0,seeds[x['id']]['suggested_order']) if x['id'] in seeds else (1,x['id']))
 for folder in ['abstracts','papers','equations','qiskit_textbooks','provenance']:(ROOT/folder).mkdir(exist_ok=True)
 rows=[];screen=[]
 math=re.compile(r'\$\$(.*?)\$\$|(?<![\\$])\$(?!\$)((?:\\.|[^$])+?)(?<!\\)\$(?!\$)',re.S)
 for order,x in enumerate(selected,1):
  aid=x['id'];key='arxiv-'+aid;src=Path(x['source']);text=src.read_text()
  if aid in seeds:
   row=json.loads(json.dumps(seeds[aid]));row['seed_manifest_sha256']=sha(SEED/'manifest.jsonl')
   for path in row['files'].values():shutil.copy2(SEED/path,ROOT/path)
   abstract=(ROOT/row['files']['abstract']).read_text();body=(ROOT/row['files']['paper']).read_text()
   split={'abstract_origin':'approved_seed_export','abstract_version_match':'preserved_approved_seed','body_split_method':row['provenance']['abstract_split_method']}
   family=row['family'];tier='approved_seed';flags=[]
  else:
   abstract,body,split=split_paper(text,x.get('metadata'));abstract=clean(abstract);body=normalize_adjacent_math(clean(body))
   if abstract.strip() in body:raise ValueError(f'{aid}: abstract duplicated in body')
   headings=list(re.finditer(r'^#{1,6}\s+(.+)$',body,re.M));headpos=[m.start() for m in headings]
   newlines=[m.start() for m in re.finditer('\n',body)];equations=[]
   code_spans=[(m.start(),m.end()) for m in re.finditer(r'(?ms)^```[^\n]*\n.*?^```[^\n]*$',body)]
   for n,m in enumerate(math.finditer(body),1):
    if any(a<=m.start()<b for a,b in code_spans):continue
    display=m.group(1) is not None;latex=(m.group(1) if display else m.group(2)).strip();section=bisect.bisect_right(headpos,m.start())-1;tag=re.search(r'\\tag\{([^}]+)\}',latex)
    equations.append({'id':f'{key}:math:{n:04d}','paper_id':key,'kind':'display' if display else 'inline','latex':latex,'equation_number':tag.group(1) if tag else None,'section':headings[section].group(1) if section>=0 else None,'paper_text_start':m.start(),'paper_text_end':m.end(),'paper_text_line':bisect.bisect_left(newlines,m.start())+1,'context_before':body[max(0,m.start()-250):m.start()],'context_after':body[m.end():m.end()+250],'extraction':'verbatim_math_delimiters_from_local_conversion','review_status':'not_manually_verified_against_pdf'})
   assert any(e['kind']=='display' for e in equations),aid
   ap=ROOT/'abstracts'/f'{key}.txt';bp=ROOT/'papers'/f'{key}.txt';ep=ROOT/'equations'/f'{key}.jsonl'
   ap.write_text(abstract);bp.write_text(body);jsonl(ep,equations)
   family,target=family_for(x['title']);tier,flags=route_for(x['title'],body,family)
   itemdir=src.parent.parent;pdfs=list((itemdir/'raw').glob('*.pdf'));pdf=pdfs[0] if len(pdfs)==1 else None
   metadata=x.get('metadata') or {}
   row={'id':key,'arxiv_id':aid,'title':x['title'],'source_url':f'https://arxiv.org/abs/{aid}','family':family,'suggested_order':order,'selection_reason':'Title/abstract and local-text screening for an algorithm, constructive circuit procedure, or explicitly defined quantum-walk step; usable local mathematical text. Feasibility is a hypothesis pending implementation.','proposed_simulation':{'target':target,'paper_specific_instruction':f'Use the actual construction in "{x["title"]}"; the family target is a starting template, not an extracted claim.','total_qubit_budget':None,'target_total_qubit_cap':12,'budget_status':'design_cap_not_estimated_or_verified_resource_requirement','scope':'Small correctness instance only; paper-scale experiments and speedup claims excluded. Count ancillas, oracle registers, and qudit encoding. If the method cannot fit the cap, defer it; do not silently replace it with a different algorithm.','backend':'local Qiskit statevector or density-matrix simulation; CPU execution budget to be measured'},'files':{'abstract':str(ap.relative_to(ROOT)),'paper':str(bp.relative_to(ROOT)),'equations':str(ep.relative_to(ROOT))},'counts':{'abstract_words':len(abstract.split()),'paper_words':len(body.split()),'display_equations':sum(e['kind']=='display' for e in equations),'inline_math':sum(e['kind']=='inline' for e in equations)},'sha256':{'abstract':sha(ap),'paper':sha(bp),'equations':sha(ep)},'provenance':{'source_markdown':str(src),'source_markdown_sha256':sha(src),'source_pdf':str(pdf) if pdf else None,'source_pdf_sha256':sha(pdf) if pdf else None,'source_collection':x['source_collection'],'abstract_metadata_file':metadata.get('metadata_file'),'abstract_metadata_line':metadata.get('metadata_line'),'metadata_abstract':metadata.get('abstract'),'metadata_versions':metadata.get('versions'),'metadata_license':metadata.get('license'),'metadata_authors':metadata.get('authors'),'abstract_split_method':split['body_split_method'],'math_markup_normalization':'adjacent inline expression delimiters separated by a space; expression content unchanged'},'status':{'text_exported':True,'equations_extracted':True,'math_verified_against_pdf':False,'algorithm_implemented':False,'simulation_validated':False},'limitations':['Existing local conversion may contain mathematical transcription errors.','Figures and captions omitted; text references to figures remain and some circuits require reconstruction.','Finite-instance circuit feasibility and runtime are unverified.','Family simulation target is an editorial template, not a paper-specific experimental specification.']}
  evidence=[]
  for paragraph in re.split(r'\n\s*\n',abstract+'\n\n'+body):
   if re.search(r'\b(algorithms?|circuits?|quantum walks?|gates?|coin operator|shift operator|phase estimation|protocol)\b',paragraph,re.I):
    evidence.append(paragraph[:900])
    if len(evidence)==3:break
  row['screening']={'tier':tier,'method':'editorial_title_abstract_screen_plus_programmatic_full_text_signals','algorithm_evidence':evidence,'additional_design_requirements':flags,'small_simulation_feasibility':'not_verified','original_ten':aid in seeds,'content_type':'constructive_evolution_model' if family=='quantum_walk_construction' else 'algorithm_or_circuit_procedure','abstract_alignment':{k:v for k,v in split.items() if k!='local_abstract'}}
  rows.append(row)
  screen.append({'arxiv_id':aid,'title':row['title'],'family':family,'tier':tier,'design_requirements':flags,'abstract_words':len(abstract.split()),'abstract_metadata_similarity':split.get('local_abstract_similarity'),'body_headings':re.findall(r'^#{1,6}\s+(.+)$',body,re.M)[:30],'evidence':evidence})
  if order%50==0:print('Exported',order,flush=True)
 jsonl(ROOT/'manifest.jsonl',rows);jsonl(ROOT/'provenance/screening.jsonl',screen)
 for src in (SEED/'qiskit_textbooks').rglob('*'):
  if src.is_file():
   dst=ROOT/'qiskit_textbooks'/src.relative_to(SEED/'qiskit_textbooks');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 with (ROOT/'catalog.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['order','arxiv_id','title','family','screening_tier','display_equations','abstract_file','paper_file','equations_file'])
  for r in rows:w.writerow([r['suggested_order'],r['arxiv_id'],r['title'],r['family'],r['screening']['tier'],r['counts']['display_equations'],r['files']['abstract'],r['files']['paper'],r['files']['equations']])
 families=collections.Counter(r['family'] for r in rows);tiers=collections.Counter(r['screening']['tier'] for r in rows)
 summary={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'paper_count':len(rows),'approved_seed_papers':sum(r['screening']['original_ten'] for r in rows),'families':dict(families),'screening_tiers':dict(tiers),'display_equations':sum(r['counts']['display_equations'] for r in rows),'inline_math':sum(r['counts']['inline_math'] for r in rows),'textbook_exports':sum(1 for l in (ROOT/'qiskit_textbooks/index.jsonl').open()),'source_collections':dict(collections.Counter(r['provenance'].get('source_collection','approved_seed_main_arxiv') for r in rows)),'network_used':False,'models_started':False,'simulations_run':False,'source_manifest_sha256':sha(ROOT/'provenance/selection.json'),'manifest_sha256':sha(ROOT/'manifest.jsonl')}
 jsonfile(ROOT/'provenance/build.json',summary)
 lines=['# Paper catalog','', 'All targets remain unvalidated. The first ten preserve the approved seed.','', '| Order | Paper | Topic | Screening tier |','|---|---|---|---|']
 for r in rows:lines.append(f'| {r["suggested_order"]} | [{r["arxiv_id"]}: {r["title"].replace("|","/")}]({r["files"]["paper"]}) | {r["family"]} | {r["screening"]["tier"]} |')
 (ROOT/'PAPERS.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
