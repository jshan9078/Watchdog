from replit import db
import discord
import json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import asyncio
import os
from datetime import datetime #reminders
from dateutil.relativedelta import relativedelta
from webserver import keep_on

my_secret = os.environ['token']
intents = discord.Intents.all()


def get_prefix(client, message):
  with open('prefix.json','r') as f:
    prefix = json.load(f)
  arr=[]
  arr.append(prefix[str(message.guild.id)])
  x= str(client.user.mention) + " " 
  y= str(client.user.mention)[:2] + "!" + str(client.user.mention)[2:] + " "
  arr.append(x)
  arr.append(y)
  return arr

def server_prefix(ctx):
  with open('prefix.json','r') as f:
    prefix = json.load(f)

  return prefix[str(ctx.guild.id)]

client =  commands.Bot(command_prefix = get_prefix, intents=intents)


def check_owner(ctx):
  if (ctx.author.id==620402532346232832 or ctx.author.id==800531315602227241 or ctx.author.id==555494011947974667):
    return True


global intervals, display_time
intervals = (
    ('weeks', 604800),  
    ('days', 86400),    
    ('hours', 3600),    
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:granularity])

@client.event
async def on_guild_remove(guild):
  del db["i"+str(guild.id)]
  with open('prefix.json','r') as f:
      prefix=json.load(f)
    
  prefix.pop(str(guild.id))

  with open('prefix.json','w') as f:
    json.dump(prefix,f,indent=4)

class DurationConverter(commands.Converter):
  async def convert(self,ctx,given):
    d=0
    w=0
    mo=0
    y=0
    h=0
    m=0
    s=0
    count0=given.count("0")
    count1=given.count("1")
    count2=given.count("2")
    count3=given.count("3")
    count4=given.count("4")
    count5=given.count("5")
    count6=given.count("6")
    count7=given.count("7")
    count8=given.count("8")
    count9=given.count("9")
    countd=given.count("d")
    countw=given.count("w")
    countmo=given.count("mo")
    county=given.count("y")
    counth=given.count("h")
    countm=given.count("m")-countmo
    counts=given.count("s")
    summm=count0+count1+count2+count3+count4+count5+count6+count7+count8+count9+countd+countw+countmo+county+counth+countm+counts
    if countmo==1:
      summm+=1
    timesum=countd+countw+countmo+county+counth+countm+counts
    fff=given[0]
    lll=given[-1]
    if summm==len(given) and countd<2 and countw<2 and countmo<2 and county<2 and counth<2 and countm <2 and counts<2 and timesum>0 and timesum<8 and fff.isdigit()==True and lll.isdigit()==False:
      sub=""
      for i in range(len(given)):
        if given[i].isdigit():
          sub+=given[i]
        else:
          if given[i]=="d":
            d=int(sub)
            sub=""
          elif given[i]=="w":
            w=int(sub)
            sub=""
          elif given[i]=="m":
            if i!=len(given)-1:
              if given[i+1]=="o":
                mo=int(sub)
                sub=""
              else:
                m=int(sub)
                sub=""
            else:
              m=int(sub)
              sub=""
          elif given[i]=="y":
            y=int(sub)
            sub=""
          elif given[i]=="h":
            h=int(sub)
            sub=""
          elif given[i]=="s":
            s=int(sub)
            sub=""
      return(h,d,mo,y,w,m,s)
    raise commands.BadArgument(message="Please provide a valid duration.")

@client.command()
@commands.check(check_owner)
async def reload(ctx, *, extension):
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f"```Succesfully Reloaded {extension}```")

@client.command()
@commands.check(check_owner)
async def unload(ctx, *, extension):
  client.unload_extension(f'cogs.{extension}')
  await ctx.send(f"```Succesfully Unloaded {extension}```")

@client.command()
@commands.check(check_owner)
async def load(ctx, *, extension):
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f"```Succesfully Loaded {extension}```")

for filename in os.listdir('ModerationBot/cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

def direct(message,channel):
  value = ""
  if channel=="general":
    value = db["s"+str(message.guild.id)+"g"]

  elif channel=="logs":
    value = db["s"+str(message.guild.id)+"l"]

  elif channel=="livelogs":
    value = db["s"+str(message.guild.id)+"ls"]
  
  return int(value)
  

#bot active
@client.event
async def on_ready(): 
  await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Trying to program, but failing :D'))
  update.start()
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
  matches = db.prefix("s"+str(member.guild.id)+"ls")
  if (len(matches)==1):
    current_count_messages= int(db["s"+str(member.guild.id)+"join"])
    db["s"+str(member.guild.id)+"join"] = str(current_count_messages+1)
  channel = client.get_channel(direct(member,"general"))
  await channel.send("Hey. Welcome.")

#leave
#make embed
@client.event
async def on_member_remove(member):
  matches = db.prefix("s"+str(member.guild.id)+"ls")
  if (len(matches)==1):
    current_count_messages= int(db["s"+str(member.guild.id)+"leave"])
    db["s"+str(member.guild.id)+"leave"] = str(current_count_messages+1)
  channel = client.get_channel(direct(member,"general"))
  await channel.send(f"{member} has left the server")

def quickdelete():
  matches = db.prefix("i")
  for key in matches:
    print(key, db[key])
    del db[key]

#quickdelete()

def quickcheckreminders():
    matches = db.prefix("r")
    for key in matches:
      print(db[key])
      del db[key]
    print("total"+db["totalreminders"])
    db["totalreminders"]="0"

#quickcheckreminders()

#background tasks
@tasks.loop(seconds=0.5)
async def update():
  lines2 = db.prefix("i")
  lines3 = db.prefix("r")
  lines=lines2+lines3
  for i in range(len(lines)):
    yy=str(lines[i])
    x=db[lines[i]]
    broken=x.split(",")
    if yy[0]=="r" and broken[0]=="dm":
      when=str(broken[1])
      ppl=int(broken[2])
      notif=str(broken[3])
      date_time_obj = datetime.strptime(when, "%Y-%m-%d %H:%M:%S")
      if date_time_obj <= datetime.now():
        ppl = client.get_user(ppl)
        notif=f"*Hey, its Watchdog. I have a reminder for you.* :dog:\n**Message:** {notif}"
        await ppl.send(notif)
        del db[lines[i]]
    elif yy[0]=="r" and broken[0]!="dm":
      when=str(broken[0])
      where=int(broken[1])
      who=int(broken[2])
      notif=str(broken[3])
      date_time_obj = datetime.strptime(when, "%Y-%m-%d %H:%M:%S")
      if date_time_obj <= datetime.now():
        location = client.get_channel(where)
        notif=f"<@{who}> *Hey, its Watchdog. I have a reminder for you.* :dog:\n**Message:** {notif}"
        await location.send(notif)
        del db[lines[i]]
    elif (len(broken)==9):
      t=str(broken[0])
      ID=int(broken[1])
      h=int(broken[2])
      d=int(broken[3])
      mo=int(broken[4])
      y=int(broken[5])
      w=int(broken[6])
      m=int(broken[7])
      s=int(broken[8])
      check = client.get_channel(ID)
      online_users=sum(member.status!=discord.Status.offline and not member.bot for member in check.members)
      amatch=db.prefix("s"+str(yy[1:19])+"peakusers")
      current_most=0
      if len(amatch)==1:
        current_most=int(db["s"+str(yy[1:19])+"peakusers"])
      if online_users>current_most and len(amatch)==1:
        db["s"+str(yy[1:19])+"peakusers"]=str(online_users)
      date_time_obj = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
      d2 = datetime.now()
      current=datetime.now()
      delta = relativedelta(hours=h, days=d, months=mo, years=y, weeks=w, minutes=m, seconds=s)
      new = current+delta
      tdelta=new-d2
      the_last=display_time(tdelta.total_seconds(), 4)
      if date_time_obj <= datetime.now():
        channel = client.get_channel(ID)
        new=new.strftime("%Y-%m-%d %H:%M:%S")
        matches = db.prefix("s"+str(yy[1:19])+"leave")
        matches2 = db.prefix("s"+str(yy[1:19])+"join")
        matches3 = db.prefix("s"+str(yy[1:19])+"messages")
        matches4 = db.prefix("s"+str(yy[1:19])+"bot")
        matches5= db.prefix("s"+str(yy[1:19])+"peakusers")
        if len(matches)==1 and len(matches2)==1 and len(matches3)==1 and len(matches4)==1 and len(matches5)==1:
          forleave=db["s"+str(yy[1:19])+"leave"]
          forjoin=db["s"+str(yy[1:19])+"join"]
          formessage=db["s"+str(yy[1:19])+"messages"]
          forbotmessage=db["s"+str(yy[1:19])+"bot"]
          forpeakusers=db["s"+str(yy[1:19])+"peakusers"]
          await channel.send(f'`Stats for the Last {the_last}: Total Messages: {formessage}, Most # of people online: {forpeakusers}, # of Members who joined: {forjoin}, # of Members who left: {forleave}, # of Messages from Bots: {forbotmessage}, # of Messages from Users: {str(int(formessage)-int(forbotmessage))}`')
          db["s"+str(yy[1:19])+"leave"]="0"
          db["s"+str(yy[1:19])+"join"]="0"
          db["s"+str(yy[1:19])+"messages"]="0"
          db["s"+str(yy[1:19])+"bot"]="0"
          db["s"+str(yy[1:19])+"peakusers"]="0"
          toadd=str(new)+","+str(ID)+","+str(h)+","+str(d)+","+str(mo)+","+str(y)+","+str(w)+","+str(m)+","+str(s)
          db[lines[i]]=str(toadd)



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
  channel = client.get_channel(direct(message,"logs"))
  await channel.send(embed=embed)




keep_on()
#client.loop.create_task(update())
client.run(my_secret)