import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Help.py is ready!")

    @commands.command()
    async def f1help(self, ctx):
        f1help = discord.Embed(title="F1™ Bot Guide", description="A basic guide for F1™ Bot", color=discord.Color.red())
        # f1help.add_field(name="Bot Prefix", value="`#`",inline=False)
        f1help.add_field(name="Open bot menu", value="`/f1bot_menu`")
        f1help.add_field(name="", value="_That's it for now_", inline=False)
        f1help.set_footer(text="Brought to you by F1™ Bot")
        
        await ctx.send(embed=f1help) # (<a>=<b>) while <a> is always embed (to call embed function maybe),
                                 # and <b> should be what you declared in the line <b> = discord.Embed(...)

async def setup(client):
    await client.add_cog(Help(client))