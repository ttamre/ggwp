#!/usr/bin/env python3

"""
File: bot.py
Description: File that contains the bot class
"""

import discord
import json
import logging
from riot_client import RiotGamesClient

__author__ = "Tem Tamre"
__contact__ = "ttamre@ualberta.ca"

RiotClient = RiotGamesClient()
logging.basicConfig(level=logging.INFO)

with open("secrets.json") as f:
    owners = json.load(f)["OWNERS"]


class Bot(discord.Client):

    async def on_ready(self):
        print("-" * 24)
        print("Logged in as {}\n".format(self.user))
        print("A discord bot that allows users to fetch their League of Legends stats")
        print("Developed and maintained as a personal project by Tem Tamre (ttamre@ualberta.ca)")
        print("Source code available at https://github.com/ttamre/ggwp")
        print("-" * 24)

        await self.change_presence(status=discord.Status.online, activity=discord.Activity(name="./help for help"))

    async def on_message(self, message):
        """
        Sends a message to the channel that a command was issued in
        :param message:message  Command issued by a user
        """
        if message.author == self.user:
            return

        if message.content.startswith("./"):
            input_message = message.content.split(" ")
            logging.info("{user} said: {message}".format(user=message.author, message=message.content))

            if "./rank" == input_message[0]:
                output_message = self._rank(input_message=input_message)
            
            elif "./mastery" == input_message[0]:
                output_message = self._mastery(input_message=input_message)
            
            elif "./game" == input_message[0]:
                output_message = self._game(input_message=input_message)

            elif "./help" == input_message[0]:
                output_message = self._help()

            elif "./author" == input_message[0]:
                output_message = self._author()
            
            elif "./exit" == input_message[0]:
                if str(message.author) in owners:
                    await message.channel.send("`Logging off`")
                    await self.logout()
                else:
                    output_message = "You do not have permission to use that command"
            
            else:
                output_message = "Invalid command. For a list of commands, enter `./help`"

            await message.channel.send(output_message)

    def _rank(self, input_message):
        """
        Obtain rank info from the RiotClient and return formatted output data
        :param list:input_message   Command issued by a user
        """
        summoner_name = " ".join(input_message[1:])
        output_list = RiotClient.get_summoner_rank(summoner_name)

        if not output_list:
            return "**Invalid input**, try `./rank summoner_name`"

        output_message = ""
        for rank in output_list:
            output_message += rank + '\n'

        return output_message

    def _mastery(self, input_message):
        """
        Obtain mastery info from the RiotClient and return formatted output data
        :param list:input_message   Command issued by a user
        """
        with open("spaced_names.txt") as f:
            champions_with_spaces = f.read().splitlines()

        if " ".join(input_message[-2:]) in (champions_with_spaces):
            summoner_name = " ".join(input_message[1:-2])
            champion_name = " ".join(input_message[-2:])
        else:
            summoner_name = " ".join(input_message[1:-1])
            champion_name = input_message[-1]
        
        output_message = RiotClient.get_champion_mastery(summoner_name, champion_name)
        if not output_message:
            output_message = "**Invalid input**, try `./mastery summoner_name champion_name`"
        
        return output_message

    def _game(self, input_message):
        """
        Obtain live game info from the RiotClient and return formatted output data
        :param list:input_message   Command issued by a user
        """
        summoner_name = input_message[1] if len(input_message) == 2 else " ".join(input_message[1:])
        output_message = RiotClient.get_current_game_info(summoner_name)
        if not output_message:
            output_message = "**Invalid input**, try `./game summoner_name` for a summoner that is in an active game"
        
        return output_message

    def _help(self):
        """
        Return a list of commands that this bot accepts
        """
        rank = "To get your rank, enter `./rank summoner_name`\n"
        mastery = "To get your mastery score on a champion, enter `./mastery summoner_name champion_name`\n"
        game = "To get data for a summoner's game, enter `./game summoner_name`\n"
        author = "To view author contact info, enter `./author`\n"
        exit_ = "To log the bot off, enter `./exit` (only owners of this bot can execute this command, contact the server owner or tei#0397 for assistance)"
        return rank + mastery + game + author + exit_

    def _author(self):
        """
        Return author contact information
        """
        author = "**Author:** Tem Tamre\n"
        contact = "**Contact:** ttamre@ualberta.ca\n"
        github = "**Github:** https://www.github.com/ttamre"
        return author + contact + github