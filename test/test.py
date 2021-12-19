# -*- coding:utf-8-*-
# @author: Qiuhaixing
# !/usr/bin/env python3
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo

# App api_id: 12218302
# App api_hash: 6331242062a6378f3016db6643f10277
# App title: tgapp
# Short name: appname
# TgSoSobot
bot_token = '5096068391:AAFw4nL5LhbA9WSXeoDWhgOHje-wsWsmv48'
api_id = 12218302  # 申请的TG API ID
api_hash = '6331242062a6378f3016db6643f10277'  # 申请的TG API hash

# anon为缓存的授权密钥，可为其指定位置，比如想让anon存在于/etc下，这里的就换成/etc/anon
# with TelegramClient('anon', api_id, api_hash) as client:
#     # 代码中的me为收信人的用户名，Hello, myself!为发送内容。比如想给用户名为@vay，发送一句hello world。这里就替换成('@vay', 'hello world')
#     client.loop.run_until_complete(client.send_message('@dmtgrobot', 'Hello, myself!'))
#     client.loop.run_until_complete(client.)


client = TelegramClient('anon', api_id, api_hash)

file_path = '/tmp/sg.mp4'
# path = '/tmp/qbt.mp4'

async def main(file_path):
    # await client.send_file('@dmtgrobot', path, video_note=True, supports_streaming=True, attributes=(DocumentAttributeVideo(1440, 720,720),))
    # await client.send_file("@dmtgrobot", path, supports_streaming=True, attributes=(DocumentAttributeVideo(6*60+42, 1920, 1080),))
    # await client.send_file('@dmtgrobot', path, allow_cache=False,supports_streaming=True, attributes=(DocumentAttributeVideo(1440, 720,720),))
    await client.send_file('@dmtgrobot', file_path, allow_cache=False, supports_streaming=True)


with client:
    client.loop.run_until_complete(main(file_path))
