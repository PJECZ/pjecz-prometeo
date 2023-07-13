"""
Unit tests for edictos category
"""
import unittest

import requests

from tests.load_env import config


class TestEdictos(unittest.TestCase):
    """Tests for edictos category"""

    def test_get_edictos(self):
        """Test GET method for edictos"""
        response = requests.get(
            f"{config['host']}/v4/edictos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_edictos_by_autoridad_id_37(self):
        """Test GET method for edictos by autoridad_id 37"""
        response = requests.get(
            f"{config['host']}/v4/edictos",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 37},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 37)

    def test_get_edictos_by_autoridad_id_37_by_fechas(self):
        """Test GET method for edictos by autoridad_id 37 fecha_desde 2020-01-01 and fecha_hasta 2020-01-31"""
        response = requests.get(
            f"{config['host']}/v4/edictos",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 37, "fecha_desde": "2020-01-01", "fecha_hasta": "2020-01-31"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 37)
            self.assertGreaterEqual(item["fecha"], "2020-01-01")
            self.assertLessEqual(item["fecha"], "2020-01-31")

    def test_get_edictos_by_autoridad_id_35_and_expediente(self):
        """Test GET method for edictos by autoridad_id 35 and expediente 1774/2019"""
        response = requests.get(
            f"{config['host']}/v4/edictos",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 35, "expediente": "1774/2019"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 35)
            self.assertEqual(item["expediente"], "1774/2019")

    def test_get_edictos_by_autoridad_clave_stl_j2_civ(self):
        """Test GET method for edictos by autoridad_clave SLT-J2-CIV"""
        response = requests.get(
            f"{config['host']}/v4/edictos",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J2-CIV"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J2-CIV")

    def test_get_edictos_by_autoridad_clave_stl_j2_civ_by_fechas(self):
        """Test GET method for edictos by autoridad_clave SLT-J2-CIV fecha_desde 2020-01-01 and fecha_hasta 2020-01-31"""
        response = requests.get(
            f"{config['host']}/v4/edictos",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J2-CIV", "fecha_desde": "2020-01-01", "fecha_hasta": "2020-01-31"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J2-CIV")
            self.assertGreaterEqual(item["fecha"], "2020-01-01")
            self.assertLessEqual(item["fecha"], "2020-01-31")

    def test_get_edictos_by_autoridad_clave_stl_j1_fam_and_expediente(self):
        """Test GET method for edictos by autoridad_clave SLT-J1-FAM and expediente 1774/2019"""
        response = requests.get(
            f"{config['host']}/v4/edictos",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J1-FAM", "expediente": "1774/2019"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J1-FAM")
            self.assertEqual(item["expediente"], "1774/2019")


if __name__ == "__main__":
    unittest.main()
