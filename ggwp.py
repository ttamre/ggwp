#!/usr/bin/env python3

"""
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


if __name__ == "__main__":
    with open("secrets.json") as f:
        token = json.load(f)["DISCORD_BOT_TOKEN"]
    
    bot = Bot()
    bot.run(token)