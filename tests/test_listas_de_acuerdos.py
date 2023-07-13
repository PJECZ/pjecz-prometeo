"""
Unit tests for listas de acuerdos category
"""
import unittest

import requests

from tests.load_env import config


class TestListasDeAcuerdos(unittest.TestCase):
    """Tests for listas de acuerdos category"""

    def test_get_listas_de_acuerdos(self):
        """Test GET method for listas de acuerdos"""
        response = requests.get(
            f"{config['host']}/v4/listas_de_acuerdos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_listas_de_acuerdos_by_autoridad_id_37(self):
        """Test GET method for listas_de_acuerdos by autoridad_id 37"""
        response = requests.get(
            f"{config['host']}/v4/listas_de_acuerdos",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 37},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 37)

    def test_get_listas_de_acuerdos_by_autoridad_id_37_by_fechas(self):
        """Test GET method for listas_de_acuerdos by autoridad_id 37 fecha_desde 2020-01-01 and fecha_hasta 2020-01-31"""
        response = requests.get(
            f"{config['host']}/v4/listas_de_acuerdos",
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

    def test_get_listas_de_acuerdos_by_autoridad_clave_stl_j2_civ(self):
        """Test GET method for listas_de_acuerdos by autoridad_clave SLT-J2-CIV"""
        response = requests.get(
            f"{config['host']}/v4/listas_de_acuerdos",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J2-CIV"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J2-CIV")

    def test_get_listas_de_acuerdos_by_autoridad_clave_stl_j2_civ_by_fechas(self):
        """Test GET method for listas_de_acuerdos by autoridad_clave SLT-J2-CIV fecha_desde 2020-01-01 and fecha_hasta 2020-01-31"""
        response = requests.get(
            f"{config['host']}/v4/listas_de_acuerdos",
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


if __name__ == "__main__":
    unittest.main()
