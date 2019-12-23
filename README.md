# GGWP
A discord bot that allows users to fetch their League of Legends stats

**Status:** Development, not stable
### Installation
```batch
mkdir ggwp-bot
cd ggwp-bot
git clone https://github.com/ttamre/ggwp.git
```

## Usage
### Running the bot
Keep a file named `secrets.json` in the root project directory and structure it as follows
```json
{
    "RIOT_API_KEY": "YOUR_RIOT_DEVELOPER_API_KEY",
    "DISCORD_BOT_TOKEN": "YOUR_DISCORD_DEVELOPER_BOT_TOKEN"
}
```

Then, enter the following in the terminal (with python3)
```bash
python bot.py
```

### Commands
```
./rank summoner_name                    # Get summoner rank
./mastery summoner_name champion_name   # Get summoner mastery rank for a champion
./game summoner_name                    # Get game data for a summoner that's in game
```

## Contributing
Please email me at ttamre@ualberta.ca for details on code of conduct, and the process for submitting pull requests.

## Authors
* **Tem Tamre** - *Project Lead/Owner* - [Github](https://github.com/ttamre)

See also the list of [contributors](https://github.com/ttamre/ggwp/graphs/contributors) who participated in this project.

## License
This project is licensed under the GNU General Public License - see [LICENSE](LICENSE) for more details
