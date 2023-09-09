import discord
from discord import app_commands
from discord.ext import commands, tasks
import fastf1
from datetime import datetime, timedelta
from pytz import timezone
import time
from geopy.geocoders import Nominatim
from functools import partial
import pycountry


class Planner(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.message_id = 1115279795043979305

  @commands.Cog.listener()
  async def on_ready(self):
    self.sch.start()
    print("Planner.py is ready!")

  @tasks.loop(minutes=30)
  # @commands.Cog.listener()
  # async def on_raw_reaction_add(self, payload):
  async def sch(self):
    geolocator = Nominatim(user_agent="Planner")
    geocode = partial(geolocator.geocode,
                      language="en",
                      namedetails=True,
                      addressdetails=True)
    # if payload.message_id != self.message_id:
    #   return

    # print(payload.emoji.name)

    # if payload.emoji.name == '🔄':
    if (len(fastf1.get_events_remaining()) == 0):
      upcoming = discord.Embed(title='No more upcoming races...',
                               color=discord.Color.blue())
      current = discord.Embed(
          title='No more races...\n',
          description=f'Stay tuned for season {datetime.today().year + 1}!',
          color=discord.Color.red())
    else:
      remaining = fastf1.get_events_remaining()

      upcoming = discord.Embed(title='Upcoming Races',
                               color=discord.Color.blue())

      coming = fastf1.get_event(datetime.today().year,
                                remaining['RoundNumber'].iloc[0] - 1)

      if (time.mktime(coming['Session5DateUtc'].timetuple()) -
          time.mktime(datetime.today().timetuple())) / 86400 < 0:
        coming = fastf1.get_event(datetime.today().year,
                                  remaining['RoundNumber'].iloc[0])

      # coming = fastf1.get_event(2023, 17)

      if (coming['EventFormat'] == 'conventional'):
        sprint = ''
        session2 = 'FP2:     '
        session3 = 'FP3:     '
        session4 = 'Qualify: '
      else:
        sprint = '`Sprint`'
        session2 = 'Qualify: '
        session3 = 'Shootout:'
        session4 = 'Sprint:  '

      if (time.mktime(coming['Session5DateUtc'].timetuple()) -
          time.mktime(datetime.today().timetuple())) / 86400 > 7:
        country_code = geocode(
            coming['Country']).raw['address']['country_code']
        flag = pycountry.countries.get(alpha_2=country_code).flag
        current = discord.Embed(
            title=
            f'Next Event\n\n{flag} {coming["EventName"]} <t:{str(time.mktime(coming["Session5DateUtc"].timetuple()))[:-2]}:R>',
            color=discord.Color.red())
      if 0 < (time.mktime(coming['Session5DateUtc'].timetuple()) -
              time.mktime(datetime.today().timetuple())) / 86400 <= 7:
        country_code = geocode(
            coming['Country']).raw['address']['country_code']
        flag = pycountry.countries.get(alpha_2=country_code).flag
        current = discord.Embed(
            title=
            f'This Weekend\n\n{flag} {coming["EventName"]} <t:{str(time.mktime(coming["Session5DateUtc"].timetuple()))[:-2]}:R>',
            color=discord.Color.red())

      if time.mktime(coming['Session1DateUtc'].timetuple()) < time.mktime(
          datetime.today().timetuple()):
        fp1 = ''
      else:
        fp1 = f'> `FP1:     ` <t:{str(time.mktime(coming["Session1DateUtc"].timetuple()))[:-2]}:f> <t:{str(time.mktime(coming["Session1DateUtc"].timetuple()))[:-2]}:R>\n'

      if time.mktime(coming['Session2DateUtc'].timetuple()) < time.mktime(
          datetime.today().timetuple()):
        fp2 = ''
      else:
        fp2 = f'> `{session2}` <t:{str(time.mktime(coming["Session2DateUtc"].timetuple()))[:-2]}:f> <t:{str(time.mktime(coming["Session2DateUtc"].timetuple()))[:-2]}:R>\n'

      if time.mktime(coming['Session3DateUtc'].timetuple()) < time.mktime(
          datetime.today().timetuple()):
        fp3 = ''
      else:
        fp3 = f'> `{session3}` <t:{str(time.mktime(coming["Session3DateUtc"].timetuple()))[:-2]}:f> <t:{str(time.mktime(coming["Session3DateUtc"].timetuple()))[:-2]}:R>\n'

      if time.mktime(coming['Session4DateUtc'].timetuple()) < time.mktime(
          datetime.today().timetuple()):
        q = ''
      else:
        q = f'> `{session4}` <t:{str(time.mktime(coming["Session4DateUtc"].timetuple()))[:-2]}:f> <t:{str(time.mktime(coming["Session4DateUtc"].timetuple()))[:-2]}:R>\n'

      current.add_field(
          name=f'Round {coming["RoundNumber"]} {sprint}',
          value=
          f'> `Country: ` {coming["Country"]}\n> `Track:   ` {coming["Location"]}'
          + f'\n{fp1}{fp2}{fp3}{q}' + '> `Race:    ` <t:' +
          str(time.mktime(coming['Session5DateUtc'].timetuple()))[:-2] +
          ':f> <t:' +
          str(time.mktime(coming['Session5DateUtc'].timetuple()))[:-2] + ':R>')

      for i in range(0, len(remaining), 2):
        sprint = ''
        if (remaining['Session2'].iloc[i] == 'Qualifying'):
          sprint = ' `Sprint`'

        # when current
        country_code = geocode(
            remaining['Country'].iloc[i]).raw['address']['country_code']
        flag = pycountry.countries.get(alpha_2=country_code).flag
        upcoming.add_field(
            name=f'Round {remaining["RoundNumber"].iloc[i]}  {sprint}',
            value=
            f'> `Country:` {flag} {remaining["Country"].iloc[i]}\n> `Track:  ` {remaining["Location"].iloc[i]}\n> `Date:   ` <t:'
            + str(time.mktime(
                remaining['Session1DateUtc'].iloc[i].timetuple()))[:-2] +
            ':D>',
            inline=True)
        if len(remaining) % 2 != 0 and i == len(remaining) - 1:
          pass
        else:
          country_code = geocode(
              remaining['Country'].iloc[i + 1]).raw['address']['country_code']
          flag = pycountry.countries.get(alpha_2=country_code).flag
          upcoming.add_field(
              name=f'Round {remaining["RoundNumber"].iloc[i+1]}  {sprint}',
              value=
              f'> `Country:` {flag} {remaining["Country"].iloc[i+1]}\n> `Track:  ` {remaining["Location"].iloc[i+1]}\n> `Date:   ` <t:'
              + str(
                  time.mktime(
                      remaining['Session1DateUtc'].iloc[i +
                                                        1].timetuple()))[:-2] +
              ':D>',
              inline=True)
        upcoming.add_field(name='', value='', inline=False)

      # current.add_field(name='',
      #                   value='click 🔄 to refresh\n> Updated <t:' +
      #                   str(time.mktime(datetime.today().timetuple()))[:-2] +
      #                   ':R>',
      #                   inline=False)
    # current.add_field(name='',
    # value='click 🔄 to refresh\n> Please allow some time to refresh',
    # inline=False)
    current.set_footer(text=f'Powered by fastf1 lib | Dev by m4karoni')

    channel = self.client.get_channel(1114872342703771728)
    message = await channel.fetch_message(self.message_id)

    await message.edit(embeds=[upcoming, current])
    # await message.add_reaction('🔄')
    # await message.remove_reaction('🔄', payload.member)
    await message.clear_reactions()

  # print(guild.get_member(payload.user_id))
  # print(payload.member)

  # @commands.command()
  # async def upcoming(self, ctx):
  #     tz = timezone("Asia/Singapore")
  #     upcoming = discord.Embed(title='Upcoming Races',color=discord.Color.blue())
  #     current = discord.Embed(title='This weekend', color=discord.Color.red())
  #     remaining = fastf1.get_events_remaining()

  #     if ((time.mktime(datetime.fromisoformat(str(remaining['Session5Date'].iloc[0])).astimezone(tz).timetuple())) - time.mktime(datetime.today().timetuple()))/86400 > 7:
  #         coming = fastf1.get_event(datetime.today().year, remaining['RoundNumber'].iloc[0] - 1)
  #         if 0 < (time.mktime(datetime.fromisoformat(str(coming['Session5Date'])).astimezone(tz).timetuple()) - time.mktime(datetime.today().timetuple()))/86400 < 7:
  #             current.add_field(name=f'Round {coming["RoundNumber"]}', value=f'> Country: {coming["Country"]}\n> Track: {coming["Country"]}\n> Date & Time: <t:' + str(time.mktime(datetime.fromisoformat(str(coming['Session5Date'])).astimezone(tz).timetuple()))[:-2] + ':f>\n> <t:' + str(time.mktime(datetime.fromisoformat(str(coming['Session5Date'])).astimezone(tz).timetuple()))[:-2] + ':R>')
  #         else:
  #             current.add_field(name='There are no races this weekend :\'(', value='')

  #     if len(remaining) == 0:
  #         upcoming.add_field(name='More races in ' + str(datetime.today().year + 1) + ' season...', value='')
  #     else:
  #         for i in range(0,len(remaining),2):
  #             upcoming.add_field(name=f'Round {remaining["RoundNumber"].iloc[i]}',value=f'> Country: {remaining["Country"].iloc[i]}\n> Track: {remaining["Location"].iloc[i]}\n> Date & Time: <t:' + str(time.mktime(datetime.fromisoformat(str(remaining['Session5Date'].iloc[i])).astimezone(tz).timetuple()))[:-2] + ':f>', inline=True)
  #             if len(remaining) % 2 != 0 and i == len(remaining) - 1:
  #                 pass
  #             else:
  #                 upcoming.add_field(name=f'Round {remaining["RoundNumber"].iloc[i+1]}',value=f'> Country: {remaining["Country"].iloc[i+1]}\n> Track: {remaining["Location"].iloc[i+1]}\n> Date & Time: <t:' + str(time.mktime(datetime.fromisoformat(str(remaining['Session5Date'].iloc[i+1])).astimezone(tz).timetuple()))[:-2] + ':f>', inline=True)
  #             upcoming.add_field(name='',value='',inline=False)

  #     current.add_field(name='', value='click 🔄 to refresh',inline=False)
  #     current.set_footer(text=f'Powered by fastf1 lib')

  #     sch = await ctx.send(embeds=[upcoming, current])
  #     await sch.add_reaction('🔄')
  #     await ctx.message.delete()


async def setup(client):
  await client.add_cog(Planner(client))
