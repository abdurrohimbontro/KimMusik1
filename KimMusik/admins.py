# Copyright (C) 2021 Kim official

from asyncio import QueueEmpty

from callsmusic import callsmusic
from callsmusic.queues import queues
from config import BOT_USERNAME, que
from cache.admins import admins
from KimMusik.play import cb_admin_check
from helpers.channelmusic import get_chat_id
from helpers.dbtools import delcmd_is_on, delcmd_off, delcmd_on, handle_user_status
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


# Back Button
BACK_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ кємвαℓι", callback_data="cbback")]]
)

# @Client.on_message(filters.text & ~filters.private)
# async def delcmd(_, message: Message):
#    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!") or message.text.startswith("."):
#        await message.delete()
#    await message.continue_propagation()

# remove the ( # ) if you want the auto del cmd feature is on


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ Bot **berhasil di mulai ulang**\n✅ **Daftar Admin diperbarui**"
    )


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "🎮 **ini adalah menu kontrol bot :**",
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
                [InlineKeyboardButton("✖️ ¢ℓσѕє", callback_data="close")],
            ]
        ),
    )


@Client.on_message(command(["pause", f"pause@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❌ **tidak ada musik yang sedang diputar**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text(
            "⏸ **Musik dijeda**\n\n• **untuk melanjutkan pemutaran kembali gunakan **\n» perintah `/resume`."
        )


@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❌ **Tidak ada musik terjeda**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            "▶️ **Musik dilanjutkan**\n\n• **untuk menjeda pemutaran gunakan**\n» perintah`/pause`"
        )


@Client.on_message(command(["end", f"end@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❌ **Tidak ada musik yang sedang diputar**")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("😡 **Kenapa dimatikan**")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❌ **Tidak ada musik yang sedang diputar**")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(chat_id, queues.get(chat_id)["file"])

    qeue = que.get(chat_id)
    if qeue:
        qeue.pop(0)
    if not qeue:
        return
    await message.reply_text("⏭ **melewati ke lagu berikutnya**")


@Client.on_message(command(["auth", f"auth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("💬 balas ke pesan untuk mengotorisasi pengguna")
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "🟢 Pengguna di otorisasi.\n\nmulai sekarang Pengguna dapat menggunakan perintah admin"
        )
    else:
        await message.reply("✅ pengguna sudah diotorisasi")


@Client.on_message(command(["deauth", f"deauth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("💬 balas ke pesan untuk membatalkan otorisasi pengguna")
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "🔴 Otorisasi pengguna dibatalkan\n\nMulai sekarang Pengguna tidak dapat menggunakan perintah admin")
    else:
        await message.reply("✅ Otorisasi pengguna sudah dibatalkan")

# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Baca pesan /help untuk mengetahui cara menggunakan perintah ini"
)
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            return await message.reply_text("✅ Sudah di aktivasi")
        await delcmd_on(chat_id)
        await message.reply_text("🟢 aktivasi sukses")
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("🔴 penonaktifan sukses")
    else:
        await message.reply_text(
            "Baca pesan /help untuk mengetahui cara menggunakan perintah ini"
        )


# music player callbacks (control by buttons feature)


@Client.on_callback_query(filters.regex("cbpause"))
@cb_admin_check
async def cbpause(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if (query.message.chat.id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[query.message.chat.id] == "paused"
    ):
        await query.edit_message_text(
            "❌ **Tidak ada musik yang sedang diputar**", reply_markup=BACK_BUTTON
        )
    else:
        callsmusic.pytgcalls.pause_stream(query.message.chat.id)
        await query.edit_message_text(
            "⏸ pemutaran musik telah dijeda", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbresume"))
@cb_admin_check
async def cbresume(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if (query.message.chat.id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[query.message.chat.id] == "resumed"
    ):
        await query.edit_message_text(
            "❌ **tidak ada musik yang dijeda**", reply_markup=BACK_BUTTON
        )
    else:
        callsmusic.pytgcalls.resume_stream(query.message.chat.id)
        await query.edit_message_text(
            "▶️ pemutaran musik telah dilanjutkan", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbend"))
@cb_admin_check
async def cbend(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text(
            "❌ **tidak ada musik yang sedang diputar**", reply_markup=BACK_BUTTON
        )
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        await query.edit_message_text(
            "✅ antrian musik telah dihapus dan berhasil meninggalkan obrolan suara",
            reply_markup=BACK_BUTTON,
        )


@Client.on_callback_query(filters.regex("cbskip"))
@cb_admin_check
async def cbskip(_, query: CallbackQuery):
    global que
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text(
            "❌ **tidak ada musik yang sedang diputar**", reply_markup=BACK_BUTTON
        )
    else:
        queues.task_done(query.message.chat.id)

        if queues.is_empty(query.message.chat.id):
            callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                query.message.chat.id, queues.get(query.message.chat.id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        qeue.pop(0)
    if not qeue:
        return
    await query.edit_message_text(
        "⏭ **Melewati ke lagu berikutnya**", reply_markup=BACK_BUTTON
    )
