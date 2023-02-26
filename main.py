import os
import time
import datetime
import random
from weakref import finalize

import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio

import json

from discord import colour

os.system('cls')

with open('birth.json','r',encoding='utf-8') as birthF:
    birthData=json.load(birthF)

with open('config.json','r',encoding='utf-8') as configF:
    configData=json.load(configF)

client = discord.Client()

version="1.1.0"

def embNormal(data, describe, mode ,info, ver):
    norEmb=discord.Embed(title=data , description=describe, color=0x0abab5)
    norEmb.add_field(name="Time", value=datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), inline=True)
    norEmb.add_field(name=mode+":", value= info, inline=True)
    norEmb.add_field(name="Version", value=ver, inline=True)
    return norEmb

def embBirth(describe, text1, describe1):
    bdEmb=discord.Embed(title=f'Happy Birthday' , description=describe, color=0xfff37f)
    bdEmb.add_field(name="Today is", value=datetime.date.today().strftime("%Y/%m/%d"), inline=True)
    bdEmb.add_field(name=text1, value= describe1, inline=True)
    return bdEmb

@client.event
async def on_ready():
    print('>>>\t EVENT:\t', client.user,'is on the air !\t<<<')
    channel = client.get_channel(int(configData['logChannel']))
    await channel.send(embed=(embNormal('Hello World !', f'{client.user} is on the air !', 'Event', 'bot starting', version)))

@client.event
async def on_message(message):
    user=message.author

    if user==client.user:
        return
    
    if message.content=='$update':
    
        print('>>>\t EVENT:\t',user,'is updating birth info\t<<<')
        guild=message.guild
        await guild.create_role(name="commander")
        role=discord.utils.get(user.guild.roles, name="commander")
        member=message.author
        with open('config.json','r',encoding='utf-8') as configF:
            configData=json.load(configF)
        category=client.get_channel(int(configData['cmdCatergory']))
        try:
            await member.add_roles(role)
            channel = await guild.create_text_channel(f'{user} CMD channel',category=category)
            
        except AttributeError:
            print('>>>\t Error:\t Attribute Error\t<<<')
        finally:
            await role.delete()

@tasks.loop(seconds=60)
async def birthdatCelebrations():
    await client.wait_until_ready()
    with open('birth.json','r',encoding='utf-8') as birthF:
        birthData=json.load(birthF)
    with open('config.json','r',encoding='utf-8') as configF:
        configData=json.load(configF)
    with open('birthWishes.json','r',encoding='utf-8') as bWF:
        birthWData=json.load(bWF)
    length=len(birthWData)
    wishes=birthWData[str(random.randint(0,length*10000)%length)]
    now=datetime.datetime.now().strftime('%m/%d %H:%M')
    for date in birthData:
        if now==(birthData[date]+' 0:00'):
            print(f'>>>\t TASK:\t Send a birth celebration for {date} !\t<<<')
            celebrateChannel=client.get_channel(int(configData['celebrateChannel']))
            await celebrateChannel.send(embed=(embBirth('o((>w< ))o',f'{wishes}', f'<@{date}>')))

birthdatCelebrations.start()

client.run(configData['token'])