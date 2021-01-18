# -*- coding: utf-8 -*-

import asyncio
import logging
import aiohttp
from telethon import TelegramClient, events
import config as cfg

# Create logger
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
# Create file handler which logs even debug messages
fh = logging.FileHandler('main.log')
fh.setLevel(logging.INFO)
# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Global Variables
track = False

# Constants
URL = 'https://crossfire.crypto.com/block'
VALIDATOR_ADDRESS = ''
TIME_BETWEEN_CHECKS = 60  # Time in seconds to wait before next check
CHECKS_TO_FAIL = 5 # Number of consecutive checks that failed before notification
ADMIN = int(cfg.data['admin']) # Your own user id

try:
    bot = TelegramClient('crossfire-bot', cfg.data['telegram_api_id'], cfg.data['telegram_api_hash']).start(bot_token=cfg.data['telegram_bot_token'])
except:
    logger.error('Error when opening API', exc_info=True)


async def main():
    async with bot as client:
        @client.on(events.NewMessage(pattern='/start'))
        async def start(event):
            try:
                await event.respond('Hi, your user id is: {}'.format(event.message.sender_id))
            except:
                logger.error('Error!', exc_info=True)

        @client.on(events.NewMessage(pattern='/amisigning'))
        async def amisigning(event):
            try:
                # Only admin can use command
                if event.message.sender_id == ADMIN:
                    if VALIDATOR_ADDRESS == '':
                        await event.respond('Please enter your validator address first')
                    else:
                        sign = await signing_check(VALIDATOR_ADDRESS)
                        await event.respond('Address: {} \nSigning: {}'.format(VALIDATOR_ADDRESS, sign))
            except:
                logger.error('error', exc_info=True)

        @client.on(events.NewMessage(pattern='/track'))
        async def settrack(event):
            try:
                # Only admin can use command
                if event.message.sender_id == ADMIN:
                    if VALIDATOR_ADDRESS == '':
                        await event.respond('Please enter your validator address first')
                    else:
                        await event.respond('Start tracking')
                        global track
                        track = True
            except:
                logger.error('error', exc_info=True)

        @client.on(events.NewMessage(pattern='/stoptrack'))
        async def stoptrack(event):
            try:
                # Only admin can use command
                if event.message.sender_id == ADMIN:
                    global track
                    track = False
                    await event.respond('Stopped tracking')
            except:
                logger.error('error', exc_info=True)

        logger.info('Service is running.')
        await check_validator()
        await client.run_until_disconnected()


async def signing_check(address):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request("GET", URL) as response:
                block = await response.content.read()
                block = block.decode()
        return 'Yes' if address in block else 'No'
    except:
        logger.error('error', exc_info=True)


async def check_validator():
    failed = 0
    while 1:
        try:
            if track:
                async with aiohttp.ClientSession() as session:
                    async with session.request("GET", URL) as response:
                        block = await response.content.read()
                        block = block.decode()
                    if VALIDATOR_ADDRESS in block:
                        failed = 0
                    else:
                        failed = failed + 1
                        if failed >= CHECKS_TO_FAIL:
                            await bot.send_message(ADMIN, 'Not signing! Use /stoptrack to stop')
            await asyncio.sleep(TIME_BETWEEN_CHECKS)
        except:
            logger.error('error', exc_info=True)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
