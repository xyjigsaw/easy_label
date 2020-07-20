# Name: test
# Author: Reacubeth
# Time: 2020/7/15 21:05
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

from fastapi import FastAPI
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import Route, WebSocketRoute
from fastapi.middleware.cors import CORSMiddleware

users = {}


class WSEndPoint(WebSocketEndpoint):
    @staticmethod
    async def get_socket_ID(websocket):
        socket_str = str(websocket)[1:-1]
        socket_list = socket_str.split(' ')
        socket_ID = socket_list[3]
        print(socket_ID)
        return socket_ID

    # Connect
    async def on_connect(self, websocket):
        await websocket.accept()
        socket_ID = await self.get_socket_ID(websocket)

        users[socket_ID] = {'name': socket_ID, 'websocket': websocket}

        # broadcast entry
        for user in users:
            await users[user]['websocket'].send_text(users[socket_ID]['name'] + ' Add! Total: ' + str(len(users)))

    # Broadcast Info
    async def on_receive(self, websocket, data):
        socket_ID = await self.get_socket_ID(websocket)

        for user in users:
            await users[user]['websocket'].send_text(users[socket_ID]['name'] + ' ' + data)

    # Disconnect
    async def on_disconnect(self, websocket, close_code):
        socket_only = await self.get_socket_ID(websocket)
        users.pop(socket_only)
        print('Exit Total: ' + str(len(users)))
        pass


routes = [
    WebSocketRoute("/ws", WSEndPoint)
]

app = FastAPI(routes=routes)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://10.10.10.1:8082",
    "http://10.10.10.1:8081",
    "http://10.10.10.1:8080",
    "http:192.169.0.3:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# uvicorn wsCore:app --reload --port 8000 --host 0.0.0.0

