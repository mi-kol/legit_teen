
m collections import deque
import logging

import discord
import markovify



text = deque(maxlen = 2 ** 16)
logging.basicConfig(level = logging.INFO)

bot = discord.Client()


def filtered(messages):

    for message in messages:

        if message.channel.name == 'teenagers' and message.author.name != 'Tatsumaki#8792' and message.author != bot.user and bot.user not in message.mentions and not message.content.startswith('t!') and not message.content.startswith('be_like '):

            yield message.content

loaded = False

@bot.event
async def on_ready():

    await bot.change_status(discord.Game(name = 'like a real teenager'))

@bot.event
async def on_message(message):
    global loaded


    if message.channel.name == 'teenagers' and message.author != bot.user:

        if not loaded:

            loaded = True
            logs = bot.logs_from(message.channel, limit = 256)
            async for message in logs:

                if message.channel.name == 'teenagers' and message.author.name != 'Tatsumaki#8792' and message.author != bot.user and bot.user not in message.mentions and not message.content.startswith('t!'):

                    text.append(message.content)

            print('Successfully loaded', len(text), 'messages')

        if bot.user in message.mentions:

            if 'help me' in message.content.lower():

                await bot.send_message(message.channel, 'I am a real teenager. Why would you want any help?\nAnyway, I can make up sentences with the stuff you say here, and act like I came from a specific subreddit when you write `be_like <subreddit>`.')
                return

            reply = markovify.NewlineText('\n'.join(text), state_size = 1).make_sentence()
            if reply:

                print('\t<Legit Teenager> ', reply)
                await bot.send_message(message.channel, reply)

        else:

            text.extend(filtered([message]))


try:

    bot.run('MjExNTc4MDQ3MDkzMDE0NTI5.CofW7Q.h0jCedeWCouTkcj5F9esOdiHnb8')

except:

    with open('saved.txt', 'w') as session:

session.write('\n\n'.join(text))
