"""Ein frischer GraphHopper-Stand braucht persistente Eingaben und sein bestehendes Fahrzeugprofil."""
from pathlib import Path
import unittest
import yaml


class RoutingConfigurationTests(unittest.TestCase):
    def test_daten_und_graph_liegen_auf_dem_separaten_staging_volume(self):
        config = yaml.safe_load((Path(__file__).resolve().parents[1] / 'config.yml').read_text())['graphhopper']
        self.assertTrue(config['datareader.file'].startswith('/data/'))
        self.assertTrue(config['graph.location'].startswith('/data/'))

    def test_bestehende_car_route_bleibt_verfuegbar(self):
        config = yaml.safe_load((Path(__file__).resolve().parents[1] / 'config.yml').read_text())['graphhopper']
        self.assertIn('car', {profile['name'] for profile in config['profiles']})


if __name__ == '__main__':
    unittest.main()
