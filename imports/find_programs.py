#Look at this shitshow, I'm not putting this in command_handler.
import os
import glob
from settings import Swearing
from rapidfuzz import fuzz

def launch_program(args: str) -> str:
    return "Needs to be fixed. Tell the user that the dev hasn't fixed this function yet."
# Rest is unreachable for now.
    GlobalStartMenuDir = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"
    UserStartMenuDir = "C:\\Users\\UnixTMDev Lastname\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"
    #.lnk is shortcuts
    global_shortcuts = []
    user_shortcuts = []
    for x in glob.glob(pathname='*.lnk', root_dir=GlobalStartMenuDir):
        global_shortcuts.append(x)

    for x in glob.glob(pathname='*\\*.lnk', root_dir=GlobalStartMenuDir):
        global_shortcuts.append(x)

    for x in glob.glob(pathname='*.lnk', root_dir=UserStartMenuDir):
        user_shortcuts.append(x)

    for x in glob.glob(pathname='*\\*.lnk', root_dir=UserStartMenuDir):
        user_shortcuts.append(x)

    global_match, global_score = find_best_match(args,global_shortcuts)
    local_match, local_score = find_best_match(args,user_shortcuts)
    print("L",local_score,"|","G",global_score)
    if local_score <= 75 and global_score <= 75:
        return "Not found, are you crazy?"
    else:
        try:
            if global_score > local_score:
                os.startfile(GlobalStartMenuDir+"\\"+global_match)
                if global_match.__contains__("Visual Studio Code"):
                    if Swearing:
                        return "Oh fuck, I found it."
                    else:
                        return "Oh god, here it is, I guess."
                return "Found it!"
            if global_score < local_score:
                os.startfile(UserStartMenuDir+"\\"+local_match)
                if global_match.__contains__("Visual Studio Code"):
                    if Swearing:
                        return "Oh fuck, I found it."
                    else:
                        return "Oh god, here it is, I guess."
                return "Found it!"
            if global_score == local_score:
                os.startfile(UserStartMenuDir+"\\"+local_match)
                if global_match.__contains__("Visual Studio Code"):
                    if Swearing:
                        return "Oh fuck, I found it."
                    else:
                        return "Oh god, here it is, I guess."
                return "Found 2 matches, launching user instance."
        except:
            return "You canceled it. I think. Anyway it didn't launch."
def find_best_match(query, shortcut_paths) -> str|int:
    best_match = None
    highest_score = 0

    for shortcut in shortcut_paths:
        shortcut_name = os.path.splitext(os.path.basename(shortcut))[0]  # Strip extension
        score = fuzz.partial_ratio(query.lower(), shortcut_name.lower())
        
        if score > highest_score:
            highest_score = score
            best_match = shortcut
    
    return best_match, highest_score
if __name__ == "__main__":
    desired = input("Wanted program: ")
    print(launch_program(desired))
