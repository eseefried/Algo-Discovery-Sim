import re,html,difflib

def normalize(s):return re.findall(r'[a-z]+',html.unescape(s).lower())
def similarity(a,b):
 a=normalize(a);b=normalize(b)
 if not a or not b:return 0
 return difflib.SequenceMatcher(None,a,b,autojunk=False).ratio()
def split_paper(text,metadata):
 intro=re.search(r'^#{1,6}\s+(?:(?:[IVX]+|\d+)[.\s]+)?Introduction\b[^\n]*',text,re.M|re.I)
 marker=re.search(r'^(?:#{1,6}\s*)?(?:\*\*)?Abstract(?:\*\*)?[.\s:—–-]*(?:\n|(?=[A-Z]))',text,re.M)
 meta=(metadata or {}).get('abstract','').strip()
 if intro:
  front=text[:intro.start()];body=text[intro.start():];method='body begins at introduction heading'
  if marker and marker.end()<intro.start():local=front[marker.end():].strip()
  else:
   paras=[p for p in re.split(r'\n\s*\n',front) if len(p)>120 and not p.lstrip().startswith('#')]
   if meta:local=max(paras,key=lambda p:similarity(meta,p),default='')
   else:local=max(paras,key=len,default='')
 else:
  # Without an introduction heading, locate the abstract paragraph(s) using
  # the local arXiv metadata. Drop front matter and only those paragraphs.
  start=marker.end() if marker else 0
  paras=list(re.finditer(r'[^\n]+(?:\n(?!\s*\n)[^\n]+)*',text[start:15000]))
  candidates=[]
  for i,p in enumerate(paras):
   if len(p.group())<100 or p.group().lstrip().startswith('#'):continue
   for count in range(1,4):
    if i+count>len(paras):break
    end=paras[i+count-1].end();part=text[start+p.start():start+end]
    candidates.append((similarity(meta,part) if meta else (1/len(part) if marker and i==0 else 0),start+p.start(),start+end,part))
  best=max(candidates,default=(0,0,0,''))
  if meta and best[0]<.38:raise ValueError(f'cannot locate local abstract confidently: similarity={best[0]:.3f}')
  if not best[2]:raise ValueError('no abstract boundary')
  local=best[3];body=text[best[2]:];method='unsectioned introduction: local abstract located by metadata token alignment' if meta else 'first long paragraph after abstract marker'
 # Abstract metadata and headings sometimes contain classification boilerplate.
 local=re.split(r'\n\s*(?:\*\*pacs\*\*|PACS|Keywords|Key words|Introduction\b|\*\*Keywords)',local,flags=re.I)[0].strip()
 extra=re.search(r'(?mi)^\s*(?:Table\s+\d+\s*:|Errata\s*:|Program summary\s*$|\[\]\s*$)',local)
 if extra:
  body=local[extra.start():].strip()+'\n\n'+body
  local=local[:extra.start()].strip()
 abstract=local;abstract_origin='local_paper_conversion_aligned_with_metadata_when_available'
 if len(abstract)<150 or len(body)<3000:raise ValueError('abstract/body too short')
 score=similarity(meta,local) if meta else None
 return abstract,body,{'body_split_method':method,'abstract_origin':abstract_origin,'local_abstract_similarity':round(score,4) if score is not None else None,'local_abstract':local,'abstract_version_match':'metadata_unavailable' if score is None else ('not_established' if score<.85 else 'high_textual_similarity_not_version_certification')}
