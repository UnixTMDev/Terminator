#Don't show this!!!!!!!!
STEAM_API_KEY = "3F67F525F0A7DB6D8CCBD5004E79FFDF"
#TODO: Add support to deal with Steam Family sharing
from rapidfuzz import fuzz
import os
def find_best_match(query, options):
    best_match = None
    highest_score = 0

    for option in options:
        score = fuzz.partial_ratio(query.lower(), option.lower())
        
        if score > highest_score:
            highest_score = score
            best_match = option
    
    return best_match, highest_score

def get_library(user="UnixTMDev") -> dict:
    """Returns user's Steam library, similar to most JSON responses. user must be a valid Steam vanity URL.
    If retrieving user's Steam library fails, it'll read a library from 'fallback_library.json'."""
    try:
        from steam_web_api import Steam

        steam = Steam(STEAM_API_KEY)

        gamer = steam.users.search_user(user)
        games = steam.users.get_owned_games(gamer["player"].get("steamid",""))
        # {'game_count': 1234, 'games':[{ASDFDSFAFDSA} etc etc]}
        # {'appid':440, 'name': 'Team Fortress 2', 'playtime_forever': <minutes>, 'img_icon_url': 'fagfdsafsfsadfsdfdsa', 'playtime_windows_forever': 0, 'playtime_mac_forever': 0, 'playtime_linux_forever': 0, 'playtime_deck_forever': 0, 'rtime_last_played': 0, 'playtime_disconnected': 0}
    except Exception as e:
        print(e)
        try:
            import json
            game_list = ""
            with open("imports/fallback_library.json","r") as f:
                game_list = f.read()
            games = json.loads(game_list)
        except:
            print(e)
            return {}

    game_ids = {}
    speakable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    for x in games["games"]:
        name_pre = x.get("name","Team Fortress 3")
        name = ''.join(filter(lambda x: x in speakable, name_pre)).lower().replace(":","")
        appid = str(x.get("appid", "440"))
        game_ids[name] = appid
    return game_ids

#
def get_appid(game,gamer="UnixTMDev") -> str:
    """Returns (as a string) the Steam AppID for the game provided. Only searches gamer's Steam library for that game,
    for convenience's sake. gamer should be set as a valid Steam vanity URL. Casing in game doesn't matter."""
    game_ids = get_library(gamer)
    #All the game names in game_ids are lowercase. (Uppercase letters are in speakable anyway 'cause the filter comes before the lowercasing.)
    result = game_ids.get(game.lower(),"0")
    if result == "0":
        match, score = find_best_match(game.lower(),game_ids)
        #print(f"Found {match} with a score of {score}")
        if score > 75:
            #print("Cool")
            result = game_ids.get(match.lower(),"0")
    return result

#Wowww so good
##print(game_ids)
