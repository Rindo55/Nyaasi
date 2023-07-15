
import asyncio
import time
import aiohttp
import requests
import aiofiles
import sys

from main.modules.compressor import compress_video

from main.modules.utils import episode_linker, get_duration, get_epnum, status_text, get_filesize, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from main.modules.uploader import upload_video
from main.modules.thumbnail import generate_thumbnail

import os

from main.modules.db import del_anime, save_uploads

from main.modules.downloader import downloader

from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name

from config import INDEX_USERNAME, UPLOADS_USERNAME, UPLOADS_ID, INDEX_ID, PROGRESS_ID, LINK_ID

from main import app, queue, status

from pyrogram.errors import FloodWait

from pyrogram import filters

from main.inline import button1

status: Message

async def tg_handler():

    while True:

        try:

            if len(queue) != 0:

                i = queue[0]  

                i = queue.pop(0)

                id = await start_uploading(i)

                await del_anime(i["title"])

                await save_uploads(i["title"])

                await asyncio.sleep(30)

            else:                

                if "Idle..." in status.text:

                    try:

                        await status.edit(await status_text("Idle..."),reply_markup=button1)

                    except:

                        pass

                await asyncio.sleep(30)

                

        except FloodWait as e:

            flood_time = int(e.x) + 5

            try:

                await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

            except:

                pass

            await asyncio.sleep(flood_time)

        except:

            pass

            

async def start_uploading(data):

    try:

        title = data["title"]
        link = data["link"]
        size = data["size"]
        nyaasize = data["size"]
        subtitle = data["subtitle"]
        vlink = data['vlink']
        dlink = data['dlink']
        trust = data['trust']
        cid = data['categoryid']
        category = data['category']
        magnet = "https://nyaasi.herokuapp.com/nyaamagnet/urn:btih:" + link
        clink = "https://nyss.si/?c=" + "cid"
        if trust=="Yes":
            trust="#trusted"
        else:
            trust=""
        xtext=f"**{title}**" + "\n" + "{size}" + " | " + f"[Download]({dlink})" + " | " + f"[View]({vlink})" + " | " + "{trust}" + "\n" + f"[#C{cid} {category}](clink)" + "\n" + "\n" + f"[🔗 Magnet](magnet)"
        KAYO_ID = -1001900103251
        untext = await app.send_message(
                      chat_id=KAYO_ID,
                      text=xtext
                  ) 

    except FloodWait as e:

        flood_time = int(e.x) + 5

        try:

            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

        except:

            pass

        await asyncio.sleep(flood_time)

    return id
