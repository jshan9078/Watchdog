from replit import db
import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import find
from datetime import datetime #reminders
from dateutil.relativedelta import relativedelta
from main import DurationConverter, display_time, server_prefix

class Configuration(commands.Cog):

  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def prefix(self,ctx):
    x = server_prefix(ctx)
    await ctx.send(f"```Current Prefix for Watchdog: {x}```")

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def interval(self,ctx,duration: DurationConverter):
    h,d,mo,y,w,m,s=duration
    matches = db.prefix("s"+str(ctx.guild.id)+"ls")
    if len(matches)==1:
      send_to=int(db["s"+str(ctx.guild.id)+"ls"])
      channel = self.client.get_channel(send_to)
      current = datetime.now()
      date_time_obj=current.strftime("%Y-%m-%d %H:%M:%S")
      delta = relativedelta(hours=h, days=d, months=mo, years=y, weeks=w, minutes=m, seconds=s)
      new = current+delta
      tdelta=new-datetime.now()
      the_last=display_time(tdelta.total_seconds()+1, 4)
      new=new.strftime("%Y-%m-%d %H:%M:%S")
      new_value=str(new)+","+str(db["s"+str(ctx.guild.id)+"ls"])+","+str(h)+","+str(d)+","+str(mo)+","+str(y)+","+str(w)+","+str(m)+","+str(s)
      db["i"+str(ctx.guild.id)]=str(new_value)
      matchess = db.prefix("s"+str(ctx.guild.id)+"leave")
      matches2 = db.prefix("s"+str(ctx.guild.id)+"join")
      matches3 = db.prefix("s"+str(ctx.guild.id)+"messages")
      matches4 = db.prefix("s"+str(ctx.guild.id)+"bot")
      matches5= db.prefix("s"+str(ctx.guild.id)+"peakusers")
      if len(matchess)==1 and len(matches2)==1 and len(matches3)==1 and len(matches4)==1 and len(matches5)==1:
        forleave=db["s"+str(ctx.guild.id)+"leave"]
        forjoin=db["s"+str(ctx.guild.id)+"join"]
        formessage=db["s"+str(ctx.guild.id)+"messages"]
        forbotmessage=db["s"+str(ctx.guild.id)+"bot"]
        forpeakusers=db["s"+str(ctx.guild.id)+"peakusers"]
        await channel.send(f'`Time (UTC): {date_time_obj}, Total Messages: {formessage}, Most # of people online: {forpeakusers}, # of Members who joined: {forjoin}, # of Members who left: {forleave}, # of Messages from Bots: {forbotmessage}, # of Messages from Users: {str(int(formessage)-int(forbotmessage))}\nNext Update at {str(new)}`')
        await ctx.send(f"```Successfully changed your server's interval time between live stat updates: {the_last}```")
        db["s"+str(ctx.guild.id)+"leave"]="0"
        db["s"+str(ctx.guild.id)+"join"]="0"
        db["s"+str(ctx.guild.id)+"messages"]="0"
        db["s"+str(ctx.guild.id)+"bot"]="0"
        db["s"+str(ctx.guild.id)+"peakusers"]="0"
    else:
      await ctx.send("```Please select a channel to send the live updates to before using this command. To choose a channel for live updates, use the livestats command under the configuration section.```")
    

  @interval.error
  async def interval_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send(f"```Please provide the amount of time you want in between live stat updates.```")
    elif isinstance(error,commands.BadArgument):
      await ctx.send(f"```Please provide a valid duration.```")
    
  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def confighelp(self,ctx):
    x = server_prefix(ctx)
    
    embed=discord.Embed(title="Thanks for having me :)", description="I am a moderation bot making it easier to manage your server.", color=0x34b4eb)
    
    embed.set_author(name="Watchdog#4044",icon_url=self.client.user.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)

    embed.add_field(name="Choose your General Channel",value=f"`{x}general [channel]` \n e.g) {x}general #main, {x}general #833036832785694751", inline=False)

    embed.add_field(name="Choose your Logs Channel",value=f"`{x}logs [channel]` \n  e.g) {x}logs #serverlogs, {x}logs #833036832785694751", inline=False)

    embed.add_field(name="Choose your Live Stats Channel",value=f"`{x}livestats [channel]` \n  e.g) {x}livestats #stats, {x}livestats #833036832785694751", inline=False)

    embed.add_field(name="For more info...",value=f"`{x}help`", inline=False)

    embed.set_footer(text="Thanks for using Watchdog.")
    await ctx.send(embed=embed)


  @commands.command()
  @commands.has_permissions(manage_channels=True)
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
    await ctx.send(f'**General Channel: {general} \nLogs Channel: {logs} \nServer Stats Channel: {stats}**')

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def general(self,ctx,chat: commands.TextChannelConverter):
    new_general=chat
    db["s"+str(ctx.guild.id)+"g"] = str(new_general.id)
    matches = db.prefix("s"+str(ctx.guild.id)+"g")
    for i in range(len(matches)):
      print(matches[i],db[matches[i]])
    await ctx.send(f"**Your server's general chat is now {new_general.mention}\nID: {new_general.id} **")

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def logs(self,ctx,chat: commands.TextChannelConverter):
    new_general=chat
    db["s"+str(ctx.guild.id)+"l"] = str(new_general.id)
    matches = db.prefix("s"+str(ctx.guild.id)+"l")
    for i in range(len(matches)):
      print(matches[i],db[matches[i]])
    await ctx.send(f"**Your server's logs channel is now {new_general.mention}\nID: {new_general.id} **")

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def livestats(self,ctx,chat: commands.TextChannelConverter):
    new_general=chat
    db["s"+str(ctx.guild.id)+"ls"] = str(new_general.id)
    db["s"+str(ctx.guild.id)+"join"] = "0"
    db["s"+str(ctx.guild.id)+"messages"] = "0"
    db["s"+str(ctx.guild.id)+"leave"] = "0"
    db["s"+str(ctx.guild.id)+"peakusers"]="0"
    current = datetime.now()
    delta = relativedelta(seconds=10)
    new = current+delta
    new=new.strftime("%Y-%m-%d %H:%M:%S")
    new_value=str(new)+","+str(db["s"+str(ctx.guild.id)+"ls"])+",1,0,0,0,0,0,0"
    db["i"+str(ctx.guild.id)]=str(new_value)
    db["s"+str(ctx.guild.id)+"bot"] = "0"
    matches = db.prefix("s"+str(ctx.guild.id)+"ls")
    for i in range(len(matches)):
      print(matches[i],db[matches[i]])
    await ctx.send(f"**Your server's live stats channel is now {new_general.mention}\nID: {new_general.id}\nYour server will get live updates every 1 hour. If you want to change the timing, use the interval command in the configuration section.**")

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def setprefix(self,ctx,new_prefix):
    with open('prefix.json','r') as f:
        prefix=json.load(f)
      
    prefix[str(ctx.guild.id)] = new_prefix

    with open('prefix.json','w') as f:
      json.dump(prefix,f,indent=4)

    await ctx.send(f"```Successfully changed prefix to {new_prefix}```")
  
  @setprefix.error
  async def setprefix_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the prefix you would like to set as your server's prefix for Watchdog.```")

  @general.error
  async def general_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the channel you would like to set as your server's general channel.```")
    elif isinstance(error,commands.ChannelNotFound):
      await ctx.send("```Please include a valid channel you would like to set as your server's general channel.```")
    
  @logs.error
  async def logs_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the channel you would like to set as your server's logs channel.```")
    elif isinstance(error,commands.ChannelNotFound):
      await ctx.send("```Please include a valid channel you would like to set as your server's logs channel.```")
  
  @livestats.error
  async def livestats_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the channel you would like to set as your server's live stats channel.```")
    elif isinstance(error,commands.ChannelNotFound):
      await ctx.send("```Please include a valid channel you would like to set as your server's live stats channel.```")

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    db["s"+str(guild.id)] = str(guild.id)
    with open('prefix.json','r') as f:
      prefix=json.load(f)
    
    prefix[str(guild.id)] = '+'

    with open('prefix.json','w') as f:
      json.dump(prefix,f,indent=4)

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