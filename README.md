# Pali suttas Telegarm bot

## Installation
```bash
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```

## Usage
- Create a bot with [BotFather](https://t.me/BotFather)
- Get the bot token
- Set the token in the [config.py](./config.py)

Run with:
```bash
python3 pali_bot.py
```

## TODO
- Serialize data to JSON or YAML
- Implement setup.py
- ~~Move `*.txt` to `data/`~~
- Buttons menu
- ~~Suggestion: apply some permissive license~~
- Testing: run commands, check no exceptions
- Suggestion: rename commands like `/any`, `/theragatha`...
- Suggestion: automatic tags to easily search messages
- Suggestion: bold title of a sutta
