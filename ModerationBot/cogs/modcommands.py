import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class Moderation(commands.Cog):

  def __init__(self, client):
    self.client = client

  #purge commands
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def clear(self,ctx, *, inp: int):
    await ctx.channel.purge(limit=inp)


  @clear.error
  async def clear_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include how many messages you wish to delete.```")
  

  #kick
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member,*,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Reason of Kick: {reason}')

  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the user you wish to kick.```")

  #ban
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member,*,reason=None):
    # guild = self.client.get_guild()
    guild = self.client.get_guild(ctx.guild.id)
    if guild.get_member(member.id) is not None: 
      await member.ban(reason=reason)
      await ctx.send(f'Banned {member.mention}')
    else:
      await ctx.send("Member Doesnt Exist")

  @ban.error
  async def ban_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the user you wish to ban.```")
    
  #unban
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    i=0
    for ban_entry in banned_users:
      user1 = ban_entry.user
      if str(user1)==str(member):
        print("breh")
      i+=1
    print(i)
    #except discord.NotFound:
      #await ctx.send('```The user is not banned.```')
      #return
    
    # for ban_entry in banned_users:
      # user = ban_entry.user
      # if (user.name, user.discriminator) == (member_name, # member_discriminator):
        # await ctx.guild.unban(user)
        # await ctx.send(f'Unbanned {user.mention}')
    # await ctx.send("```User is not banned.```")

  @unban.error
  async def unban_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the user you wish to unban.```")

  #nickname changes
  @commands.command()
  @commands.has_permissions(manage_nicknames=True)
  async def nick(self, ctx,member: discord.Member,*,nick):
      await member.edit(nick=nick)
      await ctx.send(f'Changed nickname for {member.mention}')

  @nick.error
  async def nick_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the user or nickname as well.```")

def setup(client):
  client.add_cog(Moderation(client))