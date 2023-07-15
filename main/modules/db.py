import asyncio
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from config import MONGO_DB_URI

print("[INFO]: STARTING MONGO DB CLIENT")
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.autoanime

animedb = db.animes
uploadsdb = db.uploads
user_data = db['users']

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def get_animesdb(): 
    anime_list = []
    async for title in animedb.find():
        anime_list.append(title)
    return anime_list

async def save_animedb(title,data): 
    data = await animedb.insert_one({"name": title, "data": data})
    return
  
async def del_anime(title): 
    data = await animedb.delete_one({"name": title})
    return

async def get_uploads(): 
    anime_list = []
    async for title in uploadsdb.find():
        anime_list.append(title)
    return anime_list

async def save_uploads(title): 
    data = await uploadsdb.insert_one({"name": title})
    return
