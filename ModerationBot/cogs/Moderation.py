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
  async def kick(self, ctx, member: commands.MemberConverter,*,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Reason of Kick: {reason}')

  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the user you wish to kick.```")
    elif isinstance(error,commands.MemberNotFound):
      await ctx.send("```Please provide a valid user to kick.```")

  #ban
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: commands.MemberConverter,*,reason=None):
    # guild = self.client.get_guild()
    guild = self.client.get_guild(ctx.guild.id)
    if guild.get_member(member.id) is not None: 
      await member.ban(reason=reason)
      await ctx.send(f'Banned {member.mention} \nReason: {reason}')
    else:
      await ctx.send("Member Doesnt Exist")

  @ban.error
  async def ban_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the user you wish to ban.```")
    elif isinstance(error,commands.MemberNotFound):
      await ctx.send("```Please provide a valid user to ban.```")
    
  #unban
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    i=0
    if (len(banned_users)==0):
      await ctx.send("```The user you tried to unban is not banned.```")
    for ban_entry in banned_users:
      user1 = ban_entry.user
      if str(user1)==str(member):
        await ctx.guild.unban(user1)
        await ctx.send(f'Unbanned {user1.mention}')
        break
      elif (i==len(banned_users)-1):
        await ctx.send("```The user you tried to unban is not banned.```")
        break
      i+=1

  @unban.error
  async def unban_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the user you wish to unban.```")

  #nickname changes
  @commands.command()
  @commands.has_permissions(manage_nicknames=True)
  async def nick(self, ctx,member: commands.MemberConverter,*,nick):
      await member.edit(nick=nick)
      await ctx.send(f'Changed nickname for {member.mention}')

  @nick.error
  async def nick_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("```Please include the user or nickname as well.```")
    elif isinstance(error,commands.MemberNotFound):
      await ctx.send("```Please provide a valid user to change their nickname.```")

def setup(client):
  client.add_cog(Moderation(client))