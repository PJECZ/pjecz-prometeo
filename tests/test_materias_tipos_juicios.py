"""
Unit tests for materias category
"""
import unittest

import requests

from tests.load_env import config


class TestMaterias(unittest.TestCase):
    """Tests for materias category"""

    url = f"{config['host']}/v4/materias_tipos_juicios"

    def test_get_materias_tipos_juicios(self):
        """Test GET method for materias_tipos_juicios"""
        response = requests.get(
            url=f"{self.url}/listado",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_materias_tipos_juicios_with_page_and_size(self):
        """Test GET method for materias_tipos_juicios with page 2 and size 5"""
        response = requests.get(
            url=f"{self.url}/listado",
            headers={"X-Api-Key": config["api_key"]},
            params={"page": 2, "size": 5},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
