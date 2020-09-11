# Name: wsCore
# Author: Reacubeth
# Time: 2020/7/15 18:40
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from async_db import change_status
import json

users = {}
p_num = {}
user2file = {}


class WSEndPoint(WebSocketEndpoint):
    @staticmethod
    async def get_socket_ID(websocket):
        socket_str = str(websocket)[1:-1]
        socket_list = socket_str.split(' ')
        socket_ID = socket_list[3]
        return socket_ID

    @staticmethod
    async def ws_exit(p_id, socket_ID):
        users.pop(socket_ID)
        if socket_ID in user2file:
            await change_status(user2file[socket_ID], 0)
            del user2file[socket_ID]
        if p_id in p_num:
            p_num[p_id] -= 1
        for user in users:
            info = {'subject': 'total', 'message': {'num': len(users),
                                                    'p_id': p_id,
                                                    'socket_ID': socket_ID,
                                                    'des': 'off'}}
            if users[user]['p_id'] == p_id:
                await users[user]['websocket'].send_text(json.dumps(info))

    # Connect
    async def on_connect(self, websocket):
        await websocket.accept()
        socket_ID = await self.get_socket_ID(websocket)
        openMsg = await websocket.receive_text()
        p_id = json.loads(openMsg)['message']['p_id']
        users[socket_ID] = {'name': socket_ID, 'websocket': websocket, 'p_id': p_id}
        if p_id not in p_num:
            p_num[p_id] = 1
        else:
            p_num[p_id] += 1

        # broadcast entry
        for user in users:
            info = {'subject': 'total',
                    'message': {'num': p_num[users[user]['p_id']],
                                'p_id': users[socket_ID]['p_id'],
                                'socket_ID': socket_ID,
                                'des': 'on'}}
            if p_id == users[user]['p_id']:
                await users[user]['websocket'].send_text(json.dumps(info))

    # Broadcast Info
    async def on_receive(self, websocket, data):
        socket_ID = await self.get_socket_ID(websocket)
        data = json.loads(data)
        subject = data['subject']
        message = data['message']

        if subject == 'lock' and int(message['status']) == 1:
            user2file[socket_ID] = message['f_id']

        if subject == 'offline':
            await self.ws_exit(message['p_id'], socket_ID)
        else:
            for user in users:
                info = {'subject': subject, 'message': message}
                if users[user]['name'] != socket_ID and users[user]['p_id'] == message['p_id']:
                    await users[user]['websocket'].send_text(json.dumps(info))

    # Disconnect
    async def on_disconnect(self, websocket, close_code):
        socket_ID = await self.get_socket_ID(websocket)
        try:
            p_id = users[socket_ID]['p_id']
            await self.ws_exit(p_id, socket_ID)
        except Exception as e:
            pass


routes = [
    WebSocketRoute("/ws", WSEndPoint)
]
