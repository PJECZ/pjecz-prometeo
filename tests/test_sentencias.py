"""
Unit tests for sentencias category
"""
import unittest

import requests

from tests.load_env import config


class TestSentencias(unittest.TestCase):
    """Tests for sentencias category"""

    def test_get_sentencias(self):
        """Test GET method for sentencias"""
        response = requests.get(
            f"{config['host']}/v4/sentencias",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_sentencias_by_autoridad_id_37(self):
        """Test GET method for sentencias by autoridad_id 37"""
        response = requests.get(
            f"{config['host']}/v4/sentencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 37},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 37)

    def test_get_sentencias_by_autoridad_id_37_by_expediente(self):
        """Test GET method for sentencias by autoridad_id 37 by expediente 197/2019"""
        response = requests.get(
            f"{config['host']}/v4/sentencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 37, "expediente": "197/2019"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 37)
            self.assertEqual(item["expediente"], "197/2019")

    def test_get_sentencias_by_autoridad_id_37_by_sentencia(self):
        """Test GET method for sentencias by autoridad_id 37 by sentencia 160/2021"""
        response = requests.get(
            f"{config['host']}/v4/sentencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 37, "sentencia": "160/2021"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 37)
            self.assertEqual(item["sentencia"], "160/2021")

    def test_get_sentencias_by_autoridad_clave_stl_j2_civ(self):
        """Test GET method for sentencias by autoridad_clave SLT-J2-CIV"""
        response = requests.get(
            f"{config['host']}/v4/sentencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J2-CIV"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J2-CIV")

    def test_get_sentencias_by_autoridad_clave_stl_j2_civ_by_expediente(self):
        """Test GET method for sentencias by autoridad_clave SLT-J2-CIV by expediente 197/2019"""
        response = requests.get(
            f"{config['host']}/v4/sentencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J2-CIV", "expediente": "197/2019"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J2-CIV")
            self.assertEqual(item["expediente"], "197/2019")

    def test_get_sentencias_by_autoridad_clave_stl_j2_civ_by_sentencia(self):
        """Test GET method for sentencias by autoridad_clave SLT-J2-CIV by sentencia 160/2021"""
        response = requests.get(
            f"{config['host']}/v4/sentencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J2-CIV", "sentencia": "160/2021"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J2-CIV")
            self.assertEqual(item["sentencia"], "160/2021")


if __name__ == "__main__":
    unittest.main()
