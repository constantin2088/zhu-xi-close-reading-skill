import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_provenance import analyze
class TaskToolTests(unittest.TestCase):
 def sample(self):return json.loads((ROOT/'examples/tool-input.json').read_text(encoding='utf-8'))
 def test_reposts_do_not_multiply(self):
  self.assertEqual(analyze(self.sample())['source_chains']['c1'],['original'])
 def test_common_origin(self):
  p=self.sample();p['sources'].append({'id':'copy2','parent':'copy'});p['claims'][0]['sources']=['copy','copy2'];self.assertEqual(analyze(p)['source_chains']['c1'],['original'])
 def test_missing_original(self):
  p=self.sample();p['sources'][1]['parent']='lost'
  with self.assertRaises(ValueError):analyze(p)
 def test_source_cycle(self):
  p=self.sample();p['sources'][0]['parent']='copy'
  with self.assertRaises(ValueError):analyze(p)
 def test_unresolved_claim_reference(self):
  p=self.sample();p['claims'][0]['sources']=['unknown']
  with self.assertRaises(ValueError):analyze(p)

if __name__=='__main__':unittest.main()
