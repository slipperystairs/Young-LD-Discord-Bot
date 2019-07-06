from setup import dbl
import os
import discord
import YoungLarryDavid
from discord.ext import commands


class DiscordBotsOrgAPI(commands.Cog):
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv('BOT') # set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token, autopost=True)
        # autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))
