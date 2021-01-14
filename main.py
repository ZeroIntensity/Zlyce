import discord
from discord.ext import commands, tasks
import json
import dotenv
from server import keep_alive
import os
import asyncio
mainCol = 0x0
name = 'Zlyce'
startingprefix = f'{name.lower()}/'

intents = discord.Intents.default()
intents.members = True
intents.guilds = True



async def normalembed(ctx, title, msg):
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
  embed.description=str(error)
  embed.set_footer(text=name)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed) 

@client.event
async def on_message(message):
  if (message.content == f'<@!798624290567618580>') or (message.content == f'<@!798624290567618580> '):
    pre = await grab_prefix(ctx = message)
    await message.channel.send(f'Hey {message.author.mention}! I\'m {name}! You can see all my commands using ``{pre}help``!')

  await client.process_commands(message) # yeah

@client.event
async def on_ready():
  await client.wait_until_ready()
  print(f"Logged in as {client.user} ({client.user.id})") # Prints bot tag and ID
  await client.change_presence(activity=discord.Activity(name=f"{len(client.guilds)} Servers! | {startingprefix}help", type=discord.ActivityType.listening))

@client.event
async def on_guild_join(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f) 

  prefixes [int(guild.id)] = startingprefix # Sets the default prefix to 'zlyce/'

  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f)



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
    embed.set_footer(text=name)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if (args.lower() == 'moderation') or (args.lower() == 'mod'):
    embed=discord.Embed(color=mainCol)
    embed.timestamp=(ctx.message.created_at)
    embed.title=f'Moderation Commands'
    embed.description=f'Do ``{pre}help <command>`` for more help on a command\n\n`[] is an optional argument.`\n`<> is not an optional argument`'
    embed.add_field(name="Ban", value=f"Bans a member\n``{pre}ban <@member>``")
    embed.add_field(name="Kick", value=f"Kicks a member\n``{pre}kick <@member>``")
    embed.set_footer(text=name)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  if args.lower() == 'main':
    embed=discord.Embed(color=mainCol)
    embed.timestamp=(ctx.message.created_at)
    embed.title=f'Main Commands'
    embed.description=f'Do ``{pre}help <command>`` for more help on a command\n\n`[] is an optional argument.`\n`<> is not an optional argument`'
    embed.add_field(name="Ping", value=f"Gets bot response time\n``{pre}ping``")
    embed.add_field(name="Prefix", value=f"Changes bot prefix\n``{pre}prefix <new prefix>``")
    embed.set_footer(text=name)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  # Command help starts here
  if (args.lower() == 'member') or (args.lower() == 'user'):
    await commandhelp(ctx, 'member', f'``{pre}member [@member]``','`user`')
  if (args.lower() == 'server') or (args.lower() == 'guild'):
    await commandhelp(ctx, 'server', f'``{pre}server``','`guild`')
  if args.lower() == 'ban':
    await commandhelp(ctx, 'ban', f'``{pre}ban <@member> [reason]``','`None`')
  if args.lower() == 'kick':
    await commandhelp(ctx, 'kick', f'``{pre}kick <@member> [reason]``','`None`')
  if args.lower() == 'ping':
    await commandhelp(ctx, 'ping', f'``{pre}ping``','`api`,`latency`')


@client.command(aliases=['user'])
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
@client.command(aliases=['guild'])
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
  if not ctx.author.guild_permissions.kick_members:
    await error(ctx, 'You do not have permission to run this command.')
  try:
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
  if not ctx.author.guild_permissions.ban_members:
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
  bot_ping = round(client.latency * 1000)
  await normalembed(ctx, 'API Reponse Time',f'{bot_ping}')
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
keep_alive()
client.run(TOKEN)