import asyncio
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1

def trim_link(vlink: str):
    vlink = vlink.replace("download", "view")
    vlink = vlink.replace(".torrent", "")
    return vlink
def parse():
    a = feedparser.parse("https://siftrss.com/f/1LNyVoo9RP")
    b = a["entries"]
    data = []    

    for i in b:
        item = {}
        item['title'] = (i['title'])
        item['dlink'] = (i['link'])
        item['vlink'] = trim_link(i['link'])
        item['size'] = i['nyaa_size']   
        item['link'] = i['nyaa_infohash']
        item['categoryid'] = i['nyaa_categoryid']
        item['category'] = i['nyaa_category']
        item['trust'] = i['nyaa_trusted']
        item['remake'] = i['nyaa_remake']
        data.append(item)
    data.reverse()
    return data

async def auto_parser():
    while True:

        rss = parse()
        data = await get_animesdb()
        uploaded = await get_uploads()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])
        
        for i in rss:
            if i["title"] not in uanimes and i["title"] not in saved_anime:
                if ".mkv" in i["title"] or ".mp4" in i["title"]:
                    title = i["title"]
                    await save_animedb(title,i)

        data = await get_animesdb()
        for i in data:
            if i["data"] not in queue:
                queue.append(i["data"])    
                print("Saved ", i["name"])   

    await asyncio.sleep(30)
