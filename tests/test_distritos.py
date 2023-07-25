"""
Unit tests for distritos category
"""
import unittest

import requests

from tests.load_env import config


class TestDistritos(unittest.TestCase):
    """Tests for distritos category"""

    def test_get_distritos(self):
        """Test GET method for distritos"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_distritos_with_page_and_size(self):
        """Test GET method for distritos with page 2 and size 5"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"page": 2, "size": 5},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_distritos_by_es_distrito_judicial(self):
        """Test GET method for distritos by es_distrito_judicial"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_distrito_judicial": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_distrito_judicial"], 1)

    def test_get_distritos_by_es_distrito(self):
        """Test GET method for distritos by es_distrito"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_distrito": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_distrito"], 1)

    def test_get_distritos_by_es_jurisdiccional(self):
        """Test GET method for distritos by es_jurisdiccional"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_jurisdiccional": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_jurisdiccional"], 1)

    def test_get_distrito_by_clave(self):
        """Test for get distrito by clave"""
        for clave in ["DSLT", "DTRC"]:
            response = requests.get(
                f"{config['host']}/v4/distritos/{clave}",
                headers={"X-API-Key": config["api_key"]},
                timeout=config["timeout"],
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["success"], True)
            self.assertEqual(data["clave"], clave)


if __name__ == "__main__":
    unittest.main()
