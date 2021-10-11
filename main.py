import requests
from pyrogram import Client as Bot

from callsmusic import run
from config import API_HASH, API_ID, BG_IMAGE, BOT_TOKEN
from KimMusik import __version__

response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="KimMusik"),
)

print(f"[INFO]: 🍂 ᏦᎥᎷ 🍂 Ꮙ{__version__} 𝐓𝐄𝐋𝐀𝐇 𝐀𝐊𝐓𝐈𝐅")

bot.start()
run()
