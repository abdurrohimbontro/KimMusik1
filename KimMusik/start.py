import os
import asyncio
from time import time
from sys import version_info
from datetime import datetime

from pyrogram import Client, filters
from pyrogram import __version__ as __pyro_version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BOT_NAME, BOT_USERNAME, GROUP_SUPPORT, OWNER_NAME, UPDATES_CHANNEL, ALIVE_NAME, ALIVE_IMG
from helpers.decorators import sudo_users_only
from helpers.filters import command
from KimMusik import __version__


__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>โจ **Assalamualaikum, {message.from_user.mention} selamat datang di bot saya** \n
โ๏ธ **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) akan membantu anda memutar musik di vcg Telegram anda**

๐ **Cari tahu semua perintah Bot dan cara kerjanya dengan mengklik\nยป ๐ Tombol perintah**

๐ญ **Untuk mengetahui cara menggunakan bot ini, silakan klik ยป โ Tombol panduan dasar**

By [๐๐ฒ๐ถ.๐ฒ๐ญ](https://t.me.warga_pati)
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "โ TAMBAHKAN KE GRUP โ",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("โ panduan dasar", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("๐ Perintah", callback_data="cbcmds"),
                    InlineKeyboardButton("๐ OWNER", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "๐ข Grup Random", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "๐ฃ Channel", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "๐งฐ Penghuni surga ", url="https://t.me/rakyat pati"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    
    keyboard=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "๐ข Group", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "๐ฃ Channel", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ]
            ]
    )
    
    alive = f"**Assalamualaikum,hai {message.from_user.mention}, perkenalkan saya adalah {BOT_NAME}**\n\n๐ฅ Bot bekerja normal\n๐บ My Master: [{ALIVE_NAME}](https://t.me/{OWNER_NAME})\n๐งฉ Versi Bot : `v{__version__}`\n๐ฑ Versi Pyrogram : `{__pyro_version__}`\n๐ฒ Versi Python : `{__python_version__}`\n๐ waktu aktif : `{uptime}`\n\n**Terima kasih telah Menambahkan saya di sini, untuk memutar musik di suara Grup Anda โค๏ธ\n by [๐๐ฒ๐ถ.๐ฒ๐ญ](https://t.me.warga_pati) **"
    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(
    command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>๐๐ป **Hallo** {message.from_user.mention()}</b>

**Silakan tekan tombol di bawah ini untuk membaca penjelasan dan melihat daftar perintah yang tersedia**

โ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="๐ญ CARA MENGGUNAKAN SAYA", callback_data="cbguide")]]
        ),
    )


@Client.on_message(
    command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>๐ฟ๏ธ Hallo {message.from_user.mention} Selamat datang di Menu bantuan</b>

**di menu ini anda bisa membuka beberapa menu perintah yang tersedia, di setiap menu perintah juga ada penjelasan singkat masing-masing perintah**

โ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("๐ prnth Dasar", callback_data="cbbasic"),
                    InlineKeyboardButton("๐ prnth Canggih", callback_data="cbadvanced"),
                ],
                [
                    InlineKeyboardButton("๐ prnth Admin", callback_data="cbadmin"),
                    InlineKeyboardButton("๐ prnth Sudo", callback_data="cbsudo"),
                ],
                [InlineKeyboardButton("๐ prnth Owner", callback_data="cbowner")],
                [InlineKeyboardButton("๐ prnth Fun", callback_data="cbfun")],
            ]
        ),
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("๐")
    await m_reply.edit_text("๐")
    await m_reply.edit_text("๐")
    await m_reply.edit_text("๐")
    await m_reply.edit_text("๐")
    await m_reply.edit_text("๐")
    await asyncio.sleep(3)
    await m_reply.edit_text("๐ แฆแฅแท.แฅแด ๐")
    await asyncio.sleep(3)
    await m_reply.edit_text("๐")
    await asyncio.sleep(3)
    delta_ping = time() - start
    await m_reply.edit_text("๐ `pong`\n" f"๐ฒ๐จ ping `{delta_ping * 1000:.3f} ms`๐ฎ๐ฉ\n ๐๐ฒ๐ถ.id")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "๐ค bot status:\n"
        f"โข **waktu aktif:** `{uptime}`\n"
        f"โข **mulai aktif:** `{START_TIME_ISO}`"
    )
