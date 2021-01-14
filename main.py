import discord
from discord.ext import commands, tasks
import json
import dotenv
from server import keep_alive
import os
import asyncio
import string
import random as rand
mainCol = 0x672bff
name = 'Zlyce'
startingprefix = f'{name.lower()}/'

intents = discord.Intents.default()
intents.members = True
intents.guilds = True



async def normalembed(ctx, title, msg): # Normal premade embed
  embed=discord.Embed(color=mainCol)
  embed.timestamp=(ctx.message.created_at)
  embed.title=title
  embed.description=msg
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

async def commandhelp(ctx, command, usage, aliases): # Premade embed for command help
  embed=discord.Embed(color=mainCol)
  embed.timestamp=(ctx.message.created_at)
  embed.title=f'Help'
  embed.description=f'Help for command: **{command}**'
  embed.add_field(name="Aliases", value=aliases)
  embed.add_field(name="Usage", value=usage)
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)
  return

async def error(ctx, msg): # Premade embed for invalid arguments
  embed=discord.Embed(color=0xff0000)
  embed.timestamp=(ctx.message.created_at)
  embed.title='Error'
  embed.description=msg
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)
  return
async def get_prefix(client, message): # This one is for the command_prefix
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

async def grab_prefix(ctx): # This one is used just to grab the guilds prefix in commands
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    return prefixes[str(ctx.guild.id)]

client = commands.Bot(command_prefix = get_prefix, intents=intents) # Calls get_prefix every time

client.remove_command("help") # Remove premade help command



@client.event
async def on_command_error(ctx, error):
  embed=discord.Embed(color=0xff0000) # Using the normal embed instead of the error function because i dont want to change its name lmao
  embed.timestamp=(ctx.message.created_at)
  embed.title='Error'
  embed.description=f'{error}'
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed) 

@client.event
async def on_message(message):
  if (message.content == f'<@!798624290567618580>') or (message.content == f'<@!798624290567618580> '): # With the space and without because yeah
    pre = await grab_prefix(ctx = message)
    await message.channel.send(f'Hey {message.author.mention}! I\'m {name}! You can see all my commands using ``{pre}help``!') 

  await client.process_commands(message) # yeah

@client.event
async def on_ready():
  await client.wait_until_ready()
  print(f"Logged in as {client.user} ({client.user.id})") # Prints bot tag and ID
  await client.change_presence(activity=discord.Activity(name=f"{len(client.guilds)} Servers! | {startingprefix}help", type=discord.ActivityType.listening))
  autostatus.start()

@client.event
async def on_guild_join(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  prefixes [int(guild.id)] = startingprefix # Sets the default prefix to 'zlyce/'

  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f)

@tasks.loop(seconds=10)
async def autostatus():
  await asyncio.sleep(10) # Waits 10 seconds to switch statuses
  await client.change_presence(activity=discord.Activity(name=f'{len(client.users)} Users! | {startingprefix}prefix <your new prefix>', type=discord.ActivityType.listening))

  await asyncio.sleep(10) # Also waits 10 seconds
  await client.change_presence(activity=discord.Activity(name=f'{len(client.guilds)} Servers! | {startingprefix}help', type=discord.ActivityType.listening))



@client.command(aliases=['prefix'])
async def setprefix(ctx, *, args=None):
  if not args:
    await error(ctx, 'You need to specify a prefix.')
    return
  pre = await grab_prefix(ctx)
  if pre == args: # Checks if its the same as the current prefix
    await error(ctx, 'That is already set as your prefix')
    return
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

    prefixes [str(ctx.guild.id)] = args # Sets the new prefix
  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f)
  embed=discord.Embed(color=0x40ffa0)
  embed.timestamp=(ctx.message.created_at)
  embed.title=f'Set Prefix'
  embed.description=f'Set the prefix to `{args}`'
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command(aliases=['h'])
async def help(ctx, args=None):
  pre = await grab_prefix(ctx)
  if not args: # Send this if no category is specified
    embed=discord.Embed(color=mainCol)
    embed.timestamp=(ctx.message.created_at)
    embed.title=f'Select a category'
    embed.add_field(name="Main Commands", value=f"``{pre}help main``")
    embed.add_field(name="Tools Commands", value=f"``{pre}help tools``")
    embed.add_field(name="Moderation Commands", value=f"``{pre}help moderation``")
    embed.set_footer(text=name)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    return
  # Categories start here

  if args.lower() == 'tools': # Would use premade embeds for this, but I don't have a way to add extra fields
    embed=discord.Embed(color=mainCol)
    embed.timestamp=(ctx.message.created_at)
    embed.title=f'Tools Commands'
    embed.description=f'Do ``{pre}help <command>`` for more help on a command\n\n`[] is an optional argument.`\n`<> is not an optional argument`'
    embed.add_field(name="Member", value=f"Gives member info\n``{pre}member [@member]``")
    embed.add_field(name="Server", value=f"Gives server info\n``{pre}server``")
    embed.add_field(name="Random", value=f"Gives random text or a random number\n``{pre}random <text/number>``")
    embed.set_footer(text=name)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if (args.lower() == 'moderation') or (args.lower() == 'mod'): # Checks if the selection is mod or moderator
    embed=discord.Embed(color=mainCol)
    embed.timestamp=(ctx.message.created_at)
    embed.title=f'Moderation Commands'
    embed.description=f'Do ``{pre}help <command>`` for more help on a command\n\n`[] is an optional argument.`\n`<> is not an optional argument`'
    embed.add_field(name="Ban", value=f"Bans a member\n``{pre}ban <@member>``")
    embed.add_field(name="Kick", value=f"Kicks a member\n``{pre}kick <@member>``")
    embed.set_footer(text=name)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if args.lower() == 'main': # Checks if the selection is main
    embed=discord.Embed(color=mainCol)
    embed.timestamp=(ctx.message.created_at)
    embed.title=f'Main Commands'
    embed.description=f'Do ``{pre}help <command>`` for more help on a command\n\n`[] is an optional argument.`\n`<> is not an optional argument`'
    embed.add_field(name="Ping", value=f"Gets bot response time\n``{pre}ping``")
    embed.add_field(name="Prefix", value=f"Changes bot prefix\n``{pre}prefix <new prefix>``")
    embed.add_field(name="Info", value=f"Gives bot info\n``{pre}info``")
    embed.set_footer(text=name)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  # Command help starts here
  if (args.lower() == 'member') or (args.lower() == 'user'):
    await commandhelp(ctx, 'member', f'``{pre}member [@member]``','`user`') # This function is used just so i dont have to copy paste an embed every time
  if (args.lower() == 'server') or (args.lower() == 'guild'):
    await commandhelp(ctx, 'server', f'``{pre}server``','`guild`')
  if args.lower() == 'ban':
    await commandhelp(ctx, 'ban', f'``{pre}ban <@member> [reason]``','`None`')
  if args.lower() == 'kick':
    await commandhelp(ctx, 'kick', f'``{pre}kick <@member> [reason]``','`None`')
  if (args.lower() == 'ping') or (args.lower() == 'api') or (args.lower() == 'latency'):
    await commandhelp(ctx, 'ping', f'``{pre}ping``','`api`,`latency`')
  if (args.lower() == 'information') or (args.lower() == 'info') or (args.lower() == 'stats'):
    await commandhelp(ctx, 'info', f'``{pre}info``','`information`,`stats`')
  if args.lower() == 'random':
    await commandhelp(ctx, 'random', f'``{pre}random <text/number>``','`None`')
  if args.lower() == 'warn':
    await commandhelp(ctx, 'warn', f'``{pre}warn <@member> [reason]``','`infraction`')


@client.command(aliases=['user']) # Command that gets user info
async def member(ctx, member: discord.Member=None):
  if not member: 
    user = ctx.author
  else:
    user = member
  embed=discord.Embed(color=mainCol)
  embed.timestamp=(ctx.message.created_at)
  embed.title=f'Member Info'
  embed.description=f'Info for {user.mention}\n\n**ID:** {user.id}\n**Creation Date:** {user.created_at}\n**Avatar URL:** [Click Here]({user.avatar_url})'
  embed.set_thumbnail(url=user.avatar_url)
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command(aliases=['guild']) # Command that gets guild/server info
async def server(ctx):
  embed=discord.Embed(color=mainCol)
  embed.timestamp=(ctx.message.created_at)
  embed.title=f'Server Info'
  embed.description=f'Info for `{ctx.guild}`\n\n**ID:** {ctx.guild.id}\n**Owner:** {ctx.guild.owner.mention}\n**Creation Date:** {ctx.guild.created_at}\n**Icon URL:** [Click Here]({ctx.guild.icon_url})\n**Member Count:** {len(ctx.guild.members)}\n**Role Count:** {len(ctx.guild.roles)}'
  embed.set_thumbnail(url=ctx.guild.icon_url)
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def kick(ctx, member: discord.Member=None, *, args='No reason specified'):
  if not member:
    await error(ctx, 'Please specify a member to kick.')
  if not ctx.author.guild_permissions.kick_members: # Check to see if the author has kick_members permission
    await error(ctx, 'You do not have permission to run this command.')
  try: # Probably a better way to do this but im lazy
    await member.kick(reason=args) 
  except:
    await error(ctx, f'I don\'t have the permissions to kick `{member}`.')
    return
  await normalembed(ctx, 'Kick', f'Successfully kicked `{member}` for `{args}`')
  embed=discord.Embed(color=mainCol)
  embed.timestamp=(ctx.message.created_at)
  embed.title='Kicked'
  embed.description=f'You were kicked in `{ctx.guild}` by {ctx.author.mention}\nReason: `{args}`'
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  try:
    await member.send(embed=embed)
  except:
    pass


@client.command()
async def ban(ctx, member: discord.Member=None, *, args='No reason specified'): 
  if not member:
    await error(ctx, 'Please specify a member to ban.')
  if not ctx.author.guild_permissions.ban_members: # Check to see if the author has ban_members permission
    await error(ctx, 'You do not have permission to run this command.')
  try:
    await member.ban(reason=args)
  except:
    await error(ctx, f'I don\'t have the permissions to ban `{member}`.')
    return
  await normalembed(ctx, 'Ban', f'Successfully banned `{member}` for `{args}`')
  embed=discord.Embed(color=mainCol)
  embed.timestamp=(ctx.message.created_at)
  embed.title='Banned'
  embed.description=f'You were banned in `{ctx.guild}` by {ctx.author.mention}\nReason: `{args}`'
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  try:
    await member.send(embed=embed)
  except:
    pass

@client.command(aliases=['latency','api']) 
async def ping(ctx):
  bot_ping = round(client.latency * 1000) # Gets the latency
  await normalembed(ctx, 'API Reponse Time',f'{bot_ping}')

@client.command(aliases=['information','stats'])
async def info(ctx): # No ones gonna use this but who cares
  await normalembed(ctx, 'Bot Info',f'**Hosted On:** [repl.it](https://repl.it)\n**GitHub Repo:** [Click Here](https://github.com/ZeroIntensity/Zlyce)\n**Servers:** {len(client.guilds)}\n**Users:** {len(client.users)}')



@client.event
async def on_message_delete(message):
  with open("snipes.json", "r") as f:
    snipes = json.load(f)
    avurl = str(message.author.avatar_url).replace('//','slashslash') # Converts the // to slashslash so json doesnt comment it out
    x = { # Dictionary that will be used in the snipe command
  "content": str(message.content), # Gets the message content
  "author": str(message.author), # Gets the author
  "avatar_url": str(avurl), # Gets the avatar url with the // replaced
    } 
    snipes[str(message.guild.id)] = x
  with open("snipes.json", "w") as f:
    json.dump(snipes, f) 

@client.command()  
async def snipe(ctx):
  try:
    with open("snipes.json", "r") as f:
      snipes = json.load(f)
      message = snipes[str(ctx.guild.id)]
  except:
    await error(ctx, 'I found nothing to snipe.')
    return
  avurl = str(message.get("avatar_url")).replace('slashslash', '//') # Convert back the slashslash into a //
  embed=discord.Embed(color=mainCol)
  embed.description=message.get("content")
  embed.set_footer(text=f'Attatchments will not appear.')
  embed.set_author(name=message.get("author"), icon_url=avurl)
  await ctx.send(embed=embed)

@client.command()
async def random(ctx, args=None): 
  if args == None:
    await error(ctx, 'Please specify text or number.')
    return

  if args.lower() == 'text':
    letters = string.ascii_letters
    randomstring = ''.join(rand.choice(letters) for i in range(10)) # Creates a random 10 letter string
    await normalembed(ctx, 'Random Text', randomstring)
    return
  if args.lower() == 'number':
    await normalembed(ctx, 'Random Number', str(rand.randint(0, 1000000))) # Creates a random int (converted to string) that goes to 1000000
    return
  else:
    await error(ctx, 'That is not a valid option.')
  
@client.command(aliases=['infraction'])
async def warn(ctx, member: discord.Member = None, args='No reason specified'):
  if not member:
    await error(ctx, 'Please specify a member.')
    return
  
  with open("warns.json", "r") as f:
    warns = json.load(f)
    try:
      warn = warns[str(ctx.guild.id) + '-' + str(ctx.author.id)]
      oldwarnnum = warn.get("warnnum")
      warnnum = int(oldwarnnum) + 1
    except:
      warnnum = 1
    x = {
  "author": str(ctx.author),
  "reason": str(args),
  "warnnum": str(warnnum)
    } 
    warns[str(ctx.guild.id) + '-' + str(ctx.author.id)] = x
  with open("warns.json", "w") as f:
    json.dump(warns, f) 
  
  embed=discord.Embed(color=mainCol)
  embed.timestamp=(ctx.message.created_at)
  embed.title='Warn'
  embed.description=f'You were warned in `{ctx.guild}` by {ctx.author.mention}\nReason: `{args}`'
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  try:
    await member.send(embed=embed)
  except:
    pass
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
keep_alive()
client.run(TOKEN)