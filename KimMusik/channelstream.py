# Copyright (C) 2021 Kim official

import os
from os import path

import requests
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch

from callsmusic import callsmusic
from callsmusic.callsmusic import client as USER
from callsmusic.queues import queues
from config import que, DURATION_LIMIT, BOT_USERNAME, UPDATES_CHANNEL as updateschannel
from converter.converter import convert
from downloaders import youtube
from KimMusik.play import cb_admin_check, generate_cover
from helpers.filters import command, other_filters
from helpers.admins import get_administrators
from helpers.decorators import authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_file_name

chat_id = None


@Client.on_message(command(["cplaylist", f"cplaylist@{BOT_USERNAME}"]) & other_filters)
async def playlist(client, message):
    try:
        lel = await client.get_chat(message.chat.id)
        lol = lel.linked_chat.id
    except:
        message.reply("❌ `NOT_LINKED`\n\n• **Userbot tidak dapat memutar musik, karena grup belum terhubung ke Channel**")
        return
    global que
    queue = que.get(lol)
    if not queue:
        await message.reply_text("pemain tidak terhubung ke vcg")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "💡 **Sedang diputar** di {}".format(lel.linked_chat.title)
    msg += "\n- " + now_playing
    msg += "\n- Req by " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Antrian**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n- {name}"
            msg += f"\n- Req by {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        # if chat.id in active_chats:
        stats = "⚙️ pengaturan **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Volume : {}%\n".format(vol)
            stats += "Musik dimainkan : `{}`\n".format(len(que))
            stats += "Sedang diputar : **{}**\n".format(queue[0][0])
            stats += "Requested by : {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "cleave"),
                InlineKeyboardButton("⏸", "cpuse"),
                InlineKeyboardButton("▶️", "cresume"),
                InlineKeyboardButton("⏭", "cskip"),
            ],
            [
                InlineKeyboardButton("📖 PLAY-LIST", "cplaylist"),
            ],
            [InlineKeyboardButton("✖️ Close", "ccls")],
        ]
    )
    return mar


@Client.on_message(command(["ccurent", f"ccurent@{BOT_USERNAME}"]) & other_filters)
async def ee(client, message):
    try:
        lel = await client.get_chat(message.chat.id)
        lol = lel.linked_chat.id
        conv = lel.linked_chat
    except:
        await message.reply("❌ `NOT_LINKED`\n\n• **Userbot tidak dapat memutar musik, karena grup belum terhubung ke Channel**")
        return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("Mohon hidupkan vcg dulu !")


@Client.on_message(command(["cplayer", f"cplayer@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def settings(client, message):
    playing = None
    try:
        lel = await client.get_chat(message.chat.id)
        lol = lel.linked_chat.id
        conv = lel.linked_chat
    except:
        await message.reply("❌ `NOT_LINKED`\n\n• **Userbot tidak dapat memutar musik, karena grup belum terhubung ke Channel**")
        return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("Mohon hidupkan vcg dulu!")


@Client.on_callback_query(filters.regex(pattern=r"^(cplaylist)$"))
async def p_cb(b, cb):
    global que
    try:
        lel = await client.get_chat(cb.message.chat.id)
        lol = lel.linked_chat.id
        conv = lel.linked_chat
    except:
        return
    que.get(lol)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(lol)
        if not queue:
            await cb.message.edit("pemain tidak terhubung ke vcg")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Sedang diputar** in {}".format(conv.title)
        msg += "\n- " + now_playing
        msg += "\n- Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Antrian**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req by {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(cplay|cpause|cskip|cleave|cpuse|cresume|cmenu|ccls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
        try:
            lel = await b.get_chat(cb.message.chat.id)
            lol = lel.linked_chat.id
            conv = lel.linked_chat
            chet_id = lol
        except:
            return
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "cpause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("obrolan tidak terhubung", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("musik dijeda")
            await cb.message.edit(updated_stats(conv, qeue), reply_markup=r_ply("play"))

    elif type_ == "cplay":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("obrolan tidak terhubung", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("musik dilanjutkan")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "cplaylist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("pemain tidak terhubung ke vcg")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "💡 **Sedang diputar** di {}".format(cb.message.chat.title)
        msg += "\n- " + now_playing
        msg += "\n- Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Antrian**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req by {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "cresume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("obrolan tidak terhubung atau seedang bermain", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("musik dilanjutkan!")
    elif type_ == "cpuse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("obrolan tidak terhubung atau telah dijeda", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("music dijeda")
    elif type_ == "ccls":
        await cb.answer("menu ditutup")
        await cb.message.delete()

    elif type_ == "cmenu":
        stats = updated_stats(conv, qeue)
        await cb.answer("menu dibuka")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "cleave"),
                    InlineKeyboardButton("⏸", "cpuse"),
                    InlineKeyboardButton("▶️", "cresume"),
                    InlineKeyboardButton("⏭", "cskip"),
                ],
                [
                    InlineKeyboardButton("📖 PLAY-LIST", "cplaylist"),
                ],
                [InlineKeyboardButton("✖️ Close", "ccls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)
    elif type_ == "cskip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("obrolan tidak terhubung", show_alert=True)
        else:
            queues.task_done(chet_id)

            if queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("» Tidak ada lagi daftar putar\n» userbot Meninggalkan vcg")
            else:
                callsmusic.pytgcalls.change_stream(chet_id, queues.get(chet_id)["file"])
                await cb.answer("Skipped")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    "⏭ **Anda melewati ke lagu berikutnya**"
                )

    else:
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("memutuskan musik player dari vcg")
        else:
            await cb.answer("obrolan tidak terhubung", show_alert=True)


@Client.on_message(command(["cplay", f"cplay@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def play(_, message: Message):
    global que
    lel = await message.reply("🔎 **Mencari...**")

    try:
        conchat = await _.get_chat(message.chat.id)
        conv = conchat.linked_chat
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("❌ `NOT_LINKED`\n\n• **Userbot tidak dapat memutar musik, karena grup belum terhubung ke Channel**")
        return
    try:
        administrators = await get_administrators(conv)
    except:
        await message.reply("Saya bukan admin di Channel ini, Maaf")
    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "💡 Mohon tambahkan dulu userbot ke Channel",
                    )

                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "💡 Jadikan saya admin dulu",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "✅ **userbot Berhasil bergabung ke grup**",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 Flood Wait Error 🔴 \nPengguna {user.first_name} tidak dapat bergabung dengan saluran Anda karena banyaknya permintaan untuk bot pengguna! Pastikan pengguna tidak dilarang di grup."
                        "\n\nAtau tambahkan asisten ke Grup Anda secara manual dan coba lagi</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"❌ `NOT_IN_GROUP`\n\n» **Userbot tidak ada dalam grup ini, bot tidak dapat memutar musik.**"
        )
        return
    message.from_user.id
    text_links = None
    message.from_user.first_name
    await lel.edit("🎧 **Menyiapkan...**")
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == "url"]
        text_links = [entity for entity in entities if entity.type == "text_link"]
    else:
        urls = None
    if text_links:
        urls = True
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ musik dengan durasi lebih dari `{DURATION_LIMIT}` menit tidak dapat bermain"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📋 Menu", callback_data="cmenu"),
                    InlineKeyboardButton("✖️ Close", callback_data="ccls"),
                ],
                [
                    InlineKeyboardButton(
                        text="📣 Channel", url=f"https://t.me/{updateschannel}"
                    )
                ],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/aadf8336ee9f537a179e9.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        message.from_user.first_name
        await generate_cover(title, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🎵 ***Mengirim audio...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:60]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["duration"]
            results[0]["url_suffix"]
            results[0]["views"]

        except Exception as e:
            await lel.edit("Maaf 😟 **tidak dapat menemukan lagu yang Anda minta**\n\n» **harap berikan nama lagu yang benar atau sertakan juga nama artis**")
            print(str(e))
            return
        dlurl = url
        dlurl = dlurl.replace("youtube", "youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📋 Menu", callback_data="cmenu"),
                    InlineKeyboardButton("✖️ Close", callback_data="ccls"),
                ],
                [
                    InlineKeyboardButton(
                        "📣 Channel", url=f"https://t.me/{updateschannel}"
                    )
                ],
            ]
        )
        message.from_user.first_name
        await generate_cover(title, thumbnail)
        file_path = await convert(youtube.download(url))
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("🎵 **Mengirim audio...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:60]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["duration"]
            results[0]["url_suffix"]
            results[0]["views"]

        except Exception as e:
            await lel.edit("Maaf 😟 **tidak dapat menemukan lagu yang Anda minta**\n\n» **harap berikan nama lagu yang benar atau sertakan juga nama artis**")
            print(str(e))
            return

        dlurl = url
        dlurl = dlurl.replace("youtube", "youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📋 Menu", callback_data="cmenu"),
                    InlineKeyboardButton("✖️ Close", callback_data="ccls"),
                ],
                [
                    InlineKeyboardButton(
                        "📣 Channel", url=f"https://t.me/{updateschannel}"
                    )
                ],
            ]
        )
        message.from_user.first_name
        await generate_cover(title, thumbnail)
        file_path = await convert(youtube.download(url))
    chat_id = chid
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"💡 **Musik ditambahkan»** `{position}`\n\n🏷 **Nama:** [{title[:35]}...]({url})\n⏱ **Durasi:** `{duration}`\n🎧 **Request by:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = chid
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **Nama:** [{title[:60]}]({url})\n⏱ **Durasi:** `{duration}`\n💡 **Status:** `Playing`\n"
            + f"🎧 **Request by:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
