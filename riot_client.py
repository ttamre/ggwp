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


File: riot_client.py
Description: Riot games client for the discord bot to use to make API requests

Features
- Get summoner rank         https://developer.riotgames.com/apis#league-v4/GET_getLeagueEntriesForSummoner
- Get champion mastery      https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getChampionMastery
- Current game info         https://developer.riotgames.com/api-methods/#spectator-v4/GET_getCurrentGameInfoBySummoner

Helpers
- Get summoner ID           https://developer.riotgames.com/api-methods/#summoner-v4/GET_getBySummonerName
- Get champion ID           https://developer.riotgames.com/static-data.html
"""

import json
import requests
import logging
import os
from datetime import datetime, timedelta

__author__ = "Tem Tamre"
__contact__ = "ttamre@ualberta.ca"

logging.basicConfig(level=logging.INFO)


class RiotGamesClient():
    def __init__(self, secrets_path="secrets.json"):
        self.riot_host = "https://na1.api.riotgames.com"
        self.ddragon_host = "http://ddragon.leagueoflegends.com"
        self.api_key = self._get_api_key(path=secrets_path)
        self.headers = self.generate_headers()
        self.queue_types = {"RANKED_FLEX_SR": 440, "RANKED_SOLO_5x5": 420}
        self.queue_ids = {
            0: "Custom",
            430: "Normal Blind",
            400: "Normal Draft",
            420: "Ranked Solo",
            440: "Ranked Flex",
            450: "ARAM"
        }

    def get_summoner_rank(self, summoner_name:str):
        """
        Get a summoner's rank

        :param str:summoner_name    Sanitized summoner name
        :return str:                Output message to write to text channel
        """
        summoner_id = self._get_summoner_id(summoner_name)
        url = self.riot_host + "/lol/league/v4/entries/by-summoner/{sid}".format(sid=summoner_id)
        response = requests.get(url, headers=self.headers)
        try:
            json_object = json.loads(response.text)
            queues = []
            for obj in json_object:
                queue_id = self.queue_types.get(obj["queueType"], '')
                queue = self.queue_ids.get(queue_id, '')
                rank = "{tier} {rank}".format(tier=obj["tier"].title(), rank=obj["rank"])
                lp = obj["leaguePoints"]
                queues.append("**{queue}:** {rank} {lp}LP".format(queue=queue, rank=rank, lp=lp))
            return queues
        except Exception as e:
            if response.status_code != 200:
                logging.error("ERROR: Response code {} in league_client.get_summoner_rank()".format(response.status_code))
                logging.error("Summoner: {s} ({sid})".format(s=summoner_name, sid=summoner_id))
            else:
                logging.error("ERROR: Generic error in league_client.get_summoner_rank()")
            logging.error(e)

    def get_champion_mastery(self, summoner_name:str, champion_name:str):
        """
        Get a summoner's champion mastery level

        :param str:summoner_name    Sanitized summoner name
        :param str:champion_name    Sanitized champion name
        :return str:                Output message to write to text channel
        """
        summoner_id = self._get_summoner_id(summoner_name)
        champion_id = self._get_champion_id(champion_name.title())
        url = self.riot_host + "/lol/champion-mastery/v4/champion-masteries/by-summoner/{sid}/by-champion/{cid}".format(
            sid=summoner_id,
            cid=champion_id
        )
        response = requests.get(url, headers=self.headers)
        try:
            json_object = json.loads(response.text)
            return "**{summoner}'s {champion}:** Mastery rank **{rank}** with **{points}** points".format(
                summoner=summoner_name,
                champion=champion_name,
                rank=json_object["championLevel"],
                points="{:,}".format(json_object["championPoints"])
            )
        except Exception as e:
            if response.status_code != 200:
                logging.error("ERROR: Response code {} in league_client.get_champion_mastery()".format(response.status_code))
                logging.error("Summoner: {s} ({sid})".format(s=summoner_name, sid=summoner_id))
                logging.error("Champion: {c} ({cid})".format(c=champion_name, cid=champion_id))
            else:
                logging.error("ERROR: Generic error in league_client.get_champion_mastery()")
            logging.error(e)

    def get_current_game_info(self, summoner_name:str):
        """
        Get the current game information of a summoner
        
        :param str:summoner_name    Sanitized summoner name
        :return str:                Output message to write to text channel
        """
        summoner_id = self._get_summoner_id(summoner_name)
        url = self.riot_host + "/lol/spectator/v4/active-games/by-summoner/{sid}".format(sid=summoner_id)
        response = requests.get(url, headers=self.headers)
        try:
            json_object = json.loads(response.text)
            return "**{summoner}** is **{time}** minutes into a **{mode}** game".format(
                summoner=summoner_name,
                time=self.seconds_to_time(json_object["gameLength"]),
                mode=self.queue_ids.get(json_object["gameQueueConfigId"], "???")
            )
        except Exception as e:
            if response.status_code != 200:
                logging.error("ERROR: Response code {} in league_client.get_current_game_info()".format(response.status_code))
                logging.error("Summoner: {s} ({sid})".format(s=summoner_name, sid=summoner_id))
            else:
                logging.error("ERROR: Generic error in league_client.get_current_game_info()")
            logging.error(e)


    def _get_summoner_id(self, summoner_name:str):
        """
        Get a summoner's ID by name
        
        :param str:summoner_name    Sanitized summoner name
        :return str:                Summoner ID
        """
        url = self.riot_host + "/lol/summoner/v4/summoners/by-name/" + summoner_name
        response = requests.get(url, headers=self.headers)
        try:
            json_object = json.loads(response.text)
            return json_object["id"]
        except Exception as e:
            if response.status_code != 200:
                logging.error("ERROR: Response code {} in league_client.get_summoner_id()".format(response.status_code))
            else:
                logging.error("ERROR: Generic error in league_client.get_summoner_id()")
                logging.error(e)

    def _get_champion_id(self, champion_name:str):
        """
        Get a champion's ID by name
        
        :param str:summoner_name    Sanitized summoner name
        :return str:                Summoner ID
        """
        champion_name = champion_name.replace(" ", "")
        url = self.ddragon_host + "/cdn/6.24.1/data/en_US/champion/{name}.json".format(name=champion_name)
        response = requests.get(url)
        try:
            json_object = json.loads(response.text)
            return json_object["data"][champion_name]["key"]
        except Exception as e:
            if response.status_code != 200:
                logging.error("ERROR: Response code {} in league_client.get_champion_id()".format(response.status_code))
            else:
                logging.error("ERROR: Generic error in league_client.get_champion_id()")
            logging.error(e)

    def seconds_to_time(self, seconds:int):
        """
        Convert seconds to a human-readable time format (MM:SS)

        :param int:seconds  Seconds to convert
        :return str:        Time in MM:SS (None on failure)
        """
        try:
            seconds = int(seconds)
        except ValueError:
            return "Unknown"
        except TypeError:
            return "Unknown"
        except Exception as e:
            logging.error(e)
            return "Unknown"

        sec = timedelta(seconds=seconds)
        d = datetime(1,1,1) + sec
        return f"{d.minute}:{d.second:02}"

    def generate_headers(self):
        return {
            "Origin": "https://developer.riotgames.com",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": self.api_key,
            "Accept-Language": "en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
    
    def _get_api_key(self, path):
        with open(path) as f:
            json_object = json.load(f)
        return json_object["RIOT_API_KEY"]
