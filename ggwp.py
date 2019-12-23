import json

from bot import Bot

if __name__ == "__main__":
    with open("secrets.json") as f:
        json_object = json.load(f)
        token = json_object["DISCORD_BOT_TOKEN"]
    bot = Bot()
    bot.run(token)