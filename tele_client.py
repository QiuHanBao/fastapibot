from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
from setting import api_id, api_hash, TOKEN

bot_token = TOKEN
api_id = api_id  # 申请的TG API ID
api_hash = api_hash  # 申请的TG API hash


# file_path = '/tmp/sg.mp4'
# path = '/tmp/qbt.mp4'

async def main(client, file_path):
    # await client.send_file('@dmtgrobot', path, video_note=True, supports_streaming=True, attributes=(DocumentAttributeVideo(1440, 720,720),))
    # await client.send_file("@dmtgrobot", path, supports_streaming=True, attributes=(DocumentAttributeVideo(6*60+42, 1920, 1080),))
    # await client.send_file('@dmtgrobot', path, allow_cache=False,supports_streaming=True, attributes=(DocumentAttributeVideo(1440, 720,720),))
    await client.send_file('@dmtgrobot', file_path, allow_cache=False, supports_streaming=True)


# with client:
def run(file_path):
    client = TelegramClient('anon', api_id, api_hash)
    client.loop.run_until_complete(main(client, file_path))
