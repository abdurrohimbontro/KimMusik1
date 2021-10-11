import asyncio

from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["join", f"join@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>• **saya tidak memiliki izin:**\n\n» __Tambah Pengguna__</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "asisten Musik"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "🤖: Saya bergabung untuk memutar musik di vcg"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>✅ userbot susah bergabung ke obrolan</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n\n Pengguna {user.first_name} tidak dapat bergabung dengan grup Anda karena banyaknya permintaan bergabung untuk userbot."
            "\n\atau secara manual menambahkan asisten ke Grup Anda dan coba lagi</b>",
        )
        return
    await message.reply_text(
        f"<b>✅ userbot sukses bergabung ke grup</b>",
    )


@Client.on_message(
    command(["leave", f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def rem(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ userbot berhasil Meninggalkan grup")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>pengguna tidak dapat meninggalkan grup Anda, mungkin menunggu lama.\n\atau secara manual mengeluarkan saya dari grup Anda</b>"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **userbot** Meninggalkan semua grup")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Userbot Meninggalkan semua grup...\n\nLeft: {left} chats.\ngagal: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"Userbot pergi...\n\nLeft: {left} chats.\ngagal: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Left {left} chats.\ngagal {failed} chats."
    )


@Client.on_message(
    command(["joinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply(
            "❌ `NOT_LINKED`\n\n• **Userbot tidak dapat memutar musik, karena grup belum terhubung ke Channel**"
        )
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>• **saya tidak memiliki izin:**\n\n» __Tambah Pengguna__</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "asisten"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "🤖: Saya bergabung ke grup untuk memutar musik di vcg"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>✅ userbot sudah bergabung ke Channel</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑\n\n**userbot tidak dapat bergabung ke Channel** karena banyaknya permintaan bergabung untuk userbot, pastikan userbot tidak dilarang di Channel."
            f"\n\atau tambahkan @{ASSISTANT_NAME} secara manual ke Channel Anda dan coba lagi</b>",
        )
        return
    await message.reply_text(
        "<b>✅ userbot berhasil bergabung ke channel</b>",
    )
