#!/usr/bin/env python

"""
File: bot.py
Description: Bot class
"""

import discord
import json
import logging
from riot_client import RiotGamesClient

client = RiotGamesClient()
logging.basicConfig(level=logging.INFO)

class Bot(discord.Client):
    async def on_ready(self):
        print("\nLogged in as {}\n".format(self.user))
        self.client = RiotGamesClient()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("./"):
            input_message = message.content.split(" ")

            if "rank" in input_message[0]:
                summoner_name = input_message[1]
                logging.info("INFO: Executing RiotGamesClient.get_summoner_rank() in Bot.on_message()")
                output_message = client.get_summoner_rank(summoner_name)
                if not output_message:
                    output_message = "**Invalid input**, try `./rank summoner_name`"
                logging.info("INFO: Sending RiotGamesClient.get_summoner_rank() response to text channel in Bot.on_message()")
                await message.channel.send(output_message)
            
            if "mastery" in input_message[0]:
                summoner_name = input_message[1]
                champion_name = input_message[2]
                logging.info("INFO: Executing RiotGamesClient.get_champion_mastery() in Bot.on_message()")
                output_message = client.get_champion_mastery(summoner_name, champion_name)
                if not output_message:
                    output_message = "**Invalid input**, try `./mastery summoner_name champion_name`"
                logging.info("INFO: Sending RiotGamesClient.get_champion_mastery() response to text channel in Bot.on_message()")
                await message.channel.send(output_message)
            
            if "game" in input_message[0]:
                summoner_name = input_message[1]
                logging.info("INFO: Executing RiotGamesClient.get_current_game_info() in Bot.on_message()")
                output_message = client.get_current_game_info(summoner_name)
                if not output_message:
                    output_message = "**Invalid input**, try `./game summoner_name` for a summoner that is in an active game"
                logging.info("INFO: Sending RiotGamesClient.get_summoner_rank() response to text channel in Bot.on_message()")
                await message.channel.send(output_message)


if __name__ == "__main__":
    with open("secrets.json") as f:
        json_object = json.load(f)
        token = json_object["DISCORD_BOT_TOKEN"]
    bot = Bot()
    bot.run(token)