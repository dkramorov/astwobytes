#!/usr/bin/env python
# python3 -m websockets --version
# websockets 10.3
import json
import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://185.130.212.110:5153') as websocket:
        #name = input("What's your name? ")
        #await websocket.send(name)
        #print("> {}".format(name))

        data = {'FRAMES_UNTIL_STOP_TALK': 10, 'call_id': '123'}
        await websocket.send(json.dumps(data))

        greeting = await websocket.recv()
        print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())