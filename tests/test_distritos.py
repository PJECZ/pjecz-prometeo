"""
Unit tests for distritos category
"""
import unittest

import requests

from tests.load_env import config


class TestDistritos(unittest.TestCase):
    """Tests for distritos category"""

    def test_get_distrito_by_clave(self):
        """Test for get distrito by clave"""
        for clave in ["DSLT", "DTRC"]:
            response = requests.get(
                f"{config['host']}/v3/distritos/{clave}",
                headers={"X-API-Key": config["api_key"]},
                timeout=config["timeout"],
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["success"], True)
            self.assertEqual(data["clave"], clave)


if __name__ == "__main__":
    unittest.main()
