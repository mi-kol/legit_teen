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

                if message.channel.name == 'teenagers' and message.author.name != 'Tatsumaki#8792' and message.author != bot.user and bot.user not in message.mentions and not message.content.startswith('t!'):

                    text.append(message.content)

            print('Successfully loaded', len(text), 'messages')

        if bot.user in message.mentions:
            reply = markovify.NewlineText('\n'.join(text), state_size = 1).make_sentence()
            if message.channel.name == 'bot_commands':
            # (old) added this line so only works in bot commands
                if 'restart' in message.content.lower() and message.author.name == "khsunny786#7666":
                    os.exec*()
                    # await bot.send_message(message.channel, 'I am a real teenager. Why would you want any help?\nAnyway, I can make up sentences with the stuff you say here, and act like I came from a specific subreddit when you write `be_like <subreddit>`.')
                    # return

                elif 'dmk' in message.content.lower():
                    # added by request of sunny. when tagged with DMK, it will tag three random people.
                    selected = []
                        
                    for x in range(0, 3):
                        selected.append(random.choice(members))

                    await bot.send_message(message.channel, tag(selected[0]) + " " + tag(selected[1]) + tag(selected[2]))
                    return
            
                else:
                    print('\t<Legit Teenager> ', reply)
                    await bot.send_message(message.channel, reply)
                    # (old) [CHANGE REVERSED] changed this just for kicks
            else:
                return
            # (old) added this in conjunction with if statement above to make sure only bot-commands can use it
        else:
            text.extend(filtered([message]))


try:

    bot.run('MjExNTc4MDQ3MDkzMDE0NTI5.CofW7Q.h0jCedeWCouTkcj5F9esOdiHnb8')
    # DO NOT UNCOMMENT bot.run('MjQwMTg1MzQ2ODc5NTIwNzcw.Cu_ppg.d3GoatugzCK3aV_PKmk8yB0SS8w')

except:

    with open('saved.txt', 'w') as session:
        session.write('\n\n'.join(text))

