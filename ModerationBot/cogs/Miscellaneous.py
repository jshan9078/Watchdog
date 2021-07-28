from replit import db
import discord
from discord.ext import commands
import random
from random import choice

class Miscellaneous(commands.Cog):

  def __init__(self, client):
    self.client = client

  #ping command
  @commands.command()
  async def ping(self, ctx):
    await ctx.send(f'```Current Ping: {round(self.client.latency*1000)} ms```')

  """
  #auto responder
  @commands.Cog.listener()
  async def on_message(self, message):
    selfmatches = db.prefix("u"+str(message.author.id))
    if len(selfmatches)==0 and message.author.bot==False:
      db["u"+str(message.author.id)]="$0,#0,&0"
    db["s"+str(message.guild.id)] = str(message.guild.id)
    matches = db.prefix("s"+str(message.guild.id)+"ls")
    if (message.author.bot and len(matches)==1):
      current_count_messages = int(db["s"+str(message.guild.id)+"bot"])
      db["s"+str(message.guild.id)+"bot"] = str(current_count_messages+1)
    if (len(matches)==1):
      current_count_messages = int(db["s"+str(message.guild.id)+"messages"])
      db["s"+str(message.guild.id)+"messages"] = str(current_count_messages+1)
  """

  #8ball
  @commands.command(aliases=['8ball'])
  async def eightball(self, ctx, *, question):
    responses = ["It is certain.",
          "It is decidedly so.",
          "Without a doubt.",
          "Yes - definitely.",
          "You may rely on it.",
          "As I see it, yes.",
          "Most likely.",
          "Outlook good.",
          "Yes.",
          "Signs point to yes.",
          "Reply hazy, try again.",
          "Ask again later.",
          "Better not tell you now.",
          "Cannot predict now.",
          "Concentrate and ask again.",
          "Don't count on it.",
          "My reply is no.",
          "My sources say no.",
          "Outlook not so good.",
          "Very doubtful."]
    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}')
  
  @eightball.error
  async def ball_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include a question for the almighty 8ball to answer.```")

  #servercount
  @commands.command()
  async def membercount(self, ctx):
    server = self.client.get_guild(ctx.guild.id)
    await ctx.send(f'Member Count: {server.member_count}')

def setup(client):
  client.add_cog(Miscellaneous(client))
