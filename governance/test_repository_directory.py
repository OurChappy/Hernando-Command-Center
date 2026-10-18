"""Read-only repository governance manifest checks. Run: python -m unittest discover -s governance -p 'test_*.py' -v"""
import json, unittest
from pathlib import Path
DATA=json.loads(Path(__file__).with_name('repository-directory.json').read_text())
class TestDirectory(unittest.TestCase):
 def test_repo_ids_unique_and_complete(self):
  rs=DATA['repositories']
  self.assertEqual(len(rs),15)
  self.assertEqual(len({x['github_repository_id'] for x in rs}),15)
  self.assertEqual(len({x['full_name'] for x in rs}),15)
  self.assertTrue(all(x['full_name'].startswith('OurChappy/') for x in rs))
 def test_no_mutations(self):
  self.assertTrue(DATA['no_repository_mutations'])
  self.assertEqual(DATA['policy'],'documentation_only')
 def test_explicit_workstreams(self):
  keys={x['key'] for x in DATA['pr_workstreams']}
  self.assertEqual(keys,{'REGISTRY','CONSOLE','AGENT_BUILDER','EDUCAGEN','CI'})
 def test_master_branch_preserved(self):
  r=next(x for x in DATA['repositories'] if x['full_name']=='OurChappy/stripe-python')
  self.assertEqual(r['default_branch'],'master')
if __name__=='__main__':unittest.main()
