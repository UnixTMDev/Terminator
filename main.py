##TODO##
# Give context (last ~5 messages)
# Allow to get results before writing extra commands.
##TODO##

from imports.global_junk import *
from RealtimeSTT import AudioToTextRecorder
from settings import *

from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
import asyncio

import ollama
import imports.llm_prompts as llm_prompts
import time
import sys
import pyperclip
import os
import json
from imports.steam_search import get_library

HumanResponses = True
# Why patch out the check when I can... not do that.

loop = asyncio.new_event_loop()

##TTS##
#import pyttsx3
#tts = pyttsx3.init()
#tts.setProperty("rate", SpeechRateDesired)
from yapper import Yapper, PiperSpeaker, PiperVoiceGB, PiperQuality

termer = PiperSpeaker(
    volume=0.5,
    voice=PiperVoiceGB.NORTHERN_ENGLISH_MALE
)

yapper = Yapper(speaker=termer)
#engine.connect('started-word', onWord)
def say(swag):
    if type(swag) == type(None) or swag.strip() in ["", None, False, 0]:
        return
    #global tts, ui
    yapper.yap(swag, plain=True)
    #tts.say(swag)
    #loop.call_soon(tts.runAndWait)
    #tts_thread = Thread(target=lambda: tts.iterate())
    #tts_thread.start()
    
    time.sleep(1.5)
##TTS##

from textual.app import App, ComposeResult
from textual.containers import Container,Horizontal,Vertical
from textual.widgets import Log, Label
from textual.color import Color
from textual.binding import Binding

def getSuicideCommand():
    from platform import system
    if system() == "Linux" or system() == "Darwin":
        return f"kill -9 {os.getpid()}"
    elif system() == "Windows":
        return f"taskkill /f {os.getpid()}"
    else:
        return f"kill -9 {os.getpid()}"

class MyTUI(App):
    BINDINGS = [
        Binding("q", "quit", "Quit the app"),
    ]
    def compose(self) -> ComposeResult:
        yield Container(
            Label(""),
            Log(id="userWords",name="User Speech"),
            Vertical(
            Log(id="commands",name="Commands Executed"),
            Horizontal(
            Log(id="results",name="Command Results"),
            Log(id="speech",name="Speech"),
            ),),
            Log(id="debug",name="Debug"),
        )

    runningReal = False
    

    def on_mount(self):
        self.runningReal = True
        self.screen.styles.background = Color.parse("#34027a")
        # Redirect stdout and stderr
        #f = open("log.txt","w")
        self.file = open("junk/log.txt","w")
        sys.stdout = self
        sys.stderr = self

    def action_quit(self) -> None:
        """Action to quit the app."""
        sys.exit(0)
        raise KeyboardInterrupt
        os.system(getSuicideCommand())
        self.exit()

    def on_shutdown(self):
        sys.exit(0)
        os.system(getSuicideCommand())
        raise KeyboardInterrupt

    def write(self, message):
        """Capture stdout/stderr and write to log."""
        log_widget = self.query_one("#debug", Log)
        log_widget.write(message.strip()+"\n")  # Strip extra newlines
        self.file.write(f"STDOUT -> {message}")
        self.file.flush()

        #asyncio.run(self.refresh())

    def flush(self):
        return



    async def log_message(self, log_id: str, message: str):
        if self.runningReal == False:
            print(message)
            return
        log_widget = self.query_one(log_id, Log)
        log_widget.write(message + "\n")  # Append new line
        log_widget.scroll_end()  # Forces it to scroll down
        self.refresh()
        self.file.write(f"{log_id} -> {message}\n")
        self.file.flush()

    log_text = log_message
    
ui = MyTUI()

from path_stuff import get_executables_in_path as path_execs
import command_handler as cmd_parser
not_ideal_misfires = ["suicide","cancel","invalid","exit_program","pause_listening","close_program","stop_program","open_url"]
for x in UnwantedMisfires: not_ideal_misfires.append(x)

LAST_CMD = ""

import re

def normalize(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

async def callbacklol(command, device="PC"):
    global tts, LAST_CMD

    await ui.log_text("#userWords",f"{'<' if not any(w in command.lower() for w in WakeWords.split(',')) else '<<'} \"{command}\"")

    if LAST_CMD == normalize(command):
        return ""
    else:
        LAST_CMD = normalize(command)

    if not any(w in command.lower() for w in WakeWords.split(',')) and device == "PC":
        return ""
    if any(w in command.lower() for w in WakeWords.split(',')):
        pass   

    command_list = "The valid commands and their argument formats are:"
    for x in list(cmd_parser.args_format.keys()):
        command_list = command_list+f" {x} (argument format: {cmd_parser.args_format[x]}),"
    llm_messages = [
        {'role': 'system','content':llm_prompts.get_overall_command},
        {'role': 'assistant','content':command_list},
        {'role': 'tool','content':str(get_library(Gamer))},
        {'role': 'system','content':f"The user ({UsersName}) wants you to know about them: \"{UserInfo}\". Also, they are talking from their {device}."},
        {'role': 'system', 'content':f"Reminder, the valid commands are (this time without the arguments): {str(cmd_parser.args_format.keys())}. These are the only commands you may use."},
        #{'role':'user','content':"You CAN do math and launch programs and crap. Also you have control of my bedroom light. I only listen to music on YouTube. You can launch most games on Steam. Minecraft is the main exception to that. Minecraft gets its own command. It's NEVER used as an argument. Got that? Good. AND, You CAN play YouTube videos, you CAN directly control my phone."},
        {'role':'system','content':f"If the user says 'this' or 'that', they could be referring to their clipboard contents, which is currently \"{pyperclip.paste()}\"."},
        {'role':"system","content":f"The executables installed are (shown as Python list): {str(path_execs())}"},
        {'role':'user','content':command}
    ]
    # NOTE: For whatever reason, adding a message before the one @:150 disables the prompt.
    # I don't even know, man.
    llm_response = ollama.chat(model=LLMModel, messages=llm_messages)
    cmd = llm_response['message']['content'].removeprefix("dict_keys(['").removesuffix("'])")
    #print("LLM says: ",cmd)
    
    if cmd.split(";")[0] in not_ideal_misfires:
        #print("Double-checking, too many false negatives nowadays.")
        llm_response = ollama.chat(model=LLMModel, messages=llm_messages)
        cmd = llm_response['message']['content'].removeprefix("dict_keys(['").removesuffix("'])")
        #print("LLM says: ",cmd)
        #print("Must be the right command THIS time, surely.")
        if cmd.split(";")[0] in not_ideal_misfires:
            #print("TRIPLE-checking, it wasn't.")
            llm_response = ollama.chat(model=LLMModel, messages=llm_messages)
            cmd = llm_response['message']['content'].removeprefix("dict_keys(['").removesuffix("'])")
            #print("LLM says: ",cmd)
            #print("Third strike, you're out.")
    await ui.log_text("#commands",cmd)
    if cmd.split(";")[0].strip() not in ["invalid","cancel"]:
        result = await cmd_parser.parse(cmd.replace("`",""))
        if "reRuŃ" in result[:8]:
            await ui.log_text("#results",f"PRERUN: {result}")
            llm_messages2 = [
            #    {'role': 'system','content':llm_prompts.get_overall_command},
            #    {'role': 'assistant','content':command_list},
            #    {'role': 'tool','content':str(get_library(Gamer))},
            #    {'role': 'system','content':f"The user wants you to know about them: \"{UserInfo}\""},
            #    {'role': 'system', 'content':f"Reminder, the valid commands are (this time without the arguments): {str(cmd_parser.args_format.keys())}. These are the only commands you may use."},
            #    {'role':'user','content':"You CAN do math and launch programs and crap. Also you have control of my bedroom light. I only listen to music on YouTube. You can launch most games on Steam. Minecraft is the main exception to that. Minecraft gets its own command. It's NEVER used as an argument. Got that? Good. AND, You CAN play YouTube videos. Also, importantly, don't use the \"wait\" command if there's no operations to be done on the command results."},
            #    {'role':'system','content':f"If the user says 'this' or 'that', they could be referring to their clipboard contents, which is currently \"{pyperclip.paste()}\"."},
            #    {'role':"system","content":f"The executables installed are (rendered as a Python list): {str(path_execs())}"},
                {'role':'user','content':command},
                #{'role':'assistant','content':cmd.split("wait;")[0]},
                {'role':'tool','content':result.replace("reRuŃ", "").strip()},
                {'role':'system','content':"What question to WolframAlpha should you send to convert the units to what the user wants? ONLY RESPOND WITH THE WOLFRAM ALPHA SEARCH QUERY."},
            #    {'role': 'system','content':llm_prompts.get_overall_command},
                #{'role': "system", 'content':"Remember that THE USER WILL NEVER SEE YOUR MESSAGE. ONLY RESPOND WITH THE COMMANDS THE USER WOULD HAVE WANTED AFTER YOU GET THE DATA."}
            ]
            llm_response2 = ollama.chat(model=LLMModel, messages=llm_messages2)
            cmd2 = llm_response2['message']['content'].removeprefix("dict_keys(['").removesuffix("'])")
            result2 = await cmd_parser.wolfram(cmd2.replace("`",""))
            result = result+"\nUNIT CONVERSIONS DONE: "+cmd2.replace("`","")+" "+result2
            await ui.log_text("#commands",f"DEAR WOLFRAM: {cmd2}")
        WordsReady = True
    else:
        result = ""
        WordsReady = False
    await ui.log_text("#results", result)
    if HumanResponses and WordsReady and cmd.split(";")[0] != "pokedex" and cmd.split(";")[0] != "wikipedia":
        llm_messages = [
            {'role':'system', 'content':llm_prompts.human_response_prompt},
            {'role':'assistant','content':cmd},
            {'role':'user','content':command},
            {'role':'tool', 'content':result}
        ]
        llm_response2 = ollama.chat(model=ResponseModel, messages=llm_messages)
        message = llm_response2['message']['content'].removeprefix("dict_keys(['").removesuffix("'])")
    else:
        message = result
    await ui.log_text("#speech",message)
    return message

#HOLY HELL IT WORKS
async def terminator_loop():
    while True:
        time.sleep(1)
        def recording_finished():
            asyncio.run(ui.log_text("#debug","speech end"))
            #print("User stopped speaking, transcribing.")
            return

        with AudioToTextRecorder(spinner=not USE_TUI, model="medium.en", language="en",on_recording_start=lambda: asyncio.run(ui.log_message("#debug","speech start")), on_recording_stop=recording_finished, post_speech_silence_duration=1.25, no_log_file=False
            ) as recorder:
            say("Terminator active...")
            await ui.log_message("#speech","Terminator active...")
            while True:
                try:
                    def asdffdsa(a):
                        #with open("test.txt","a") as f:
                        #    f.write("CALLED2")
                        #asyncio.run(ui.log_text("#debug",a))
                        b = asyncio.run(callbacklol(a))
                        say(b)
                    recorder.text(asdffdsa)
                except Exception as e:
                    await ui.log_text("#debug", f"ERROR: {str(e)}")

import websockets



async def api_handler(websocket):
    print("new chat client connected")
    while True:
        try:
            data = await websocket.recv()
            data = json.loads(data)
            msg = data.get("msg")
            device = data.get("device", "<UNKNOWN DEVICE>")
            if device == "phone":
                await asyncio.sleep(5)
            res = await callbacklol(msg, device=device)
            await websocket.send(res)
        except websockets.exceptions.ConnectionClosed:
            break

async def cmd_handler(websocket):
    print("new command client connected")
    cmd_sockets.append(websocket)
    while True:
        try:
            res = await websocket.recv()
            response = json.loads(res)
            target = response.get("device","unknown")
            latest_responses[target] = response.get("result", "ERROR")
            #if target in response_events:
                #print(f"Scheduling event set for {target}")
                #print(f"cmd_handler() event object for {target}: {response_events[target]}")
                #print(f"cmd_handler() running in loop: {asyncio.get_running_loop()}")
                #await response_events[target].put(response.get("result", "ERROR"))  # Put result in queue

        except websockets.exceptions.ConnectionClosed:
            cmd_sockets.remove(websocket)
            break

async def api_thread():
    async with websockets.serve(api_handler, "0.0.0.0", 5700):
        await asyncio.Future()  # run forever

async def cmd_api_thread():
    async with websockets.serve(cmd_handler, "0.0.0.0", 5701):
        await asyncio.Future()  # run forever


async def startup():
    #ttsth = Thread(target=lambda: tts.startLoop(False))
    #ttsth.start()
    if USE_TUI:
        #therminator = Thread(target=lambda: asyncio.run(terminator_loop()))
        #therminator.start()
        therminator_api = Thread(target=lambda: asyncio.run(api_thread()))
        therminator_api.start()
        therminator_cmd_api = Thread(target=lambda: asyncio.run(cmd_api_thread()))
        therminator_cmd_api.start()
        time.sleep(5)
        ui_thread = Thread(target=lambda: asyncio.run(ui.run_async()))
        ui_thread.start()
        await terminator_loop()
    else:
        therminator_api = Thread(target=lambda: asyncio.run(api_thread()))
        therminator_api.start()
        therminator_cmd_api = Thread(target=lambda: asyncio.run(cmd_api_thread()))
        therminator_cmd_api.start()
        await terminator_loop()

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    asyncio.run(startup())
# {"device":"phone","result":"Test response. Success :)"}