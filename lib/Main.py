import discord
from discord.ext import commands
import asyncio
import os
from EventListener import handle_events
from PluginLoader import PluginLoader
from CommandHandler import register as register_commands

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "plugins"))
CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "bin", "plugins.json"))
ENV_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", ".env"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="DealerBot Active"))

async def start_bot():
    loader = PluginLoader(PLUGIN_DIR, CONFIG_PATH)
    plugins = loader.load_plugins()
    register_commands(bot, plugins)

    with open(ENV_PATH) as f:
        for line in f:
            if "DISCORD_TOKEN" in line:
                token = line.strip().split("=")[1]
                break
        else:
            raise ValueError("DISCORD_TOKEN not found in .env")

    await bot.start(token)

async def main():
    event_task = asyncio.create_task(handle_events(bot))
    await start_bot()
    await event_task

if __name__ == "__main__":
    asyncio.run(main())
