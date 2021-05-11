import wikipediaapi
import os
import keep_alive
import discord
import replit
from owotext import OwO
uwu = OwO()
from replit import db
import random
wiki = wikipediaapi.Wikipedia('en')
from discord.ext import commands
def isreferpage(page):
  summary = page.summary.split(" ")
  if not summary: return False
  del summary[0]
  summary = " ".join(summary)
  return summary.startswith("may refer to:")
prefixes = db["prefixes"]
def get_prefix(client=None, message=None):
    return prefixes.get(message.guild.id, "wp")
bot = commands.Bot(command_prefix=get_prefix)
@bot.event
async def on_ready():
  print("READY")
@bot.command()
async def owowiki(ctx, *, name):
  return await _wiki(ctx, name=name, owo=True)
@bot.command()
async def prefix(ctx, *, prefix=None):
 """This shows the prefix if provided with no prefix. If provided with a prefix and you have the ban permission, it will change the prefix to the provided one."""
 global prefixes
 if prefix:
  if not ctx.channel.permissions_for(ctx.guild.me).ban_members:
    return await ctx.send("You must be able to ban members to use this command!")
  if prefix == "reset": prefix = "wp"
  if len(prefix)>5:
    return await ctx.send("Whoa thats a bit big.. try something 5 chars or under.")
  elif len(prefix)==0:
    return await ctx.send("*Googles How to explain to a stupid discord user that making a prefix 0 chars long is problematic*")
  if prefix == "wp":
    if prefixes.get(ctx.guild.id):
      del prefixes[ctx.guild.id]
  else:
    prefixes[ctx.guild.id] = prefix
  return await ctx.send(f"Server prefix is now '{prefix}'")
 else:
  return await ctx.send(f"The Server prefix is '{get_prefix(message=ctx.message)}'")
@bot.command()
async def blend(ctx, *, name):
  title = "Finished blending!"
  msg = await ctx.send(random.choice(("Blending!", "The blender is stuck! *Hits with a Lopadotemachoselachogaleokranioleipsanodrimhypotrimmatosilphiokarabomelitokatakechymenokichlepikossyphophattoperisteralektryonoptekephalliokigklopeleiolagoiosiraiobaphetraganopterygon.* There! ***NOW BLEND YOU STUPID MACHINE!!!***", "Where is my blender? *Sees it in the garbage bag* **OH FOR FUCKS SAKE**")))
  follownum = 30
  page = wiki.page(name)
  embed = discord.Embed()
  if not page.exists():
   page = wiki.page(name.replace(" ", "_"))
   if not page.exists():
    embed.color = discord.Colour.from_rgb(128, 191, 255)
    embed.title = f"Page {name} does not exist"
    embed.description = f"I cannot find the page called {name}."
    embed.color = discord.Colour.from_rgb(179, 0, 0)
    return await msg.edit(content="", embed=embed)
  if list(page.links) == []:
    embed.color = discord.Colour.from_rgb(128, 191, 255)
    embed.title = f"Page {name} does not have any links to follow"
    embed.description = f"The way I blend wiki articles is by following links, because there is no links to follow I cannot use this wiki article."
    embed.color = discord.Colour.from_rgb(179, 0, 0)
    return await msg.edit(content="", embed=embed)
  embed.color = discord.Colour.from_rgb(128, 191, 255)
  names = []
  x=""
  for _ in range(follownum):
    vlinks = list(page.links)
    if _+1 == follownum:
      for n in range(len(vlinks)):
        link = vlinks[n]
        if (str(link).lower().startswith("wikipedia:") or str(link).lower().startswith("talk:") or str(link).lower().startswith("template talk:")):
          del vlinks[n]
    if vlinks==[]:
        embed.color = discord.Colour.from_rgb(128, 191, 255)
        title = f"I got stuck in a rut!"
        embed.description = f"I had to cut off the output as I ran into a page with no valid links, you can still find it below though."
        embed.color = discord.Colour.from_rgb(255, 244, 38)
        break
    x = random.choice(vlinks)
    page = wiki.page(x)
    names.append(f'{x}')
  embed.title = title
  embed.add_field(name="Look at how it changed!", value=f"{name} -> {' -> '.join(names)}")
  return await msg.edit(content="", embed=embed)
@bot.command(name="wiki")
async def _wiki(ctx, *, name, owo=False):
  page = wiki.page(name)
  prefix = get_prefix(message=ctx.message)
  embed = discord.Embed()
  if not page.exists():
   page = wiki.page(name.replace(" ", "_"))
   if not page.exists():
    embed.color = discord.Colour.from_rgb(128, 191, 255)
    if owo:
      embed.title = uwu.whatsthis(f"Page {name} does not exist")
    else:
      embed.title = f"Page {name} does not exist"
    if owo:
      embed.description = uwu.whatsthis(f"I cannot find the page called {name}.")
    else:
      embed.description = f"I cannot find the page called {name}."
    embed.color = discord.Colour.from_rgb(179, 0, 0)
    await ctx.send("You got mail.")
    return await ctx.author.send(embed=embed)
  embed.color = discord.Colour.from_rgb(128, 191, 255)
  if isreferpage(page):
    summary = page.summary.split("\n")
    embed.title = summary.pop(0)
    embed.description = "\n".join(summary)
    await ctx.send("You got mail :P")
    return await ctx.author.send(embed=embed)
  else:
    await ctx.send("You got mail!")
    emsgs = []
    embed.set_footer(text="Send next to see the next section and send exit to exit.")
    for section in page.sections:
      if owo:
        embed.title = uwu.whatsthis(section.title)
      else:
        embed.title = section.title
      if owo:
        embed.description = uwu.whatsthis(section.text)
      else:
        embed.description = section.text
      if len(embed) > 2048:
       while True:
        x = embed.description.split(".")
        y = []
        while len(embed) > 2048:
          y.append(x.pop(-1))
          embed.description = ".".join(x)
        await ctx.author.send(embed=embed)
        embed.title = embed.title+" continued"
        embed.description = '.'.join(y)
        if not len(embed) > 2048:
          await ctx.author.send(embed=embed)
          break
      else:
        await ctx.author.send(embed=embed)
      try:
          msg = await bot.wait_for('message', check=lambda msg: msg.author.id == ctx.author.id and type(msg.channel) == discord.DMChannel and (msg.content.lower()=="next" or msg.content.lower()=="exit"), timeout=120)
      except Exception as e:
           print(repr(e))
           return await ctx.author.send("Auto exited")
      if msg.content.lower() == "exit":
        return await ctx.author.send("Exited")
    return await ctx.author.send("There is no next. This session has been exited.")
keep_alive.start()
bot.run(os.environ.get("TOKEN"))