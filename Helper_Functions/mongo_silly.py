# --------- web imports ---------
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Literal
from bson import ObjectId
import time
import datetime
from datetime import timedelta
from Helper_Functions.end_time import months_to_days

"""
####################################################################
############       THE WHOLE POINT OF THIS       ###################
##############        FILE IS TO HOLD        #######################
#######      HELPER FUNCTIONS AND OTHER VARIABLES       ############
####################################################################
"""

# ---------------------------------------------variables-----------------------------------------------------------------

# ------------- mongo variables -------------
mongo_ids = {
    "name" : ObjectId('64f8d47f827cce7b4ac9d35b'),
    "tier" : ObjectId('64f8bc4d094bdbfc3f7d0050'),
    "curator" : ObjectId('64f8d63592d3fe5849c1ba35'),
    "tasks" : ObjectId('64f8d6b292d3fe5849c1ba37'),
    "user" : ObjectId('64f8bd1b094bdbfc3f7d0051'),
    "unfinished" : ObjectId('650076a9e35bbc49b06c9881')
}
uri = "mongodb+srv://andrewgarcha:KUTo7dCtGRy4Nrhd@ce-cluster.inrqkb3.mongodb.net/?retryWrites=true&w=majority"
mongo_client = AsyncIOMotorClient(uri)
mongo_database = mongo_client['database_name']
collection = mongo_client['database_name']['ce-collection']

# ------------- image icons -------------
ce_mountain_icon = "https://cdn.discordapp.com/attachments/639112509445505046/891449764787408966/challent.jpg"
ce_hex_icon = "https://imgur.com/a/HiQfqi5"
ce_james_icon = "https://imgur.com/a/yJ5jc51"
final_ce_icon = "https://imgur.com/a/p47JeLn"
ce_mountain_icon = ce_hex_icon

# ------------- discord channel numbers -------------
# ce
ce_log_id = 1208259110638985246             # log
ce_casino_test_id = 1208259878381031485     # fake casino
ce_casino_id = 1080137628604694629          # real casino
ce_game_additions = 949482536726298666      # game additions
# bot test
test_log_id = 1141886539157221457
test_casino_id = 811286469251039333
# go-to channels
game_additions = ce_log_id
casino = ce_casino_test_id
log = ce_log_id

# ------------- emoji icons -------------
icons = {
    "Tier 0" : '<:tier0:1126268390605070426>',
    "Tier 1" : '<:tier1:1126268393725644810>',
    "Tier 2" : '<:tier2:1126268395483037776>',
    "Tier 3" : '<:tier3:1126268398561677364>',
    "Tier 4" : '<:tier4:1126268402596585524>',
    "Tier 5" : '<:tier5:1126268404781809756>',
    "Tier 6" : '<:tier6:1126268408116285541>',
    "Tier 7" : '<:tier7:1126268411220074547>',

    "Action" : '<:CE_action:1126326215356198942>',
    "Arcade" : '<:CE_arcade:1126326209983291473>',
    "Bullet Hell" : '<:CE_bullethell:1126326205642190848>',
    "First-Person" : '<:CE_firstperson:1126326202102186034>',
    "Platformer" : '<:CE_platformer:1126326197983383604>',
    "Strategy" : '<:CE_strategy:1126326195915591690>',

    "Points" : '<:CE_points:1128420207329816597>'
}


# ---------------------------------------------functions-----------------------------------------------------------------

# 


# -------- get and set mongo databases --------
mongo_names = Literal["name", "tier", "curator", "user", "tasks", "unfinished"]
async def get_mongo(title : mongo_names):
    """Returns the MongoDB associated with `title`."""
    return await collection.find_one({'_id' : mongo_ids[title]})

async def dump_mongo(title : mongo_names, data) :
    """Dumps the MongoDB given by `title` and passed by `data`."""
    return await collection.replace_one({'_id' : mongo_ids[title]}, data)


# ----- get unix timestamp for x days from now -----
def get_unix(days = 0, minutes = -1, months = -1) -> int:
    """Returns a unix timestamp for `days` days (or `minutes` minutes, or `months` months) from the current time."""
    # return right now
    if(days == "now") : return int(time.mktime((datetime.datetime.now()).timetuple()))
    
    # return minutes
    elif (minutes != -1) : return int(time.mktime((datetime.datetime.now()+timedelta(minutes=minutes)).timetuple()))

    # return months
    elif (months != -1) : 
        days = months_to_days(months)
        return get_unix(days)

    # return days
    else: return int(time.mktime((datetime.datetime.now()+timedelta(days)).timetuple()))

# ----- convert ce timestamp to unix timestamp -----
def timestamp_to_unix(timestamp : str) -> int :
    """Takes in the CE timestamp (`"2024-02-25T07:04:38.000Z"`) and converts it to unix timestamp (`1708862678`)"""
    return int(time.mktime(datetime.datetime.strptime(str(timestamp[:-5:]), "%Y-%m-%dT%H:%M:%S").timetuple()))

# ----------------------------------------------------------------------------------------------------------------------------