from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues
from converter import converter
from downloaders import youtube

from config import DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name

@Client.on_message(command("fplay") & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name



    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲.")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=f"https://telegra.ph/file/46c460685ec153d93e3cf.jpg",
        caption=f"#⃣ 𝐘𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐬𝐨𝐧𝐠 **queued** 𝐚𝐭 𝐩𝐨𝐬𝐢𝐭𝐢𝐨𝐧 {position}!")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"https://telegra.ph/file/46c460685ec153d93e3cf.jpg",
        caption=f"▶️ **Playing** 𝐡𝐞𝐫𝐞 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐛𝐲 {costumer}"
        )
        return await lel.delete()
