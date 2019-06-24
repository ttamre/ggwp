#!/usr/bin/env python

"""
File: riot_client.py
Description: Riot games client for the discord bot to use to make API requests

Features
- Get summoner rank         ?
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
    def __init__(self):
        self.riot_host = "https://na1.api.riotgames.com"
        self.ddragon_host = "http://ddragon.leagueoflegends.com"
        self.api_key = self.load_secrets()
        self.headers = self.generate_headers()
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
        return "Rank lookup functionality not yet implemented"

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
            json_object = json.load(response.text)
            print(json.dumps(json_object, indent=2))
            return "{summoner} is {time} minutes into a {mode} game".format(
                summoner=summoner_name,
                time=self.seconds_to_time(json_object["gameLength"]),
                mode=self.queue_ids.get(json_object["gameQueueConfigId"], "???")
            )
        except Exception as e:
            if response.status_code != 200:
                logging.error("ERROR: Response code {} in league_client.get_current_game_info()".format(response.status_code))
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

    def seconds_to_time(self, seconds):
        """
        Convert seconds to a human-readable time format (MM:SS)

        :param int:seconds  Seconds to convert
        :return str:        Time in MM:SS
        """
        sec = timedelta(seconds=seconds)
        d = datetime(1,1,1) + sec
        print("{min}:{sec}".format(min=d.minute, sec=d.second))
        return "{min}:{sec}".format(min=d.minute, sec=d.second)

    def generate_headers(self):
        return {
            "Origin": "https://developer.riotgames.com",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": self.api_key,
            "Accept-Language": "en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
    
    def load_secrets(self):
        with open("secrets.json") as f:
            json_object = json.load(f)
            return json_object["RIOT_API_KEY"]