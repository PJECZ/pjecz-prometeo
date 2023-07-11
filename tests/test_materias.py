"""
Unit tests for materias category
"""
import unittest

import requests

from tests.load_env import config


class TestMaterias(unittest.TestCase):
    """Tests for materias category"""

    def test_get_materia_by_clave(self):
        """Test for get materia by clave"""
        for clave in ["FAM", "CIV", "MER"]:
            response = requests.get(
                f"{config['host']}/v3/materias/{clave}",
                headers={"X-API-Key": config["api_key"]},
                timeout=config["timeout"],
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["success"], True)
            self.assertEqual(data["clave"], clave)


if __name__ == "__main__":
    unittest.main()
