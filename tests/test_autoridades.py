"""
Unit tests for autoridades category
"""
import unittest

import requests

from tests.load_env import config


class TestAutoridades(unittest.TestCase):
    """Tests for autoridades category"""

    def test_get_autoridad_by_clave(self):
        """Test for get autoridad by clave"""
        for clave in ["SLT-J1-FAM", "TRC-J2-CIV", "MNC-J2-FAM"]:
            response = requests.get(
                f"{config['host']}/v3/autoridades/{clave}",
                headers={"X-API-Key": config["api_key"]},
                timeout=config["timeout"],
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["success"], True)
            self.assertEqual(data["clave"], clave)


if __name__ == "__main__":
    unittest.main()
