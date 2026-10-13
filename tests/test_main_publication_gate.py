"""Eine Main-Integration darf keine ungeprüften Registry-Stände veröffentlichen."""
from pathlib import Path
import unittest
import yaml


class MainPublicationGateTests(unittest.TestCase):
    def test_main_workflow_hat_keine_schreibrechte_auf_container_registry(self):
        workflow = yaml.safe_load((Path(__file__).resolve().parents[1] / '.github/workflows/docker-build.yml').read_text())
        trigger = workflow.get('on', workflow.get(True))
        self.assertIn('main', trigger['push']['branches'])
        for job in workflow['jobs'].values():
            permissions = job.get('permissions', workflow.get('permissions', {}))
            self.assertNotEqual(permissions.get('packages'), 'write')


if __name__ == '__main__':
    unittest.main()
