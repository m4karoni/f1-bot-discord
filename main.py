import discord
from discord.ext import commands, tasks
import os
import asyncio
from itertools import cycle
from webserver import keep_alive

client = commands.Bot(command_prefix="~", intents=discord.Intents.all())

bot_status = cycle(
    ["Leclrec crying", "Verst-happening diss track", "Hamil-time"])
activity = discord.ActivityType
type = cycle([activity.listening, activity.playing, activity.watching])


@tasks.loop(seconds=5)
async def change_status():
  await client.change_presence(
      activity=discord.Activity(name=next(bot_status), type=next(type)))


@client.event
async def on_ready():
  await client.tree.sync()
  print(f'{client.user} is now running!')
  change_status.start()


async def load():
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      await client.load_extension(f"cogs.{filename[:-3]}")
      # print(f"{filename[:-3]} is loaded") # For debugging


keep_alive()

my_secret = os.environ['SECRET_KEY']


async def main():
  async with client:
    await load()
    await client.start(my_secret)


asyncio.run(main())
