import json
import discord
import time
import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import requests

# icons for CE emoji
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



ce_mountain_icon = "https://cdn.discordapp.com/attachments/639112509445505046/891449764787408966/challent.jpg"
ce_james_icon = "https://cdn.discordapp.com/attachments/1028404246279888937/1136056766514339910/CE_Logo_M3.png"
final_ce_icon = "https://cdn.discordapp.com/attachments/1135993275162050690/1144289627612655796/image.png"


# ------------------------------------------------ CREATE MULTI EMBED ------------------------------------------------------------ #
def create_multi_embed(event_name, time_limit, game_list, cooldown_time, interaction, database_name) :
    from Helper_Functions.mongo_silly import get_mongo, dump_mongo, get_unix

    # ----- Set up initial embed -----
    embeds = []
    embeds.append(discord.Embed(
        color = 0x000000,
        title=event_name,
        timestamp=datetime.datetime.now()
    ))
    embeds[0].set_footer(text=f"Page 1 of {str(len(game_list) + 1)}", icon_url = final_ce_icon)
    embeds[0].set_author(name="Challenge Enthusiasts")

    # ----- Add all games to the embed -----
    games_value = ""
    i = 1
    for selected_game in game_list:
        games_value += "\n" + str(i) + ". " + selected_game
        i+=1
    embeds[0].add_field(name="Rolled Games", value = games_value)

    # ----- Display Roll Requirements -----
    embeds[0].add_field(name="Roll Requirements", value =
        f"You have two weeks to complete " + embeds[0].title + "."
        + "\nMust be completed by <t:" + str(get_unix(time_limit))
        + f">.\n{event_name} has a cooldown time of {cooldown_time} days.", inline=False)
    embeds[0].timestamp = datetime.datetime.now()
    embeds[0].set_thumbnail(url = interaction.user.avatar)
    
    # ----- Create the embeds for each game -----
    page_limit = len(game_list) + 1
    i=0
    for selected_game in game_list :
        total_points = 0
        embeds.append(getEmbed(selected_game, interaction.user.id, database_name))
        embeds[i+1].set_footer(text=(f"Page {i+2} of {page_limit}"),
                                icon_url=final_ce_icon)
        embeds[i+1].set_author(name="Challenge Enthusiasts")
        embeds[i+1].set_thumbnail(url=interaction.user.avatar)
        for objective in database_name[selected_game]["Primary Objectives"] :
            total_points += int(database_name[selected_game]["Primary Objectives"][objective]["Point Value"])
        i+=1
    
    return embeds # Set the embed to send as the first one



# ----------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------- GET EMBED FUNCTION ------------------------------------------------------ #
# ----------------------------------------------------------------------------------------------------------------------------------- #
def getEmbed(game_name, authorID, database_name):

    total_points = 0
    #TODO add error exceptions
    #TODO turn this into a class with getters and setters for wider versatility
    
    if(game_name in list(database_name)) : 
        correct_app_id = database_name[game_name]["Steam ID"]
        print(f"found {game_name} with app id {correct_app_id} in local json file :)")
    else :
        print(f"couldn't find {game_name} in local json file, searching steam :(")
        game_word_lst = game_name.split(" ")
        for name in game_word_lst:
            if len(name) != len(name.encode()):
                game_word_lst.pop(game_word_lst.index(name))

        searchable_game_name = " ".join(game_word_lst)

        payload = {'term': searchable_game_name, 'f': 'games', 'cc' : 'us', 'l' : 'english'}
        response = requests.get('https://store.steampowered.com/search/suggest?', params=payload)

        divs = BeautifulSoup(response.text, features="html.parser").find_all('div')
        ass = BeautifulSoup(response.text, features="html.parser").find_all('a')
        options = []
        for div in divs:
            try:
                if div["class"][0] == "match_name":
                    options.append(div.text)
            except:
                continue

            correct_app_id = ass[0]['data-ds-appid']

        for i in range(0, len(options)):
            if game_name == options[i]:
                correct_app_id = ass[i]['data-ds-appid']

# --- DOWNLOAD JSON FILE ---

    # Open and save the JSON data
    payload = {'appids': correct_app_id, 'cc' : 'US'}
    response = requests.get("https://store.steampowered.com/api/appdetails?", params = payload) #TODO: possible error here
    jsonData = json.loads(response.text)
    
    # Save important information
    imageLink = jsonData[correct_app_id]['data']['header_image']
    gameDescription = str(jsonData[correct_app_id]['data']['short_description']).replace('&amp;', '&').replace('&quot;', '\"')
    if(jsonData[correct_app_id]['data']['is_free']) : 
        gamePrice = "Free"
    
    elif('price_overview' in list(jsonData[correct_app_id]['data'].keys())) :
        gamePrice = jsonData[correct_app_id]['data']['price_overview']['final_formatted']
    else :
        gamePrice = "No price listed."
    gameNameWithLinkFormat = game_name.replace(" ", "_")

# --- CREATE EMBED ---

    # and create the embed!
    embed = discord.Embed(title=f"{game_name}",
        url=f"https://store.steampowered.com/app/{correct_app_id}/{gameNameWithLinkFormat}/",
        description=(f"{gameDescription}"),
        colour=0x000000,
        timestamp=datetime.datetime.now())

    embed.add_field(name="Price", value = gamePrice, inline=True)
    
    embed.set_author(name="Challenge Enthusiasts", url=f"https://cedb.me/game/{database_name[game_name]["CE ID"]}/")
    embed.set_image(url=imageLink)
    embed.set_thumbnail(url=ce_mountain_icon)
    embed.set_footer(text="CE Assistant",
        icon_url=final_ce_icon)
    embed.add_field(name="Rolled by", value = "<@" + str(authorID) + ">", inline=True)
    if game_name in database_name.keys() :
        for objective in database_name[game_name]["Primary Objectives"] :
            total_points += int(database_name[game_name]["Primary Objectives"][objective]["Point Value"])
        embed.add_field(name="CE Status", 
                        value=icons[database_name[game_name]["Tier"]] + icons[database_name[game_name]["Genre"]] + f" - {total_points} Points" + icons["Points"], 
                        inline=True)
        try:
            embed.add_field(name="CE Owners", value= database_name[game_name]["Total Owners"], inline=True)
            embed.add_field(name="CE Completions", value= database_name[game_name]["Full Completions"], inline=True)
        except:""
    else : embed.add_field(name="CE Status", value="Not on Challenge Enthusiasts", inline=True)

    return embed
