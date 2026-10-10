"""Local deterministic aid; never a factual or model behavior certificate."""
def analyze(p):
 sources=p['sources'];lookup={x['id']:x for x in sources}
 if len(lookup)!=len(sources):raise ValueError('duplicate source id')
 def root(k,seen=None):
  seen=set() if seen is None else seen
  if k in seen:raise ValueError('cyclic provenance')
  if k not in lookup:raise ValueError('unknown source')
  seen.add(k);parent=lookup[k].get('parent')
  return root(parent,seen) if parent else k
 for k in lookup:root(k)
 result={}
 for c in p['claims']:
  if c['id'] in result:raise ValueError('duplicate claim id')
  result[c['id']]=sorted({root(k) for k in c['sources']})
 return {'source_chains':result,'note':'Distinct chains are not proof of truth or independence; check actual common origins.'}

if __name__=='__main__':
 import json,sys
 print(json.dumps(analyze(json.loads(open(sys.argv[1],encoding='utf-8').read())),ensure_ascii=False,indent=2))
