import dbl
import os
import sys
import discord
from discord.ext import commands

class DiscordBotsOrgAPI(commands.Cog):
    """Handles interactions with the discordbots.org API"""

    def __init__(self, client):
        self.client = client
        self.token = 'TOKEN' # set this to your DBL token
        self.dblpy = dbl.Client(self.client, self.token, autopost=True)
        # autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")

def setup(client):
    client.add_cog(DiscordBotsOrgAPI(client))
