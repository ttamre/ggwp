# GGWP
[![CircleCI](https://circleci.com/gh/ttamre/ggwp/tree/master.svg?style=svg)](https://circleci.com/gh/ttamre/ggwp/tree/master)

A locally-hosted discord bot that allows users to fetch their League of Legends stats

**Status:** Stable

### Installation
```bash
git clone https://github.com/ttamre/ggwp.git
```

## Usage
### Running the bot
Keep a file named `secrets.json` in the root project directory and structure it as follows
```json
{
    "RIOT_API_KEY": "YOUR_RIOT_DEVELOPER_API_KEY",
    "DISCORD_BOT_TOKEN": "YOUR_DISCORD_DEVELOPER_BOT_TOKEN",
    "OWNERS": ["user#0000"]
}
```

Then run
```bash
python3 ggwp.py
```

### Commands
```
./rank summoner_name                    # Get summoner rank
./mastery summoner_name champion_name   # Get summoner mastery rank for a champion
./game summoner_name                    # Get game data for a summoner that's in game
./help                                  # View all available commands
./exit                                  # Exit the bot (must be an owner to use this)
```

## License
This project is licensed under the GNU General Public License - see [LICENSE](LICENSE) for more details
