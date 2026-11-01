import copy
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from portfolio.dispatcher import plan

ROOT = Path(__file__).resolve().parents[1]


class DispatcherTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / 'portfolio/synthetic-registry.json').read_text())
        self.tasks = json.loads((ROOT / 'portfolio/synthetic-tasks.json').read_text())['tasks']

    def reason(self, task):
        return plan(self.registry, [task])['tasks'][0]['reason']

    def test_three_lanes_and_repository_lock(self):
        result = plan(self.registry, self.tasks)
        self.assertEqual(result['counts'], {'selected': 3, 'held': 3, 'completed': 0})
        self.assertEqual([r['task_id'] for r in result['selected']], ['SYN-01', 'SYN-02', 'SYN-03'])
        self.assertEqual(result['tasks'][-1]['reason'], 'repository_busy')

    def test_repeat_is_deterministic_and_inputs_unchanged(self):
        original = copy.deepcopy((self.registry, self.tasks))
        self.assertEqual(plan(self.registry, self.tasks), plan(self.registry, self.tasks))
        self.assertEqual(original, (self.registry, self.tasks))

    def test_lane_capacity(self):
        a, b = copy.deepcopy(self.tasks[1]), copy.deepcopy(self.tasks[1])
        b.update(id='extra', repository_id='4')
        rows = plan(self.registry, [a, b])['tasks']
        self.assertEqual(rows[1]['reason'], 'lane_capacity')

    def test_unknown_repository(self):
        self.assertEqual(self.reason(self.tasks[-1]), 'repository_not_registered')

    def test_project_mapping_not_inferred(self):
        self.registry['registry_items'][0]['project_id'] = None
        self.assertEqual(self.reason(self.tasks[0]), 'project_mapping_unverified')

    def test_wrong_project(self):
        self.tasks[0]['project_id'] = 'invented'
        self.assertEqual(self.reason(self.tasks[0]), 'project_mapping_unverified')

    def test_unknown_task_dependency(self):
        self.tasks[0]['depends_on'] = ['missing']
        self.assertEqual(self.reason(self.tasks[0]), 'dependency_unknown')

    def test_pending_dependency(self):
        rows = plan(self.registry, self.tasks)['tasks']
        self.assertEqual(next(r for r in rows if r['task_id'] == 'SYN-04')['reason'], 'dependency_pending')

    def test_completed_dependency_unlocks_without_mutating_registry(self):
        result = plan(self.registry, [self.tasks[0], self.tasks[3]], ['SYN-01'])
        self.assertEqual(result['selected'][0]['task_id'], 'SYN-04')

    def test_stale_ci(self):
        self.tasks[1]['ci']['sha'] = 'old-head'
        self.assertEqual(self.reason(self.tasks[1]), 'ci_unverified')

    def test_failed_missing_or_empty_ci_checks(self):
        for state in ['failure', 'skipped', 'cancelled', None]:
            self.tasks[1]['ci']['checks']['unit'] = state
            self.assertEqual(self.reason(self.tasks[1]), 'ci_unverified')
        self.tasks[1]['required_checks'] = []
        self.assertEqual(self.reason(self.tasks[1]), 'ci_unverified')

    def test_repair_can_address_failed_ci(self):
        self.tasks[0]['ci'] = {'checks': {'unit': 'failure'}}
        self.assertIsNone(self.reason(self.tasks[0]))

    def test_missing_head(self):
        self.tasks[0].pop('head_sha')
        self.assertEqual(self.reason(self.tasks[0]), 'head_sha_missing')

    def test_duplicate_provider_identity_rejected(self):
        self.registry['registry_external_refs'].append(self.registry['registry_external_refs'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate provider'):
            plan(self.registry, self.tasks)

    def test_duplicate_task_or_registry_id_rejected(self):
        with self.assertRaises(ValueError):
            plan(self.registry, self.tasks + [self.tasks[0]])
        self.registry['projects'].append(self.registry['projects'][0])
        with self.assertRaises(ValueError):
            plan(self.registry, self.tasks)

    def test_unknown_lane_rejected(self):
        self.tasks[0]['lane'] = 'deploy'
        with self.assertRaisesRegex(ValueError, 'Unknown lane'):
            plan(self.registry, self.tasks)

    def test_task_cycle_rejected(self):
        self.tasks[0]['depends_on'] = ['SYN-04']
        with self.assertRaisesRegex(ValueError, 'Task dependency cycle'):
            plan(self.registry, self.tasks)

    def test_registry_dependency_holds(self):
        self.registry['registry_dependencies'] = [{'source_item_id':'synthetic-item-1', 'target_item_id':'synthetic-item-2'}]
        self.registry['registry_items'][1]['status'] = 'discovered'
        self.assertEqual(self.reason(self.tasks[0]), 'registry_dependency_unverified')

    def test_registry_cycle_rejected(self):
        self.registry['registry_dependencies'] = [{'source_item_id':'synthetic-item-1', 'target_item_id':'synthetic-item-1'}]
        with self.assertRaisesRegex(ValueError, 'Registry dependency cycle'):
            plan(self.registry, self.tasks)

    def test_dangling_registry_edge_rejected(self):
        self.registry['registry_dependencies'] = [{'source_item_id':'synthetic-item-1', 'target_item_id':'missing'}]
        with self.assertRaisesRegex(ValueError, 'Dangling'):
            plan(self.registry, self.tasks)

    def test_no_network_and_no_process_execution(self):
        with patch.object(socket.socket, 'connect', side_effect=AssertionError('network forbidden')), patch('subprocess.run', side_effect=AssertionError('execution forbidden')):
            self.assertEqual(plan(self.registry, self.tasks)['mode'], 'plan_only')

    def test_cli_and_private_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'plan.json'
            subprocess.run([sys.executable, '-m', 'portfolio.dispatcher', '--registry', str(ROOT/'portfolio/synthetic-registry.json'), '--tasks', str(ROOT/'portfolio/synthetic-tasks.json'), '--output', str(output)], cwd=ROOT, check=True, capture_output=True)
            self.assertEqual(json.loads(output.read_text())['counts']['selected'], 3)
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)


if __name__ == '__main__':
    unittest.main()
