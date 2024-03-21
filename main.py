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


def create_character_card(name, personality, social_contribution, inteligence, aca, activity, specility, avatar, note):
    overall = int((personality + social_contribution + activity + aca + inteligence) / 5)
    grade = get_grade(overall)  # Call the get_grade function for overall score

    embed = discord.Embed(
        title=f"{name}'s OAA ",
        description="",
        color=discord.Color.blue()
    )
    embed.set_author(name="Stats", icon_url=avatar)

    # Add fields with grades
    fields = [
        ("**Personality:**", personality, get_grade(personality)),
        ("**Academic Ability:**", aca, get_grade(aca)),
        ("**Inteligence:**", inteligence, get_grade(inteligence)),
        ("**Activity:**", activity, get_grade(activity)),
        ("**Social contribution:**", social_contribution, get_grade(social_contribution))
    ]

    for field_name, field_value, field_grade in fields:
        embed.add_field(name=field_name, value=f"{field_value} ({field_grade})", inline=False)

    embed.add_field(name="", value=f"**Speciality: ({specility})\n**", inline=False)
    embed.add_field(name="", value=f"**OVERALL: ({overall})** {grade}", inline=False)  # Add grade to overall field
    embed.set_thumbnail(url=avatar)

    embed.set_footer(text=f"Note: {note}")

    return embed

def get_grade(score):
  """
  This function takes a score as input and returns the corresponding letter grade
  based on the provided grading scale.
  """
  if 0 <= score <= 24:
    grade = "D"
  elif 25 <= score <= 29:
    grade = "D+"
  elif 30 <= score <= 44:
    grade = "C"
  elif 45 <= score <= 49:
    grade = "C+"
  elif 50 <= score <= 64:
    grade = "B"
  elif 65 <= score <= 69:
    grade = "B+"
  elif 70 <= score <= 80:
    grade = "A"
  elif 81 <= score <= 89:
    grade = "A+"
  elif 90 <= score <= 99:
    grade = "S"
  elif score == 100:
    grade = "S+"
  else:
    raise ValueError(f"Invalid score: {score}")

  return grade

@bot.tree.command()
# @app_commands.describe("select player")
async def find(interaction: discord.Interaction, memeber: discord.Member):
        matching_players = pl.find({"_id": memeber.id})
        try:
        
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
        except:
            await interaction.response.send_message("OAA of chosen member doesn't exist")


@bot.tree.command()
# @app_commands.describe("add a member OAA")
@app_commands.checks.has_any_role("Appraisers")
async def add(interaction: discord.Interaction, member: discord.Member, personality: int,
             inteligence: int, academic_ability: int, social_contribution: int,
             speciality: str, activity: int, note: str = None):

    try:
        # Validate integer values (0 <= value <= 100)
        filtered_list = [value for value in [personality, academic_ability, inteligence, social_contribution, activity]
                         if 0 <= value <= 100]

        if len(filtered_list) != 5:
            raise ValueError("Stats must be between 0 and 100.")

        player_data = {
            "_id": int(member.id),
            "p_name": member.name,
            "p_personality": personality,
            "p_intelligence": inteligence,
            "p_activity": activity,
            "p_academic_ability": academic_ability,
            "p_social_contribution": social_contribution,
            "p_speciality": speciality,
            "p_note": note
        }

        # Insert the character data into the 'cards' collection
        pl.insert_one(player_data)
        await interaction.response.send_message(f"{member.name} added to OAA")

    except ValueError as e:
        await interaction.response.send_message(f"Invalid stat values: {e}. Stats must be between 0 and 100.")
    except Exception as e:  # Catch other potential errors
        print(f"Error adding character: {e}")
        await interaction.response.send_message(f"An error occurred while adding {member.name}. Please try again later.")

@bot.tree.command()
# @app_commands.describe("update a member OAA")
@app_commands.checks.has_any_role("Appraisers")
async def update(interaction: discord.Interaction, member: discord.Member, personality: int = 0,
                  inteligence: int = 0, academic_ability: int = 0, social_contribution: int = 0,
                  speciality: str = None, activity: int = 0, note: str = None):

    update_data = {}

    # Filter and validate integer values (0 < value <= 100)
    filtered_integers = [value for value in [personality, academic_ability, inteligence, social_contribution, activity]
                         if 0 < value <= 100]

    # Build update dictionary for integer fields
    
    if 0<personality <=100:
       update_data["p_personality"] = personality
    if 0<inteligence <=100:
       update_data["p_inteligence"] = inteligence
    if 0<social_contribution <=100:
       update_data["p_social_contribution"] = social_contribution
    if 0<academic_ability <=100:
       update_data["p_academic_ability"] = academic_ability
    if 0<activity <=100:
       update_data["p_activity"] = activity
    # Handle optional string fields (speciality and note)
    if speciality is not None:
        update_data["p_speciality"] = speciality
    if note is not None:
        update_data["p_note"] = note

    # Check if there's any data to update
    if not update_data:
        await interaction.response.send_message(f"No valid values provided to update for {member.name}")
        return

    try:
        # Perform the update using MongoDB's update_one method with filters
        result = pl.update_one({"_id": int(member.id)}, {"$set": update_data})

        if result.matched_count == 0:
            await interaction.response.send_message(f"Couldn't find a character for {member.name} to update.")
        else:
            await interaction.response.send_message(f"{member.name}'s character data has been updated.")

    except Exception as e:
        print(f"Error updating character: {e}")
        await interaction.response.send_message(f"An error occurred while updating. Please try again later.")

@bot.tree.command()
# @app_commands.describe("delete a member OAA")
@app_commands.checks.has_any_role("Appraisers")
async def delete(interaction: discord.Interaction, member: discord.Member):
    try:
        # Perform the delete using MongoDB's delete_one method with filters
        result = pl.delete_one({"_id": int(member.id)})

        if result.deleted_count == 0:
            await interaction.response.send_message(f"Couldn't find a character for {member.name} to delete.")
        else:
            await interaction.response.send_message(f"{member.name}'s character data has been deleted.")

    except Exception as e:
        print(f"Error deleting character: {e}")
        await interaction.response.send_message(f"An error occurred while deleting. Please try again later.")

    
     
bot.run(os.environ['TOKEN'])
