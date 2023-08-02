"""
Unit tests for materias category
"""
import unittest

import requests

from tests.load_env import config


class TestMaterias(unittest.TestCase):
    """Tests for materias category"""

    url = f"{config['host']}/v4/materias"

    def test_get_materias(self):
        """Test GET method for materias"""
        response = requests.get(
            url=f"{self.url}/listado",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_materias_with_page_and_size(self):
        """Test GET method for materias with page 2 and size 5"""
        response = requests.get(
            url=f"{self.url}/listado",
            headers={"X-Api-Key": config["api_key"]},
            params={"page": 2, "size": 5},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_materia_by_clave(self):
        """Test for get materia by clave"""
        for clave in ["FAM", "CIV", "MER"]:
            response = requests.get(
                url=f"{self.url}/{clave}",
                headers={"X-API-Key": config["api_key"]},
                timeout=config["timeout"],
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["success"], True)
            self.assertEqual(data["clave"], clave)


if __name__ == "__main__":
    unittest.main()
