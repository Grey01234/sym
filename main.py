import os
import discord
import asyncio
from discord.ext import commands
from pymongo import MongoClient
# from keep_alive import keep_alive
from discord import app_commands
import random
from discord.ext import commands
from discord.ui import Select
from discord.ui import Button
from discord import  SelectOption,ButtonStyle,Embed,interactions
intents = discord.Intents.default()

intents.message_content = True

# Define the prefix and create the bot
bot = commands.Bot(command_prefix="!", intents=intents)

my_secret = os.environ['pass']
# use('mongodbVSCodePlaygroundDB');
uri = f"mongodb+srv://kiyotakas048:{my_secret}@cluster0.ffx6f52.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(uri)

db = mongo_client.get_database('ROTE')
pl = db["player"]

class card_creation:
  # print("hello")

  @staticmethod
  def card_data():
      player_id = int(input("Enter the player id: "))
      player_name = input("What is the name of your player? ")
      player_personality = input("player personality? ")
      player_inteligence = input("player inteligence? ")
      player_activity = input("player activity? ")
      player_effort = input("player effort? ")
      player_social_contribution = input("What is the mental health of your player? ")
      player_speciality = input("player specializes in? ")

      # Create a dictionary with the character data
      player_data = {
          "p_id": player_id,
          "p_name": player_name,
          "p_personality": player_personality,
          "p_inteligence": player_inteligence,
          "p_activity": player_activity,
          "p_effort": player_effort,
          "p_social_contribution": player_social_contribution,
          "p_speciality": player_speciality

      }

      # Insert the character data into the 'cards' collection
      pl.insert_one(player_data)
# card_creation.card_data() 
def grading(number):
    pass

@bot.event
async def on_ready():
    print("Logged in as", bot.user.name)
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except:
        print(" it failed!")


def create_character_card(name, personality, social_contribution, inteligence,aca, activity, specility, avatar,note):
    overall= int((personality + social_contribution + activity +aca+ inteligence)/5)


    embed = discord.Embed(
        title=f"{name}'s OAA ",
        description="",
        color=discord.Color.blue()
    )
    embed.set_author(name="Stats", icon_url=avatar)

    embed.add_field(name="", value=f"**Personality:({personality})**", inline=False)

    embed.add_field(name="", value=f"**Academic Ability: ({aca})\n**", inline=False)
    embed.add_field(name="", value=f"**Inteligence: ({inteligence})**\n", inline=False)
    embed.add_field(name="", value=f"**Activity: ({activity})**\n", inline=False)

    embed.add_field(name="", value=f"**Social contribution: ({social_contribution})**\n", inline=False)
    embed.add_field(name="", value=f"**Speciality: ({specility})\n**", inline=False)
    embed.add_field(name="", value=f"**OVERALL: ({overall})**\n", inline=False)
    embed.set_thumbnail(url=avatar)

    embed.set_footer(text=f"Note: {note}")

    return embed


@bot.tree.command()
# @app_commands.describe("select player")
async def find(interaction: discord.Interaction, memeber: discord.Member):
        matching_players = pl.find({"_id": memeber.id})


        for character_data in matching_players:
            character_name =memeber.name
            personality = character_data["p_personality"]
            mental= character_data["p_inteligence"]
            aca= character_data["p_academic_ability"]
            # effort = character_data["p_effort"]
            coop = character_data.get("p_social_contribution", "Not specified")
            speciality = character_data.get("p_speciality", "Not specified")
            activity = character_data.get("p_activity", "Not specified")
            note = character_data.get("p_note", "Not specified")
            url=memeber.avatar.url

        embed = create_character_card(character_name,personality,coop,mental,aca,activity,speciality,url,note)
        await interaction.response.send_message(embed=embed)

@bot.tree.command()
# @app_commands.describe("add a member OAA")
@app_commands.checks.has_any_role("S") 
async def add(interaction: discord.Interaction, member: discord.Member, personality: int,inteligence: int,academic_ability:int,social_contribution:int,speciality:str,activity:int,note: str=None):
    list = [personality,academic_ability,inteligence,social_contribution,activity]
    filtered_list = [item for item in list if 0 <= item <= 100]

    if len(list) == len(filtered_list):
        player_data = {
            "_id": int(member.id),
            "p_name": member.name,
            "p_personality": personality,
            "p_inteligence": inteligence,
            "p_activity": activity,
            "p_academic_ability": academic_ability,
            "p_social_contribution": social_contribution,
            "p_speciality": speciality,
            "p_note":note

        }

        # Insert the character data into the 'cards' collection
        pl.insert_one(player_data)
        await interaction.response.send_message(f"{member.name} added to OAA")
    else:
        await interaction.response.send_message(f"personality,academic_ability,inteligence,social_contribution,activity can't be negetive nor can they be more than 100")



bot.run(os.environ['TOKEN'])