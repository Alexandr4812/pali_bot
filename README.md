# Pāli canon Telegarm bot

## About
Bot created to read some short suttas with Telegram. For now there are charged
few canon sections in Russian.

YAML formatted data files had been created with
[scrapper](https://gitlab.com/bergentroll/theravada-ru-sutta-scrapper).


## Installation
```bash
python3 -m venv env
. env/bin/activate
pip3 install -e .
```

## Usage
- Create a bot with [BotFather](https://t.me/BotFather)
- Get the bot token
- Set the token in the [config.py](./config.py)

Run with:
```bash
. env/bin/activate
pali_bot
```

## TODO
- Suggestion: `/*_sutta N` command to get n-th sutta from a section
