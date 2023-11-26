# bot.py
import os
import sys
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from wizard_event_scrapper import Database, Requests
from scryfall import Requests as ScryfallRequests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()

class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents = intents,
            help_command = None
        )

    def check_zip_code(self, text) -> None:
        """
        This code searches for a zip code and returns it
        """
        m = re.search(r'(?!\A)\b\d{5}(?:-\d{4})?\b', text)
        if m:
            return m.group(0)
        else:
            logging.info("The request doesn't contain a zip code. Please provide on in your next query.")

    def check_location(self, text):
        location = re.search(r'\[.*?\]', text).group(0)
        return location[1:][:len(location)-2].lower()


    async def on_ready(self):
        for guild in self.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{self.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(self, message):

        print(message.content)

        if message.author == self.user:
            return


        if '!location_bot' in message.content:
            zip_code = self.check_zip_code(message.content)
            response = f"I've found the following location events for {zip_code}"
            logging.info(response)
            locations = Requests.EventRequests().getLocations(zip_code)
            for location in locations:
                # print(f"{event}")
                await message.channel.send(
                    f"""
                    {location['name']}
                    """
                )

        if '!event_bot' in message.content:
            # location = re.findall(r'\[.*?\]', message.content)
            loc_name = self.check_location(message.content)
            logging.info(f"Getting events for {loc_name}")
            loc_id = Requests.EventRequests().getLocationId(loc_name, 80126)
            loc_events = Requests.EventRequests().getLocationEvents(loc_id, 80126)
            if len(loc_events) > 0:
                for event in loc_events:
                    await message.channel.send(
                        f"{event[0]}\n"
                        f"{event[1]}\n"
                        f"{event[2]}\n"
                        "----------------------------------"
                        )
            else:
                await message.channel.send(f"No events found at {loc_name}")

        # if message.content.startswith('[['):
        #     card_name = message.content.split("[[")[1].split("]]")[0]
        #     print(card_name)
        #     card_object = ScryfallRequests.CardRequests().getCard(card_name)
        #     try:
        #         await message.channel.send(
        #             card_object['image_uris']['normal']
        #         )
        #         await message.channel.send(
        #             [f"{card_object['name']} TCGPlayer Link"](card_object['purchase_uris']['tcgplayer'])
        #         )
        #     except:
        #         await message.channel.send(
        #             card_object['details']
        #         )

        if message.content.startswith('[['):
            # card_name = message.content.split("[[")[1].split("]]")[0]
            # print(card_name)
            # card_object = ScryfallRequests.CardRequests().getCard(card_name)
            # try:
            #     await message.channel.send(
            #         card_object['image_uris']['normal']
            #     )
            #     await message.channel.send(
            #         [f"{card_object['name']} TCGPlayer Link"](card_object['purchase_uris']['tcgplayer'])
            #     )
            # except:
            #     await message.channel.send(
            #         card_object['details']
            #     )
            card_name = message.content.split("[[")[1].split("]]")[0]
            card_class = ScryfallRequests.CardRequests()
            card_object = card_class.getCard(card_name)

            if card_class.card_face_bool == True:

                name = card_class.getCardAttr('name')[0]
                name_1 = card_class.getCardAttr('name')[1]
                uri = card_class.getCardAttr('uri')
                logging.info(uri)
                try:
                    mana_cost_0 = card_class.getCardAttr('mana_cost')[0]
                    mana_cost_1 = card_class.getCardAttr('mana_cost')[1]
                except:
                    mana_cost_0 = ""
                    mana_cost_1 = ""

                try:
                    type_line_0 = card_class.getCardAttr('type_line')[0]
                    type_line_1 = card_class.getCardAttr('type_line')[1]
                except:
                    type_line_0 = ""
                    type_line_1 = ""

                try:
                    oracle_text_0 = card_class.getCardAttr('oracle_text')[0]
                    oracle_text_1 = card_class.getCardAttr('oracle_text')[1]
                except:
                    oracle_text_0 = ""
                    oracle_text_1 = ""

                try:
                    power_0 = card_class.getCardAttr('power')[0]
                    tough_0 = card_class.getCardAttr('toughness')[0]
                    p_t_0 = f"{power_0}/{tough_0}"
                except:
                    power_0 = ""
                    tough_0 = ""
                    p_t_0 = ""

                try:
                    power_1 = card_class.getCardAttr('power')[1]
                    tough_1 = card_class.getCardAttr('toughness')[1]
                    p_t_1 = f"{power_1}/{tough_1}"
                except:
                    power_1 = ""
                    tough_1 = ""
                    p_t_1 = ""

                    embed = discord.Embed(
                        title = name,
                        url =  uri,
                        description = 
                            f"{mana_cost_0}\n"
                            f"{type_line_0}\n"
                            f"{oracle_text_0}\n"
                            f"{p_t_0}\n"
                            "---------------------\n"
                            f"{name_1}\n"
                            f"{mana_cost_1}\n"
                            f"{type_line_1}\n"
                            f"{oracle_text_1}\n"
                            f"{p_t_1}"
                            
                        )
                    embed.set_thumbnail(url = card_class.getCardAttr('image_uris')[0]['normal'])
                    await message.channel.send(embed=embed)
    
            else:
                name = card_class.getCardAttr('name')
                uri = card_class.getCardAttr('uri')
                mana_cost = card_class.getCardAttr('mana_cost')
                type_line = card_class.getCardAttr('type_line')
                oracle_text = card_class.getCardAttr('oracle_text')
                power = card_class.getCardAttr('power')
                tough = card_class.getCardAttr('toughness')

                embed = discord.Embed(
                        title = name,
                        url =  uri,
                        description = 
                            f"{mana_cost}\n"
                            f"{type_line}\n"
                            f"{oracle_text}\n"
                            f"{power}/{tough}"
                            
                        )
                embed.set_thumbnail(url = card_class.getCardAttr('image_uris')['large'])
                await message.channel.send(embed=embed)

bot = DiscordBot()
bot.run(TOKEN)



# client = discord.Client(intents = discord.Intents.all())

# @client.event
# async def on_ready():
#     for guild in client.guilds:
#         if guild.name == GUILD:
#             break

#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})'
#     )

# @client.event
# async def on_message(message):

#     print(message.content)

#     if message.author == client.user:
#         return

#     def check_zip_code(text):
#         m = re.search(r'(?!\A)\b\d{5}(?:-\d{4})?\b', text)
#         if m:
#             return m.group(0)
#         else:
#             logging.info("The request doesn't contain a zip code. Please provide on in your next query.")

#     def check_location(text):
#         location = re.search(r'\[.*?\]', text).group(0)
#         return location[1:][:len(location)-2].lower()

#     if '!location_bot' in message.content:
#         zip_code = check_zip_code(message.content)
#         response = f"I've found the following location events for {zip_code}"
#         logging.info(response)
#         locations = Requests.EventRequests().getLocations(zip_code)
#         for location in locations:
#             # print(f"{event}")
#             await message.channel.send(
#                 f"""
#                 {location['name']}
#                 """
#             )

#     if '!event_bot' in message.content:
#         # location = re.findall(r'\[.*?\]', message.content)
#         loc_name = check_location(message.content)
#         logging.info(f"Getting events for {loc_name}")
#         loc_id = Requests.EventRequests().getLocationId(loc_name, 80126)
#         loc_events = Requests.EventRequests().getLocationEvents(loc_id, 80126)
#         if len(loc_events) > 0:
#             for event in loc_events:
#                 await message.channel.send(
#                     f"{event[0]}\n"
#                     f"{event[1]}\n"
#                     f"{event[2]}\n"
#                     "----------------------------------"
#                     )
#         else:
#             await message.channel.send(f"No events found at {loc_name}")


# client.run(TOKEN)