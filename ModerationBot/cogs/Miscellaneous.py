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

  #auto responder
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.content.find("hello") != -1:
      await message.channel.send("hi")
    

  #8ball
  @commands.command(aliases=['8ball', 'eightball'])
  async def _8ball(self, ctx, *, question):
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
  
  @_8ball.error
  async def ball_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include a question for the almighty 8ball to answer.```")

  #servercount
  @commands.command()
  async def membercount(self, ctx):
    server = self.client.get_guild(ctx.guild.id)
    await ctx.send(f'Member Count: {server.member_count}')

  #embed practice
  #leave the 0x
  @commands.command()
  async def club(self, ctx):
    embed=discord.Embed(title="Campbell Computer Club", url="https://docs.google.com/presentation/d/1EOvTDZXKI4qirtObM23YAqIgDhQRtZgh15mxYroO1cQ/edit?usp=sharing", description="A club with a focus on expanding your knowledge of the applications of computer science.", color=0x34b4eb)
    embed.set_image(url="https://media.discordapp.net/attachments/833036832785694751/845670874967179304/unknown.png?width=1040&height=586")
    embed.set_author(name=ctx.author.display_name + "#" +ctx.author.discriminator, url="",icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/833036832785694751/845670699116134410/unknown.png")
    embed.add_field(name="Competitive Coding", value="We prepare you for the Canadian Computing Competition and host club-wide contests.", inline=False)
    embed.add_field(name="Unity", value="We cover game development with Unity.", inline=True)
    embed.add_field(name="Web Dev",value="Brief HTML CSS basics are covered.", inline=True)
    embed.add_field(name="Discord Bots",value="We also show discord bots with discord.py", inline=True)
    embed.add_field(name="Club-Wide Server",value="{}, Click here to join our official discord server.  https://discord.gg/gK5apkeZNk".format(ctx.author.display_name,ctx.author.display_name), inline=False)
    embed.set_footer(text="We hope you check it out.")
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Miscellaneous(client))
