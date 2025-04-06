from settings import *

from imports.llm_prompts import *

from imports.global_junk import *

##Imports used several times

#What do you think it's for???
import datetime

#REST APIs and checking internet status
import requests

#Waiting n crap
import time as clock

import ollama

import sys

#Media control
#import pyautogui

#take a guess
from threading import Thread

#You'll never guess,,,,,
import webbrowser
import inspect

import asyncio

##TTS##
import pyttsx3
tts = pyttsx3.init()
tts.setProperty("rate", SpeechRateDesired)
def say(swag):
    global tts
    tts.say(swag)
    tts.runAndWait()
##TTS##

#Code time

def get_firefox_path() -> str:
    path = shutil.which("firefox")
    if path:
        return path
    else:
        raise FileNotFoundError("bro... firefox ain't even installed 💀")

def internet_connected(test_domain="https://unixtm.dev") -> bool:
    try:
        response = requests.get(test_domain, timeout=5)
        return True
    except requests.ConnectionError:
        return False

online = internet_connected()

#"<ignores arguments, use any>" as args in the format seems to work great, idk, don't piss off the AI.

import traceback
args_format = {}
from random import randint
# If I can be SO fr right now, I don't know how this works anymore.
# It looks like the code equivalent of a bunch of wires.

args_format.update({"wait":"<no args, does all unit conversions needed>"})

async def parse(command: str) -> str:
    """Parses out and runs command passed in, and returns the response as a String to be read by TTS.
    Format goes: "command;arg1 arg2 arg3" """
    if len(command.strip().splitlines()) > 1:
        responseReal = ""
        for x in command.strip().splitlines():
            if ";" not in x:
                continue
            if x.replace(";", "").strip()[:4] == "wait":
                responseReal = "reRuŃ\n"+responseReal
                return responseReal.strip()
            a = await parse(x)
            a = str(a)
            responseReal = responseReal+f"Action {command.strip().splitlines().index(x)+1}: "+a+"\n"
        return responseReal.strip()
    inst = command.split(";")[0].rstrip().lstrip().lower()
    test = inst.split()
    if len(test) > 1:
        inst = test[-1]
    args = command.removeprefix(command.split(";")[0].rstrip().lstrip()+";")
    if args == command: args = ""
    if (inst == "invalid" or inst == "cancel") and args.__contains__(";"):
        command = command[len(inst):]
        inst = command.split(";")[0].rstrip().lstrip().lower().replace(" ","_").replace("-","_")
        args = command.removeprefix(command.split(";")[0].rstrip().lstrip()+";").replace(";"," ")
    #wd = os.getcwd()
    home_dir = os.path.expanduser("~")
    os.chdir(home_dir)
    try:
        if inspect.iscoroutinefunction(globals().get(inst,invalid)):
            return await globals().get(inst,invalid)(args)
        else:
            return globals().get(inst,invalid)(args)
    except Exception as e:
        print(traceback.format_exc())

        return "Error happened. Go take a look at the logs."

args_format.update({"invalid":"<ignores arguments, use any>"})
def invalid(*args) -> str:
    """Just complains. Returns a string for TTS."""
    response = "Invalid command, idiot."
    return response

args_format.update({"relay":"<target device>:<remote Terminator command, follows \"command;args\" format>"})
async def relay(args: str,*extra_args) -> str:
    global cmd_sockets
    target = args[:args.index(":")].strip()
    c = args[args.index(":")+1:]
    cmd = c[:c.index(";")].strip()
    arguments = c[c.index(";")+1:].strip()
    data = json.dumps({
        "device": target,
        "command": cmd,
        "args": arguments
    })

    latest_responses[target] = ""
    for ws in cmd_sockets:
        await ws.send(data)

    await wait_for_condition(lambda: latest_responses[target] != "")
    result = latest_responses[target]
    print(f"response from {target}!")
    print(result)
    return result


args_format.update({"cancel":"<ignores arguments, use any>"})
def cancel(*args) -> str:
    """woops i didnt mean to get you. Returns a string for TTS."""
    response = "Oh noooo did it make a mistake???? did little baby make a mistake???"
    return response

args_format.update({"new_command":"<prompt for codellama to make command>"})
async def new_command(prompt: str) -> str:
    llm_messages = [
        {'role':'system', 'content':new_command_prompt_sync},
        {'role':'user','content':prompt}
    ]
    llm_response = ollama.chat(model="codellama", messages=llm_messages)
    comd = llm_response['message']['content']
    try:
        print(comd)
        exec(comd.replace("```",""))
        llm_messages2 = [
        {'role':'system', 'content':get_func_name},
        {'role':'user','content':comd}
        ]
        llm_response2 = ollama.chat(model="phi4", messages=llm_messages2)
        target = llm_response2['message']['content']
        #llm_messages3 = [
        #{'role':'system', 'content':get_func_args},
        #{'role':'user','content':comd}
        #]
        #llm_response3 = ollama.chat(model="phi4", messages=llm_messages3)
        #args = llm_response3['message']['content']
        print(target)
        func = locals().get(target,lambda a: "No response from command. Assuming successful action.")
        if inspect.iscoroutinefunction(func):
            aghg = await func()
            return aghg
        else:
            return func()
    except Exception as e:
        print(traceback.format_exc())

        return await new_command(prompt)

from imports.steam_search import get_appid
import os
args_format.update({"steam":"<game name>"})
def steam(args: str) -> str:
    args = args.replace("_"," ")
    #final_steam_url = "steam://"
    gameid = get_appid(args, Gamer)
    #final_steam_url = final_steam_url+'rungameid/'+gameid
    ##print(f"calling {final_steam_url}")
    #print(f"Attempting to launch appid {gameid} from Steam.")
    if str(gameid) == "0":
        #print("No we're not")
        return "Game not found. Are you SURE you have that game?"
    tjread = Thread(target=lambda: os.system(SteamExePath+f" -applaunch {gameid}"))
    tjread.start()
    return "Alright, launching from Steam. Give it a sec."

args_format.update({"suicide":"<ignores arguments, THIS SHUTS YOU DOWN>"})
def suicide(args: str) -> str:
    say("Exiting...")
    exit(0)
    return "Exit failed???"
args_format.update({"kill_yourself":"<ignores arguments, THIS SHUTS YOU DOWN>"})
kill_yourself = suicide
args_format.update({"exit":"<ignores arguments, THIS SHUTS YOU DOWN>"})
exit = suicide

args_format.update({"time":"<ignores arguments, use any>"})
def time(*args) -> str:
    now = datetime.datetime.now()
    strftime = now.strftime("%H:%M (%I:%M %p)")
    return f"It's {strftime}."


# args_format.update({"pause_listening":"<amount of seconds>"})
# def pause_listening(args: str) -> str:
#     voice.Speak(f"Alright, wacko. {args} seconds on the clock.")
#     try:
#         seconds = int(args.lstrip().rstrip())
#     except:
#         seconds = 30
#         voice.Speak("Something went wrong, goin' with 30 seconds.")
#     clock.sleep(seconds)
#     return "I'm back, what up?"

args_format.update({"pause":"<ignores arguments, use any>"})
def pause(args: str) -> str:
    #pyautogui.press("playpause")
    os.system("playerctl -a play-pause")
    return "K."
args_format.update({"resume":"<ignores arguments, use any>"})
resume = pause

args_format.update({"next_track":"<ignores arguments, use any>"})
def next_track(args: str) -> str:
    #pyautogui.press("nexttrack")
    os.system("playerctl -a next")
    return "K."

args_format.update({"prev_track":"<ignores arguments, use any>"})
def prev_track(args: str) -> str:
    #pyautogui.press("prevtrack")
    os.system("playerctl -a previous")
    return "K."

import wikipedia as wiki
args_format.update({"wikipedia":"<topic the user asked about>"})
def wikipedia(args: str) -> str:
    try:
        return wiki.summary(args, sentences=2)
    except:
        return "Not found homeboy"

args_format.update({"google_search_in_browser":"<user's search query>"})
def google_search_in_browser(args: str) -> str:
    firefox = webbrowser.Mozilla(get_firefox_path())
    query = args.lstrip().rstrip().replace(" ","+")
    ##print(query,"/args:",args)
    new_url = "https://www.google.com/search?q="+query
    #print(new_url)
    firefox.open_new(new_url)
    return "Alright."
args_format.update({"search":"<user's search query>"})
search = google_search_in_browser

from imports.pokemon import arg_format as pokedex_args_format
args_format.update({"pokedex":pokedex_args_format})
from imports.pokemon import pokedex

# args_format.update({"open_url":"<user-provided URL>"})
# def open_url(args: str) -> str:
#     firefox = webbrowser.Mozilla("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
#     firefox.open_new(args)
#     return "Alright."
    
#args_format.update({"web":"<user-provided URL>"})
#web = open_url

args_format.update({"random":"<lower and higher bound, both inclusive, separated by a colon>"})
async def random(args):
    asdf = args.split(":")
    return str(randint(int(asdf[0]),int(asdf[1])))

args_format.update({"wolfram":"<Wolfram Alpha query, usually unit conversions or other simple questions>"})
async def wolfram(args):
    if "weather" in args.lower():
        return await weather(args)
    else:
        return await wolfram2(args)
from imports.wolfram_lookup import wolfram as wolfram2

args_format.update({"youtube":"<user's YouTube search query>"})
from youtube_search import YoutubeSearch
def youtube(args: str) -> str:
    if args.lower() == "youtube": return "Not gonna search YouTube on YouTube. Isn't gonna work."
    results = YoutubeSearch(args, max_results=10).to_dict()
    firefox = webbrowser.Mozilla(get_firefox_path())
    firefox.open(f"https://youtube.com/watch?v={results[0].get('id')}", autoraise=False)
    #return f"Playing '{results[0].get('title')}' by {results[0].get('channel')}"
    return "Playing first video found."

args_format.update({"play_song":"<user's YouTube search query>"})
play_song = youtube

args_format.update({"play_podcast":"<user's YouTube search query>"})
play_podcast = youtube

args_format.update({"play_video":"<user's YouTube search query>"})
play_video = youtube

args_format.update({"play":"<user's YouTube search query>"})
play = youtube

args_format.update({"exec_file":"<Process to launch>"})
from subprocess import run as runSwagReal
import subprocess
def exec_file(a):
    tjaread = Thread(target=lambda: exec_file2(a))
    tjaread.start()
    return "Program started, return value unknown"
def exec_file2(a):
    return str(runSwagReal(["bash","-c",a], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))


args_format.update({"current_weather":"<IMPERIAL RESULTS, ignores arguments, uses user's home city>"})
import python_weather
async def current_weather(args: str) -> str:
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get(HomeCity)
    return f"""{weather.temperature} Fahrenheit and {str(weather.kind)}.
    (extraneous data, only tell if user wanted any of the following:) description: {str(weather.description)}, feels like: {str(weather.feels_like)} F,
    humidity: {weather.humidity}, precipitation: {weather.precipitation} inches,
    pressure: {weather.pressure} inches, visibility: {weather.visibility} miles,
    ultraviolet: {str(weather.ultraviolet)},
    wind direction: {str(weather.wind_direction)}, wind speed: {weather.wind_speed} mph
    """

args_format.update({"weather":"<IMPERIAL RESULTS, ignores arguments, uses user's home city>"})
weather = current_weather

args_format.update({"forecast_daily":"<IMPERIAL RESULTS, ignores arguments, uses user's home city>"})
import python_weather
async def forecast_daily(args: str) -> str:
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get(HomeCity)
    forecasts = {}
    # str(datetime.date.today().strftime("%a"))
    for day in weather:
        weekday = day.date.strftime("%a")
        forecasts[weekday if weekday != datetime.date.today().strftime("%a") else "Today"] = f"High of {day.highest_temperature} and low of {day.lowest_temperature}, moon is {str(day.moon_phase)}."
    return str(forecasts)

args_format.update({"forecast_hourly":"<IMPERIAL RESULTS, ignores arguments, uses user's home city>"})
import python_weather
async def forecast_hourly(args: str) -> str:
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get(HomeCity)
    forecasts = {}
    # str(datetime.date.today().strftime("%a"))
    for day in weather:
        for hour in day:
            huor = hour.time.strftime("%H")
            filtered_chances = {
                attr: getattr(hour, attr)
                for attr in dir(hour)
                if attr.startswith("chances_of_") and getattr(hour, attr) > 0
            }
            tha_key = huor if huor != datetime.date.today().strftime("%H") else "Now"
            if int(huor) >= int(datetime.date.today().strftime("%H")):
                forecasts[tha_key] = f"{hour.temperature} degrees F (feels like {hour.feels_like} degrees), chances of weather are: {filtered_chances}. Auto-generated description is \"{hour.description}\"."
    return str(forecasts)

args_format.update({"google_search_info":"<query>"})
from imports.web_searches import smart_search as google_search_info

#Holy Christ
import json
from settings import TargetDevice, HomeAssistantServer, HOME_ASSISTANT_TOKEN
args_format.update({"light":"(on/off/toggle)"})
def light(args: str) -> str:
    if args in ["headphones","speaker"]:
        return audio_source(args)
    headers = {"Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}", "content-type": "application/json"}
    def set_device_state(state, target) -> dict:
        res2 = requests.post(f"{HomeAssistantServer}states/{target}",data=json.dumps({"state": state}),headers=headers)
        if res2.status_code != 200:
            return False
        res = requests.post(f"{HomeAssistantServer}services/light/turn_{state}",data=json.dumps({"entity_id": target}),headers=headers)
        if res.status_code != 200:
            return False
        return json.loads(res.text)
    def get_device_state(target) -> dict:
        res = requests.get(f"{HomeAssistantServer}states/{target}",headers=headers)
        if res.status_code != 200:
            return False
        return json.loads(res.text)
    desired = args.lstrip().rstrip()
    for x in ["on","yes","true","enabled","active","powered","resume","unpause"]:
        if x in desired.lower():
            set_device_state('on', TargetDevice)
            return "Okay."
    for x in ["off","no","false","disabled","inactive","unpowered","pause"]:
        if x in desired.lower():
            set_device_state('off', TargetDevice)
            return "Okay."
    for x in ["toggle","flip","switch","swap","invert","shift",""]:
        if x in desired.lower() or not desired:
            state = get_device_state(TargetDevice).get("state","off")
            if state == "on":
                set_device_state('off', TargetDevice)
                return "Okay."
            elif state == "off":
                set_device_state('on', TargetDevice)
                return "Okay."
            else:
                set_device_state('on', TargetDevice)
                return "Okay."
    return "No valid states given. I dunno man, tell the user you screwed up."

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
#args_format.update({"audio_source":"(speaker/headphones)"})
#def audio_source(args: str) -> str:
#    match, score = find_best_match(args, ["speaker","headphones"])
#    if score < 75:
#        desired = "headphones"
#    else:
#        desired = match
#    if desired == "speaker":
#        new_device = "LG HDR 4K"
#    if desired == "headphones":
#        new_device = "Headphones"
#    #os.system("nircmd.exe setdefaultsounddevice \"" + new_device + "\"")
#    return "Dev hasn't fixed. Tell user it couldn't be done."
#args_format.update({"audio":"(speaker/headphones)"})
#audio = audio_source
#args_format.update({"speaker":"<ignores arguments, sets audio to speakers>"})
#speaker = lambda asdf: audio_source("speaker")
#args_format.update({"headphones":"<ignores arguments, sets audio to headphones>"})
#headphones = lambda asdf: audio_source("headphones")

if __name__ == "__main__":
    print("Welcome to Terminator's Command Handler")
    print(asyncio.run(parse(input("#: "))))
