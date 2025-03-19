latest_responses = {}
#response_events = {}
import asyncio

async def wait_for_condition(condition_func, check_interval=0.1):
    while not condition_func():
        await asyncio.sleep(check_interval)  # Avoid busy-waiting
    return True

#response_events = defaultdict(asyncio.Queue)

cmd_sockets = []