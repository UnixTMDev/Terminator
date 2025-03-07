import sys
sys.path.append("../terminator")

from settings import WOLFRAM_KEY
from wolframalpha import Client
import asyncio

def is_running_async():
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False

async def wolfram(args: str) -> str:
    try:
        client = Client(WOLFRAM_KEY)
        if is_running_async():
            query = await client.aquery(input=args)
        else:
            query = client.query(input=args)
        res = list(query.info)[1].text
        return res if res != "" else "Search failed."
    except Exception as e:
        print(e)
        return "Error during search."

async def async_run_it(argz):
    return await wolfram(argz)

if __name__ == "__main__":
    asyncquestionmark = input("async? y/n:")
    if asyncquestionmark == "n":
        print(wolfram(input("wolfram# ")))
    if asyncquestionmark == "y":
        print(asyncio.run(async_run_it(input("wolfram# "))))
