#!/usr/bin/env python3

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


File: ggwp.py
Description: Main callable file for the GGWP discord bot
Usage: $ python3 ggwp.py
"""

import json
import logging
from bot import Bot

__author__ = "Tem Tamre"
__contact__ = "ttamre@ualberta.ca"

logging.basicConfig(level=logging.INFO)

license_text = """
ggwp Copyright (C) 2019 Tem Tamre
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it under certain conditions.
    For further information, please refer to the source at which you obtained this software.
"""

if __name__ == "__main__":
    with open("secrets.json") as f:
        token = json.load(f)["DISCORD_BOT_TOKEN"]
    
    logging.info(license_text)
    bot = Bot()
    bot.run(token)
