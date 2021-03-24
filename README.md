# cro-chain-checker-telegram-bot
 
> Telegram Bot for monitoring your crypto.org validator node.

---

## Installation
> Requires python >= 3.7.
```bash
$ pip3 install -r requirements.txt
```
_Note: if there are errors, you might have to install or upgrade wheel and setuptools._

### Setup
- Get an `api_id` and `api_hash` from `https://my.telegram.org/`.
- Speak to `@BotFather` on Telegram and acquire a bot API .
- Fill in the information into `config.py`. Admin field is your Telegram user id. Look at next step to retreive it.
- Telegram user id can be retrieved after speaking to your own bot (/start) after following up to the above step.
- Change your constants in `cro-chain-checker-telegram-bot.py`.

### Usage
```bash
python3 cro-chain-checker-telegram-bot.py
```

Send `/amisigning` or `/track` to your bot.
