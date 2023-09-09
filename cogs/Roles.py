import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.message_id = 1115506957521010749

    @commands.Cog.listener()
    async def on_ready(self):
        print("Roles.py is ready!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.message_id:
            return

        guild = self.client.get_guild(payload.guild_id)

        if payload.emoji.name == 'mercedes':
            role = discord.utils.get(guild.roles, name='W14')
            # role = discord.utils.get(guild.roles, id=1114523038743023626)
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'redbull':
            role = discord.utils.get(guild.roles, name='RB19')
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'ferrari':
            role = discord.utils.get(guild.roles, name='SF-23')
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'mclaren':
            role = discord.utils.get(guild.roles, name='MCL60')
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'alpine':
            role = discord.utils.get(guild.roles, name='A523')
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'alphatauri':
            role = discord.utils.get(guild.roles, name='AT04')
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'astonmartin':
            role = discord.utils.get(guild.roles, name='AMR23')
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'williams':
            role = discord.utils.get(guild.roles, name='FW45')
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'alfaromeo':
            role = discord.utils.get(guild.roles, name='C43')
            await payload.member.add_roles(role)
        elif payload.emoji.name == 'haas':
            role = discord.utils.get(guild.roles, name='VF-23')
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self.message_id:
            return

        guild = self.client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if payload.emoji.name == 'mercedes':
            role = discord.utils.get(guild.roles, name='W14')
            await member.remove_roles(role) 
        elif payload.emoji.name == 'redbull':
            role = discord.utils.get(guild.roles, name='RB19')
            await member.remove_roles(role)
        elif payload.emoji.name == 'ferrari':
            role = discord.utils.get(guild.roles, name='SF-23')
            await member.remove_roles(role)
        elif payload.emoji.name == 'mclaren':
            role = discord.utils.get(guild.roles, name='MCL60')
            await member.remove_roles(role)
        elif payload.emoji.name == 'alpine':
            role = discord.utils.get(guild.roles, name='A523')
            await member.remove_roles(role)
        elif payload.emoji.name == 'alphatauri':
            role = discord.utils.get(guild.roles, name='AT04')
            await member.remove_roles(role)
        elif payload.emoji.name == 'astonmartin':
            role = discord.utils.get(guild.roles, name='AMR23')
            await member.remove_roles(role)
        elif payload.emoji.name == 'williams':
            role = discord.utils.get(guild.roles, name='FW45')
            await member.remove_roles(role)
        elif payload.emoji.name == 'alfaromeo':
            role = discord.utils.get(guild.roles, name='C43')
            await member.remove_roles(role)
        elif payload.emoji.name == 'haas':
            role = discord.utils.get(guild.roles, name='VF-23')
            await member.remove_roles(role)

    # @commands.command()
    # async def roles(self,ctx):
    #     role = discord.Embed(title='Choose your roles', description='Choose a role below with reacting to emojis', color=discord.Color.gold())
    #     role.add_field(name="", value="<:W14:1115313857871753337>**W14**", inline=False)
    #     role.add_field(name="", value="<:RB19:1115313845242699796>**RB19**", inline=False)
    #     role.add_field(name="", value="<:SF23:1115313848556191825>**SF23**", inline=False)
    #     role.add_field(name="", value="<:MCL60:1115313842029871154>**MCL60**", inline=False)
    #     role.add_field(name="", value="<:A523:1115313827685335150>**A523**", inline=False)
    #     role.add_field(name="", value="<:AT04:1115313832873705502>**AT04**", inline=False)
    #     role.add_field(name="", value="<:AMR23:1115313829539233863>**AMR23**", inline=False)
    #     role.add_field(name="", value="<:FW45:1115313839936905268>**FW45**", inline=False)
    #     role.add_field(name="", value="<:C43:1115313835809718295>**C43**", inline=False)
    #     role.add_field(name="", value="<:VF23:1115313850896625694>**VF23**", inline=False)
        
    #     msg = await ctx.send(embed=role)
    #     await ctx.message.delete()

    #     await msg.add_reaction('<:mercedes:1115318991041335366>')
    #     await msg.add_reaction('<:redbull:1115321043620474960>')
    #     await msg.add_reaction('<:ferrari:1115322414407098509>')
    #     await msg.add_reaction('<:mclaren:1115327507282006016>')
    #     await msg.add_reaction('<:alpine:1115330257336147978>')
    #     await msg.add_reaction('<:alphatauri:1115332792620957736>')
    #     await msg.add_reaction('<:astonmartin:1115483805340414052>')
    #     await msg.add_reaction('<:williams:1115484489968275476>')
    #     await msg.add_reaction('<:alfaromeo:1115488922215141386>')
    #     await msg.add_reaction('<:haas:1115504821898850304>')

async def setup(client):
    await client.add_cog(Roles(client))