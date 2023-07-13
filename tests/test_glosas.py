"""
Unit tests for glosas category
"""
import unittest

import requests

from tests.load_env import config


class TestGlosas(unittest.TestCase):
    """Tests for glosas category"""

    def test_get_glosas(self):
        """Test GET method for glosas"""
        response = requests.get(
            f"{config['host']}/v4/glosas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_glosas_by_autoridad_id_53(self):
        """Test GET method for glosas by autoridad_id 53"""
        response = requests.get(
            f"{config['host']}/v4/glosas",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 53},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 53)

    def test_get_glosas_by_autoridad_id_53_by_fechas(self):
        """Test GET method for glosas by autoridad_id 53 fecha_desde 2020-01-01 and fecha_hasta 2020-01-31"""
        response = requests.get(
            f"{config['host']}/v4/glosas",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 53, "fecha_desde": "2020-01-01", "fecha_hasta": "2020-01-31"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 53)
            self.assertGreaterEqual(item["fecha"], "2020-01-01")
            self.assertLessEqual(item["fecha"], "2020-01-31")

    def test_get_glosas_by_autoridad_clave_trn_cya(self):
        """Test GET method for glosas by autoridad_clave TRN-CYA"""
        response = requests.get(
            f"{config['host']}/v4/glosas",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "TRN-CYA"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "TRN-CYA")

    def test_get_glosas_by_autoridad_clave_trn_cya_by_fechas(self):
        """Test GET method for glosas by autoridad_clave TRN-CYA fecha_desde 2020-01-01 and fecha_hasta 2020-01-31"""
        response = requests.get(
            f"{config['host']}/v4/glosas",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "TRN-CYA", "fecha_desde": "2020-01-01", "fecha_hasta": "2020-01-31"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "TRN-CYA")
            self.assertGreaterEqual(item["fecha"], "2020-01-01")
            self.assertLessEqual(item["fecha"], "2020-01-31")


if __name__ == "__main__":
    unittest.main()
