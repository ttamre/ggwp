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

File: test_bot.py
Description: Unit test for bot.py

# TODO mocking RiotClient
"""

import unittest
from bot import Bot


class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = Bot()

    def test_help(self):
        assert isinstance(self.bot._help(), str)

    def test_author(self):
        assert isinstance(self.bot._author(), str)
    
    def tearDown(self):
        del self.bot