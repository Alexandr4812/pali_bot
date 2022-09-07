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
- Set the token in the [config.yaml](./config.yaml) or with the `PALI_BOT_TOKEN`
    environment variable

Run with:
```bash
. env/bin/activate
pali_bot
```

Alternative config location may be passed with `--config` flag.
