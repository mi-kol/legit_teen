from collections import deque
import logging

import discord
import markovify



text = deque(maxlen = 2 ** 16)
logging.basicConfig(level = logging.INFO)

bot = discord.Client()

def filtered(messages):

    for message in messages:

        if message.channel.name == 'general' and message.author != 'Tatsumaki#8792' and message.author != bot.user and bot.user not in message.mentions and not message.content.startswith('t!') and not message.content.startswith('be_like '):

            yield message.content

loaded = False


@bot.event
async def on_ready():
    await bot.change_status(discord.Game(name='like a real teenager'))


@bot.event
async def on_message(message):
    global loaded
    if not loaded:

        async for message in bot.logs_from(discord.Object(id='235888301930708992'), limit = 1024):

            if message.channel.name == 'general' and message.author != 'Tatsumaki#8792' and message.author != bot.user and bot.user not in message.mentions and not message.content.startswith('t!'):

                text.append(message.content)

        print('Successfully loaded', len(text), 'messages')
        loaded = True

    if message.author != bot.user:

        if bot.user in message.mentions and message.channel.name == 'bot_commands':

            reply = markovify.NewlineText('\n'.join(text), state_size=1).make_sentence()
            if reply:

                print('\t<Legit Teen> ', reply)
                await bot.send_message(message.channel, reply)

        else:
            if message.channel.name == 'general':
                text.extend(filtered([message]))


try:

    bot.run("yodelalaeehu")

except:

    with open('saved.txt', 'w') as session:
        session.write('\n\n'.join(text))
