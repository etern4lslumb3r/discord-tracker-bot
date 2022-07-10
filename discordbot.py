# Outline [To do list]
# IMPORTANT

# 1) Implement a movie queue.
# 2) Implement link grabber for Sflix.to site.
# 3) Gametime Notifier (Will periodically send a message notifiying server X player's daily time in-game)
# 4) Activity Change Notifier (Will send author a message whenever the target changes their discord activity)
#
# OPTIONAL
# 1) ...
# 2) ...

import discord
from datetime import datetime
import time
from threading import Thread
import os

intents = discord.Intents().default()
intents.members = True
intents.presences = True
intents.messages = True
intents.dm_messages = True

client = discord.Client(intents=intents)


def reset_member_update_list():
    global member_updates
    while True:
        time.sleep(5)
        member_updates = []


@client.event
async def on_ready():
    global member_updates
    print("{} has connected".format(client.user))

previous_target = ""


@client.event
async def on_message(message):
    global state, target, author

    if message.author == client.user:
        return

    if message.content == "!sh":
        help = "```!sh - Help Screen```"\
               "```!s {username#identifier} - Tracks the discord activity of the person, and sends updates in this chat.```"\
               "```!ds - Stops the tracking of a user.```"
        await message.channel.send(help)

    if message.content.startswith("!s "):
        guilds = client.guilds
        users = set()
        for guild in guilds:
            for member in guild.members:
                if not member.bot:
                    users.add("{}#{}".format(
                        member.name, member.discriminator))
        print(users)
        try:
            state = True
            target = message.content.split()[1].strip()
            author = message.author
            if target in users:
                await message.channel.send(f"```Tracking {target}...```")
            else:
                await message.channel.send(f"```User {target} not found...```")
        except:
            await message.channel.send(f"```Invalid Input```")

    if message.content.strip() == "!sd":
        state = False
        #target = message.content.split()[1]
        author = message.author
        try:
            previous_target = target
            await message.channel.send(f"```No longer Tracking {previous_target}...```")
        except:
            await message.channel.send(f"```Currently not Tracking```")

# SEND DM TO BOT TO SWITCH ON OR OFF
# DETECTS IF USER ACTIVITY CHANGE IS DETECTED OR WHATEVER


@client.event
async def on_member_update(before, after):
    if before.id in member_updates:
        return
    member_updates.append(before.id)
    print(before.name)
    if state == True:
        name = target.split("#")[0]
        identifier = target.split("#")[1]
        new = f"{name}#{identifier}"
        if f"{before.name}#{before.discriminator}" == new:
            try:
                old_activity = before.activity.name
            except:
                old_activity = before.activity
            try:
                new_activity = after.activity.name
            except:
                new_activity = after.activity

            recipient = client.get_user(author.id)
            await recipient.send(f"```Activity Changed!\nPrevious Activity: {old_activity}\nNew Current Activity: {new_activity}```")
            #last_message = [message async for message in recipient.history(limit=1) if message.author == client.user][0]
            #await last_message.delete()
    if state == False:
        pass

if __name__ == "__main__":
    member_update_list_reset = Thread(target=reset_member_update_list)
    member_update_list_reset.start()
    client.run(os.environ["TOKEN"])
