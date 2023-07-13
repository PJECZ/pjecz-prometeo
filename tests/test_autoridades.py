"""
Unit tests for autoridades category
"""
import unittest

import requests

from tests.load_env import config


class TestAutoridades(unittest.TestCase):
    """Tests for autoridades category"""

    def test_get_autoridades(self):
        """Test GET method for autoridades"""
        response = requests.get(
            f"{config['host']}/v4/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_autoridades_by_es_cemasc(self):
        """Test GET method for autoridades by es_cemasc"""
        response = requests.get(
            f"{config['host']}/v4/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_cemasc": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_cemasc"], 1)

    def test_get_autoridades_by_es_creador_glosas(self):
        """Test GET method for autoridades by es_creador_glosas"""
        response = requests.get(
            f"{config['host']}/v4/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_creador_glosas": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_creador_glosas"], 1)

    def test_get_autoridades_by_es_defensoria(self):
        """Test GET method for autoridades by es_defensoria"""
        response = requests.get(
            f"{config['host']}/v4/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_defensoria": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_defensoria"], 1)

    def test_get_autoridades_by_es_jurisdiccional(self):
        """Test GET method for autoridades by es_jurisdiccional"""
        response = requests.get(
            f"{config['host']}/v4/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_jurisdiccional": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_jurisdiccional"], 1)

    def test_get_autoridades_by_es_notaria(self):
        """Test GET method for autoridades by es_notaria"""
        response = requests.get(
            f"{config['host']}/v4/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_notaria": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_notaria"], 1)

    def test_get_autoridad_by_clave(self):
        """Test for get autoridad by clave"""
        for clave in ["SLT-J1-FAM", "TRC-J2-CIV", "MNC-J2-FAM"]:
            response = requests.get(
                f"{config['host']}/v4/autoridades/{clave}",
                headers={"X-API-Key": config["api_key"]},
                timeout=config["timeout"],
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["success"], True)
            self.assertEqual(data["clave"], clave)


if __name__ == "__main__":
    unittest.main()
