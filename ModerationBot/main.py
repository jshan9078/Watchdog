import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
from random import choice
import asyncio
import os
from datetime import datetime #reminders

my_secret = os.environ['token']
intents = discord.Intents.all()
client =  commands.Bot(command_prefix = 'v!', intents=intents)

for filename in os.listdir('ModerationBot/cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

#use dictionaries for rank, name, role
#global variables
messages = 0
joined = 0
left = 0

servercount = int(os.environ['sc'])

d = os.environ['sd'].split(",")

serverdata = [[0 for x in range(4)] for y in range(servercount)] 

wcord = 0
hcord = 0

for i in range(len(d)):
  serverdata[wcord][hcord]=d[i]
  serverdata[wcord][hcord] = int(serverdata[wcord][hcord])
  hcord+=1
  if (hcord==4):
    hcord=0
    wcord+=1


#change ids as seen fit
<<<<<<< HEAD
livelogs_private = int(os.environ['livelogsprivate'])

global finder2
def finder2(message,channel):
  for i in range(servercount):
    if (serverdata[i][0]==message.guild.id):
      if (channel=="logs"):
        return serverdata[i][2]
      elif (channel=="livelogs"):
        return serverdata[i][3]
      elif (channel=="guild"):
        return serverdata[i][0]
      else:
        return serverdata[i][1]
=======
livelogs_private = 847569900435931207

global finder
def finder(message, channel):
    with open ("ModerationBot/servers",'r') as f:
      lines = f.readlines()
      for i in range(len(lines)):
        currentLines = lines[i].strip()
        if (int(currentLines[0:18])==message.guild.id):
          if (channel=="logs"):
            return int(currentLines[38:56])
          elif (channel=="livelogs"):
            return int(currentLines[57:75])
          elif (channel=="guild"):
            return int(currentLines[0:18])
          else:
            return int(currentLines[19:37])
>>>>>>> 9d37e8b6bd51edbed39cfabfd754534766bc54ce

#bot active
@client.event
async def on_ready(): 
  await client.change_presence(status=discord.Status.idle, activity=discord.Game('Trying to program, but failing :D'))
  print('Bot is Ready.')

#error handling for invalid commands
@client.event
async def on_command_error (ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("```The command you tried doesn't exist.```")
  elif isinstance(error,commands.MissingPermissions):
    await ctx.send("```You don't have permission to do that.```")

#join
# make embed
@client.event
async def on_member_join(member):
  global joined
  joined+=1
  channel = client.get_channel(finder2(member,"general"))
  await channel.send("Hey. Welcome.")

#leave
#make embed
@client.event
async def on_member_remove(member):
  global left
  left+=1
  channel = client.get_channel(finder2(member,"general"))
  await channel.send(f"{member} has left the server")

#log message sent

""""
@client.event
async def on_message(message):
  # embed=discord.Embed(title="Sent Message")
  # so it doesnt respond to itself
  if message.author.id != client.user.id:
    channel = client.get_channel(815098419730710528)
    await channel.send("Message Sent")

"""

#background tasks
async def update():
  await client.wait_until_ready()
  global messages, joined, left

  while not client.is_closed():

    try:

      current = datetime.now()
      currentDisplay = current.strftime("%d/%m/%Y %H:%M:%S")

      channel = client.get_channel(livelogs_private)
      await channel.send(f'`Time: {currentDisplay}, Messages: {messages}, Members Joined: {joined}, Members Who Left: {left}\n`')

      messages=0  
      joined=0
      left=0

      await asyncio.sleep(3600)

    except Exception as e:
      print(e)
      await asyncio.sleep(3600)

#display name = default
#discriminator = tag
#avatar_url = pfp
#message.author = sender
#.mention = ping
#get_channel = redirects message
#incorporate file deletion
@client.event
async def on_message_delete(message):
  embed=discord.Embed(title="Message Deleted", url="", description="", color=0xC75052)
  embed.set_author(name=message.author.display_name + "#" +message.author.discriminator, url="",icon_url=message.author.avatar_url)
  embed.add_field(name="**From**",value=f"{message.author.mention}", inline=True)
  embed.add_field(name="**Channel**",value=f'{message.channel.mention}', inline=True)
  embed.add_field(name="Content", value=message.content, inline=False)
  channel = client.get_channel(finder2(message,"logs"))
  await channel.send(embed=embed)

client.loop.create_task(update())
client.run(my_secret)