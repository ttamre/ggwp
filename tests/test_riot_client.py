"""
ggwp - A League of Legends stat fetching Discord bot
Copyright (C) 2019 Tem Tamre

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

File: test_riot_client.py
Description: Unit test for riot_client.py
"""

import unittest
from riot_client import RiotGamesClient


class TestRiotClient(unittest.TestCase):
    def setUp(self):
        self.client = RiotGamesClient(secrets_path="secrets_template.json")

    def test_init(self):
        assert self.client.riot_host
        assert self.client.ddragon_host
        assert self.client.api_key
        assert self.client.headers
        assert self.client.queue_types
        assert self.client.queue_ids

    def test_seconds_to_time(self):
        tests = [
            ("50", "0:50"),
            ("125", "2:05"),
            ("395", "6:35"),
            ("1147", "19:07"),
            ("string", "Unknown"),
            (["list", "list"], "Unknown"),
            ({"key": "val"}, "Unknown")
        ]

        for test_case in tests:
            assert self.client.seconds_to_time(test_case[0]) == test_case[1]

    def test_get_api_key(self):
        assert self.client.api_key == "riot_api_key"

    def test_generate_headers(self):
        assert ["Origin", "Accept-Charset", "X-Riot-Token", "Accept-Language", "User-Agent"] == list(self.client.headers.keys())

    def tearDown(self):
        del self.client
