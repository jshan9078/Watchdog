from replit import db
import discord
from discord.ext import commands
from datetime import datetime #reminders
from dateutil.relativedelta import relativedelta
from main import DurationConverter, display_time

class Reminders(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def reminders(self,ctx):
    matches = db.prefix("r"+str(ctx.author.id))
    output=''
    for key in matches:
      print(db[key])
      broken=db[key].split(',')
      ID=str(key)[19:]
      notif=broken[-1]
      Location=''
      Expected_time=''

      if broken[0]=="dm":
        Location="Watchdog DM"
        Expected_time=[1]
      else:
        Location="<#"+broken[1]+">"
        Expected_time=[0]
      
      current = datetime.now()
      date_time_obj = datetime.strptime(Expected_time, '%Y-%m-%d %H:%M:%S')
      tdelta=date_time_obj-current
      the_last=display_time(tdelta.total_seconds()+1, 4)

      output+=f"**ID - {ID}** | Location: {Location}: {notif} - in {the_last} from now {Expected_time}\n"

    await ctx.send(output)
  

  @commands.command()
  async def remind(self,ctx,duration:DurationConverter,*,message):
    h,d,mo,y,w,m,s=duration
    current_count=int(db["totalreminders"])+1
    db["totalreminders"]=str(current_count)
    current = datetime.now()
    delta = relativedelta(hours=h, days=d, months=mo, years=y, weeks=w, minutes=m, seconds=s)
    new = current+delta
    tdelta=new-datetime.now()
    new=new.strftime("%Y-%m-%d %H:%M:%S")
    the_last=display_time(tdelta.total_seconds()+1, 4)
    new_value=str(new)+','+str(ctx.channel.id)+','+str(ctx.author.id)+','+message
    db["r"+str(ctx.author.id)+str(current_count)]=new_value
    await ctx.send(f"**Set a reminder for: **{the_last} from now ({str(new)} UTC)\n**Message: **{message}\nYou will be reminded in this channel.")

  @commands.command()
  async def dmremind(self,ctx,duration:DurationConverter,*,message):
    h,d,mo,y,w,m,s=duration
    current_count=int(db["totalreminders"])+1
    db["totalreminders"]=str(current_count)
    current = datetime.now()
    delta = relativedelta(hours=h, days=d, months=mo, years=y, weeks=w, minutes=m, seconds=s)
    new = current+delta
    tdelta=new-datetime.now()
    new=new.strftime("%Y-%m-%d %H:%M:%S")
    the_last=display_time(tdelta.total_seconds()+1, 4)
    new_value="dm,"+str(new)+','+str(ctx.author.id)+','+message
    db["r"+str(ctx.author.id)+str(current_count)]=new_value
    print(new_value)
    await ctx.send(f"**Set a reminder for: **{the_last} from now ({str(new)} UTC)\n**Message: **{message}\nYou will recieve the reminder in a direct message from Watchdog.")

  @remind.error
  async def remind_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send(f"```Please provide the amount of time before the reminder and a message you want in the reminder.```")
    elif isinstance(error,commands.BadArgument):
      await ctx.send(f"```Please provide a valid duration.```")
  
  @dmremind.error
  async def dmremind_error(self, ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send(f"```Please provide the amount of time before the reminder and a message you want in the reminder.```")
    elif isinstance(error,commands.BadArgument):
      await ctx.send(f"```Please provide a valid duration.```")

  

def setup(client):
  client.add_cog(Reminders(client))