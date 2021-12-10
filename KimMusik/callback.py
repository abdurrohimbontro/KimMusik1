# (C) 2021 Kim official

from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from KimMusik.play import cb_admin_check
from helpers.decorators import authorized_users_only
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>✨ **Assalamualaikum ,Selamat datang di Bot kami, saya {query.message.from_user.mention} !** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) memungkinkan Anda memutar musik di grup melalui obrolan suara Telegram **

💡 **Cari tahu semua perintah Bot dan cara kerjanya dengan mengklik\n» 📚 tombol perintah!**

❔ **Untuk mengetahui cara menggunakan bot ini, silakan klik » 📘 tombol Pandan dasar**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Tambahkan saya ke grup ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("📘 Basic Guide", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 perintah", callback_data="cbcmds"),
                    InlineKeyboardButton("💝 KIM", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 Grup Random", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Channel", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "💝 Pacar kamu ", url="https://t.me/rakyat_pati"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Assalamualaikum, Selamat datang di menu help </b>

» **di menu ini Anda dapat membuka beberapa perintah yang tersedia di menu, di setiap menu perintah juga ada penjelasan singkat masing-masing perintah**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📚 Basic Cmd", callback_data="cbbasic"),
                    InlineKeyboardButton("📕 Advanced Cmd", callback_data="cbadvanced"),
                ],
                [
                    InlineKeyboardButton("📘 Admin Cmd", callback_data="cbadmin"),
                    InlineKeyboardButton("📗 Sudo Cmd", callback_data="cbsudo"),
                ],
                [InlineKeyboardButton("📙 Owner Cmd", callback_data="cbowner")],
                [InlineKeyboardButton("🏡 kembali ke Help", callback_data="cbguide")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 ini adalah perintah dasar</b>

🎧 [ GROUP VC CMD ]

/play (nama lagu) - memutar lagu dari youtube
/ytp (nama lagu) - putar lagu langsung dari youtube
/stream (membalas audio) - memutar lagu menggunakan file audio
/playlist - tampilkan daftar lagu dalam antrian
/song (nama lagu) - download lagu dari youtube
/search (nama video) - cari video dari youtube secara detail
/vsong (nama video) - unduh video dari youtube detail
/lyric - (nama lagu) lirik scrapper
/vk (nama lagu) - unduh lagu dari mode inline

🎧 [ CHANNEL VC CMD ]

/cplay - streaming musik di obrolan suara saluran
/cplayer - tampilkan lagu dalam streaming
/cpause - jeda musik streaming
/cresume - melanjutkan streaming yang dijeda
/cskip - lewati streaming ke lagu berikutnya
/cend - mengakhiri streaming musik
/refresh - menyegarkan cache admin
/ubjoinc - undang asisten untuk bergabung ke saluran Anda

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ KEMBALI", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 ini adalah perintah canggih</b>

/start (dalam grup) - lihat status bot hidup
/reload - muat ulang bot dan segarkan daftar admin
/ping - periksa status ping bot
/ uptime - periksa status uptime bot
/id - tampilkan grup/id pengguna & lainnya

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ KEMBALI", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 ini adalah perintah admin </b>

/player - menampilkan status pemutaran musik
/pause - menjeda streaming musik
/resume - melanjutkan musik yang dijeda
/skip - lompat ke lagu berikutnya
/end - hentikan streaming musik
/join - undang userbot bergabung ke grup Anda
/leave - perintahkan userbot untuk keluar dari grup Anda
/auth - pengguna resmi untuk menggunakan bot musik
/deauth - tidak sah untuk menggunakan bot musik
/control - buka panel pengaturan pemutar
/delcmd (on | off) - aktifkan / nonaktifkan fitur del cmd
/musicplayer (on / off) - nonaktifkan / aktifkan pemutar musik di grup Anda

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ KEMBALI", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 ini adalah perintah sudo</b>

/leaveall - perintahkan asisten untuk keluar dari semua grup
/stats - tampilkan statistik bot
/rmd - hapus semua file yang diunduh

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ KEMBALI", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 perintah khusus owner</b>

/stats - tampilkan statistik bot
/broadcast - mengirim pesan siaran dari bot
/block (id pengguna - durasi - alasan) - blokir pengguna untuk menggunakan bot Anda
/unblock (id pengguna - alasan) - buka blokir pengguna yang Anda blokir karena menggunakan bot Anda
/blocklist - menunjukkan daftar pengguna yang diblokir karena menggunakan bot Anda

📝 Catatan: semua perintah yang dimiliki oleh bot ini dapat dijalankan oleh pemilik bot tanpa terkecuali.

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ KEMBALI", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ BAGAIMANA CARA MENGGUNAKAN BOT INI :

1.) pertama, tambahkan saya ke grup Anda.
2.) kemudian promosikan saya sebagai admin dan berikan semua izin kecuali admin anonim.
3.) tambahkan @{ASSISTANT_NAME} ke grup Anda atau ketik /userbotjoin untuk mengundangnya.
4.) nyalakan obrolan suara terlebih dahulu sebelum mulai memutar musik.

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📚 Daftar perintah", callback_data="cbhelp")],
                [InlineKeyboardButton("✖️ ¢ℓσѕє", callback_data="close")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
@cb_admin_check
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        "**💡 Ini adalah menu perintah bot :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏸ ραυѕє", callback_data="cbpause"),
                    InlineKeyboardButton("▶️ яєѕυмє", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("⏩ ѕкιρ", callback_data="cbskip"),
                    InlineKeyboardButton("⏹ ѕтσρ", callback_data="cbend"),
                ],
                [InlineKeyboardButton("⛔ αηтι ¢м∂", callback_data="cbdelcmds")],
                [InlinekeyboardButton("✖️ ¢ℓσѕє", callback_data="close")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
@cb_admin_check
@authorized_users_only
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>this is the feature information :</b>
        
**💡 Fitur:** hapus setiap perintah yang dikirim oleh pengguna untuk menghindari spam di grup !

❔ penggunaan:**

 1️⃣ untuk mengaktifkan fitur:
     » ketik `/delcmd on`
    
 2️⃣  untuk mematikan Fitur:
     » ketik `/delcmd off`
      
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ KEMBALI", callback_data="cbback")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Assalamualaikum, Selamat datang di menu help</b>

» **di menu ini anda bisa membuka beberapa menu perintah yang tersedia, di setiap menu perintah juga ada penjelasan singkat masing-masing perintah**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📚 Basic Cmd", callback_data="cbbasic"),
                    InlineKeyboardButton("📕 Advanced Cmd", callback_data="cbadvanced"),
                ],
                [
                    InlineKeyboardButton("📘 Admin Cmd", callback_data="cbadmin"),
                    InlineKeyboardButton("📗 Sudo Cmd", callback_data="cbsudo"),
                ],
                [InlineKeyboardButton("📙 Owner Cmd", callback_data="cbowner")],
                [InlineKeyboardButton("⬅️ KEMBALI", callback_data="cbstart")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ BAGAIMANA CARA MENGGUNAKAN BOT INI:

1.) pertama, tambahkan saya ke grup Anda.
2.) kemudian promosikan saya sebagai admin dan berikan semua izin kecuali admin anonim.
3.) tambahkan @{ASSISTANT_NAME} ke grup Anda atau ketik /userbotjoin untuk mengundangnya.
4.) nyalakan obrolan suara terlebih dahulu sebelum mulai memutar musik.

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ KEMBALI", callback_data="cbstart")]]
        ),
    )
