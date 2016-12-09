from collections import deque
import logging

import discord
import markovify
import random
import asyncio
import schedule
import time
import os




text = deque(maxlen = 2 ** 16)
logging.basicConfig(level = logging.INFO)

bot = discord.Client()
members = []

def tag(id):
    """Convert standard id number into a tag that will ping someone."""
    return "<@!" + id + ">"

def refreshPeople():
    global members
    for member in bot.get_all_members():
        members.append(member.id)

schedule.every().day.at("12:00").do(refreshPeople)

def filtered(messages):
    """Filter bot input so other bots don't interfere"""

    for message in messages:

        if message.channel.name == 'teenagers' and message.author.name != 'Tatsumaki#8792' and message.author != bot.user and bot.user not in message.mentions and not message.content.startswith('t!') and not message.content.startswith('be_like '):

            yield message.content

loaded = False

@bot.event
async def on_ready():
    """Manage bot status"""
    refreshPeople()
    await bot.change_status(discord.Game(name = 'like a real teenager'))

@bot.event
async def on_message(message):
    """Parse input from discord channel Bot Commands"""
    global loaded
    global members


    if message.channel.name == 'bot_commands' and message.author != bot.user:
        if not loaded:

            loaded = True
            logs = bot.logs_from(message.channel, limit = 256)
            async for message in logs:

                if message.channel.name == 'general' and message.author.name != 'Tatsumaki#8792' and message.author != bot.user and bot.user not in message.mentions and not message.content.startswith('t!'):

                    text.append(message.content)

            print('Successfully loaded', len(text), 'messages')

        if bot.user in message.mentions:
            reply = markovify.NewlineText('\n'.join(text), state_size = 1).make_sentence()
            if message.channel.name == 'bot_commands':
            # (old) added this line so only works in bot commands
                print('\t<Legit Teenager> ', reply)
                await bot.send_message(message.channel, reply)
                # (old) [CHANGE REVERSED] changed this just for kicks
            else:
                return
            # (old) added this in conjunction with if statement above to make sure only bot-commands can use it
        else:
            text.extend(filtered([message]))


try:

    bot.run(token)

except:

    with open('saved.txt', 'w') as session:
        session.write('\n\n'.join(text))

