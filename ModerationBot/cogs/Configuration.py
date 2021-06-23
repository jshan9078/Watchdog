from replit import db
import discord
from discord.ext import commands
import random
from random import choice
from discord.utils import find

class Configuration(commands.Cog):

  def __init__(self, client):
    self.client = client
  
  print(db.keys())

  @commands.command()
  async def config(self,ctx):
    matches = db.prefix("s"+str(ctx.guild.id))
    general="Not Set"
    logs="Not Set"
    stats="Not Set"
    for i in range(len(matches)):
      if (matches[i]=="s"+str(ctx.guild.id)+"g"):
        for channel in ctx.guild.channels:
          if channel.id == int(db[matches[i]]):
              general=channel.mention
              break
      elif (matches[i]=="s"+str(ctx.guild.id)+"ls"):
        for channel in ctx.guild.channels:
          if channel.id == int(db[matches[i]]):
              stats=channel.mention
              break
      elif (matches[i]=="s"+str(ctx.guild.id)+"l"):
        for channel in ctx.guild.channels:
          if channel.id == int(db[matches[i]]):
              logs=channel.mention
              break
    await ctx.send(f'**General Channel: {general} \n Logs Channel: {logs} \n Server Stats Channel: {stats}**')

  @commands.command()
  async def general(self,ctx,*,chat):
    new_general=chat
    if len(chat)>18:
      new_general=new_general[2:-1]
    new_chat=chat
    if len(chat)==18: 
      for channel in ctx.guild.channels:
        if channel.id == int(new_chat):
            new_chat=channel.mention
            break
    db["s"+str(ctx.guild.id)+"g"] = str(new_general)
    matches = db.prefix("s"+str(ctx.guild.id)+"g")
    for i in range(len(matches)):
      print(matches[i],db[matches[i]])
    await ctx.send(f"**Your server's general chat is now {new_chat}\n ID: {new_general} **")

  @commands.command()
  async def logs(self,ctx,*,chat):
    new_general=chat
    if len(chat)>18:
      new_general=new_general[2:-1]
    new_chat=chat
    if len(chat)==18:
      for channel in ctx.guild.channels:
        if channel.id == int(new_chat):
            new_chat=channel.mention
            break
    db["s"+str(ctx.guild.id)+"l"] = str(new_general)
    matches = db.prefix("s"+str(ctx.guild.id)+"l")
    for i in range(len(matches)):
      print(matches[i],db[matches[i]])
    await ctx.send(f"**Your server's logs channel is now {new_chat}\n ID: {new_general} **")

  @commands.command()
  async def livestats(self,ctx,*,chat):
    new_general=chat
    if len(chat)>18:
      new_general=new_general[2:-1]
    new_chat=chat
    if len(chat)==18:
      for channel in ctx.guild.channels:
        if channel.id == int(new_chat):
            new_chat=channel.mention
            break
    db["s"+str(ctx.guild.id)+"ls"] = str(new_general)
    matches = db.prefix("s"+str(ctx.guild.id)+"ls")
    for i in range(len(matches)):
      print(matches[i],db[matches[i]])
    await ctx.send(f"**Your server's live stats channel is now {new_chat}\n ID: {new_general} **")
  
  @general.error
  async def general_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the channel you would like to set as your server's general chat.```")

  @logs.error
  async def logs_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the channel you would like to set as your server's logs channel.```")
  
  @livestats.error
  async def livestats_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the channel you would like to set as your server's live stats chat.```")

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    db["s"+str(guild.id)] = str(guild.id)
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
      embed=discord.Embed(title="Thanks for having me :)", description="I am a moderation bot making it easier to manage your server.", color=0x34b4eb)
    
      embed.set_author(name="Watchdog#4044",icon_url=self.client.user.avatar_url)
      embed.set_thumbnail(url=guild.icon_url)

      embed.add_field(name="Choose your General Channel (current channel is default)",value="`+general [channel]` \n e.g) +general #main, +general #833036832785694751", inline=False)

      embed.add_field(name="Choose your Logs Channel",value="`+logs [channel]` \n  e.g) +logs #serverlogs, +logs #833036832785694751", inline=False)

      embed.add_field(name="Choose your Live Stats Channel",value="`+livestats [channel]` \n  e.g) +livestats #stats, +livestats #833036832785694751", inline=False)

      embed.add_field(name="For more info...",value="`+help`", inline=False)

      embed.set_footer(text="Thanks for using Watchdog.")
      await general.send(embed=embed)

    print(db.keys())

  
def setup(client):
  client.add_cog(Configuration(client))
