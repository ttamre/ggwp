#!/usr/bin/env python3

"""
File: bot.py
Description: Bot class

TODO help function
"""

import discord
import json
import logging
from riot_client import RiotGamesClient

client = RiotGamesClient()
logging.basicConfig(level=logging.INFO)
owners = ["tei#0397"]

class Bot(discord.Client):
    async def on_ready(self):
        print("-" * 24)
        print("Logged in as {}\n".format(self.user))
        print("A discord bot that allows users to fetch their League of Legends stats")
        print("Developed and maintained as a personal project by Tem Tamre (ttamre@ualberta.ca)")
        print("Source code available at https://github.com/ttamre/ggwp")
        print("-" * 24)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("./"):
            input_message = message.content.split(" ")
            logging.info("{user} said: {message}".format(user=message.author, message=message.content))

            if "rank" in input_message[0]:
                summoner_name = " ".join(input_message[1:])
                logging.info("INFO: Executing RiotGamesClient.get_summoner_rank() in Bot.on_message()")
                output_list = client.get_summoner_rank(summoner_name)
                if not output_list:
                    await message.channel.send("**Invalid input**, try `./rank summoner_name`")
                logging.info("INFO: Sending RiotGamesClient.get_summoner_rank() response to text channel in Bot.on_message()")
                for output_message in output_list:
                    await message.channel.send(output_message)
            
            if "mastery" in input_message[0]:
                with open("spaced_names.txt") as f:
                    champions_with_spaces = f.read().splitlines()
                
                print(champions_with_spaces)
                print(input_message[-2:])
                if " ".join(input_message[-2:]) in (champions_with_spaces):
                    logging.info("Champion with spaced name detected")
                    summoner_name = " ".join(input_message[1:-2])
                    champion_name = " ".join(input_message[-2:])
                else:
                    logging.info("Champion with single name detected")
                    summoner_name = " ".join(input_message[1:-1])
                    champion_name = input_message[-1]

                logging.info("INFO: Executing RiotGamesClient.get_champion_mastery() in Bot.on_message()")
                
                output_message = client.get_champion_mastery(summoner_name, champion_name)
                if not output_message:
                    output_message = "**Invalid input**, try `./mastery summoner_name champion_name`"
                
                logging.info("INFO: Sending RiotGamesClient.get_champion_mastery() response to text channel in Bot.on_message()")
                await message.channel.send(output_message)
            
            if "game" in input_message[0]:
                summoner_name = input_message[1] if len(input_message) == 2 else " ".join(input_message[1:])
                logging.info("INFO: Executing RiotGamesClient.get_current_game_info() in Bot.on_message()")
                
                output_message = client.get_current_game_info(summoner_name)
                if not output_message:
                    output_message = "**Invalid input**, try `./game summoner_name` for a summoner that is in an active game"
                
                logging.info("INFO: Sending RiotGamesClient.get_summoner_rank() response to text channel in Bot.on_message()")
                await message.channel.send(output_message)

            if "help" in input_message[0]:
                logging.info("INFO: Executing help message in Bot.on_message()")
                
                rank = "To get your rank, enter `./rank summoner_name`\n"
                mastery = "To get your mastery score on a champion, enter `./mastery summoner_name champion_name`\n"
                game = "To get data for a summoner's game, enter `./game summoner_name`\n"
                author = "To view author contact info, enter `./author`\n"
                
                logging.info("INFO: Sending help data to text channel in Bot.on_message()")
                await message.channel.send(rank + mastery + game + author)

            if "author" in input_message[0]:
                logging.info("INFO: Executing author message in Bot.on_message()")
                
                author = "**Author:** Tem Tamre\n"
                contact = "**Contact:** ttamre@ualberta.ca\n"
                github = "**Github:** https://www.github.com/ttamre"

                logging.info("INFO: Sending author data to text channel in Bot.on_message()")
                await message.channel.send(author + contact + github)
            
            if "exit" in input_message[0] and str(message.author) in owners:
                logging.info("INFO: {user} sent exit command".format(user=message.author))
                await message.channel.send("`Logging off`")
                await self.logout()
