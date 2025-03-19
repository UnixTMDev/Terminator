# This is where Terminator's settings will be set.
# All caps-labeled items should be kept secret from others.

##Keys/tokens for services that Terminator can use.
from secrets_real import HOME_ASSISTANT_TOKEN, WOLFRAM_KEY

#Notes about yourself, maybe this'll help the LLM figure out the command.
from secrets_real import UserInfo

#What is your home city?
from secrets_real import HomeCity

#Terminator misrecognizes what you want sometimes, add commands here that you want to double-check the validity of.
UnwantedMisfires = ["launch","open_program","run_program","wikipedia", "light","audio_source","headphones","speaker",'lock_computer', 'wikipedia',"time"]

##Steam config options
#Steam vanity URL for user. (e.g. UnixTMDev, carvenwhimsy)
Gamer = "UnixTMDev"

#Path to Steam executable
SteamExePath = "/usr/bin/env steam"

##Wake Word crap
#Wake words, comma separated. Any word may be used, must be lowercase
WakeWords = "terminator,jarvis"


##Home Assistant crap
#Target device for light controls. Should be a HomeAssistant device
TargetDevice = "light.redstone_lamp"

#Self explanatory. Should be in the format of "http://[ip]:[port]/api/"
HomeAssistantServer = "http://10.0.0.90:8123/api/"

##TTS
#Words per minute.
SpeechRateDesired = 150

##LLM settings
#An LLM proccesses the user input, select it here.
#ollama model names, see at https://ollama.com/library
LLMModel = "phi4"
ResponseModel = "phi4"

from secrets_real import *