from replit import db
import discord
from discord.ext import commands
import random
from random import choice
from discord.utils import find

class serverjoin(commands.Cog):

  def __init__(self, client):
    self.client = client
  
  print(db.keys())

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    db[str(guild.id)] = str(guild.id)
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
      embed=discord.Embed(title="Thanks for having me :)", description="I am a moderation bot making it easier to manage your server.", color=0x34b4eb)
    
      embed.set_author(name="Watchdog#4044",icon_url=self.client.user.avatar_url)
      embed.set_thumbnail(url=guild.icon_url)

      embed.add_field(name="Choose your General Channel (current channel is default)",value="`v!general [channel]`", inline=False)

      embed.add_field(name="Choose your Logs Channel",value="`v!logs [channel]`", inline=False)

      embed.add_field(name="Choose your Live Stats Channel",value="`v!livestats [channel]`", inline=False)

      embed.add_field(name="For more info...",value="`v!help`", inline=False)

      embed.set_footer(text="Thanks for using Watchdog.")
      await general.send(embed=embed)

    print(db.keys())


  
def setup(client):
  client.add_cog(serverjoin(client))
