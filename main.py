import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import random
from datetime import datetime
import asyncio
import json
from pathlib import Path
from functools import partial
import discord
from discord.ext import commands
import random
import asyncio
from pytz import timezone 
import json
from pathlib import Path
from pymongo import MongoClient
import os
import time
from cmdhelp import HelpCommand
from firefly import Firefly
import gif_actions
from dotenv import load_dotenv

# Load environment variables from .env file (for bot token)
load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
if not BOT_TOKEN:
    raise ValueError("No TOKEN found in the environment variables or .env file.")

mongo_uri = os.getenv("MONGO_URI")
_mcst = time.time()
client = MongoClient(mongo_uri)
_mcet = time.time()
print("Connected to Mongo atlas in %.2fs."%(_mcet - _mcst))


# Initialize the bot
_bist = time.time()
bot = commands.Bot(command_prefix=["F ", "f "], intents=discord.Intents.all(), case_insensitive=True)
bot.remove_command('help')

# Function to update or create entry in the collection
def update_count(collection_name: str, username: str, count: int = 1):
    """
    Updates or creates an entry in the given MongoDB collection for the specified username.

    :param collection_name: The name of the MongoDB collection.
    :param username: The username whose count to increment.
    :param count: The number to increment (default is 1).
    """
    db = client["CommandCounts"]
    collection = db[collection_name]

    # `update_one` with upsert to update or create the entry
    result = collection.update_one(
        {"username": username},
        {"$inc": {"count": count}},
        upsert=True
    )

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    await bot.add_cog(Firefly(bot, client))
    await bot.add_cog(HelpCommand(bot))
    # Start the birthday checker when the bot runs
    check_birthdays.start()
    _biet = time.time()
    print("Bot set up in %.2fs."%(_biet - _bist))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith('yui f '):
        # Strip the prefix and pass the rest of the message as a command
        message.content = message.content.lower().replace('yui f ', 'f F ')
        await bot.process_commands(message)
    else:
        await bot.process_commands(message)

# F Command
@bot.command(name="F")
async def pay_respects(ctx, username: str):
    respects = {}
    respects[username] = []
    
    button = discord.ui.Button(emoji="🇫")

    async def on_click(interaction):
        if not interaction.user.id in respects[username]:
            respects[username].append(interaction.user.id)
            await interaction.response.send_message(f"{interaction.user.name} has paid their respects.")
        else:
            await interaction.response.defer()

    button.callback = on_click
    view = discord.ui.View(timeout=40)
    view.add_item(button)

    respectmsg = await ctx.send(f"Press F to pay respect to {username}", view=view)

    # Wait for 40 seconds and display results
    await asyncio.sleep(40)
    button.disabled = True
    await respectmsg.edit(view=view)
    if len(respects[username])==1:
        await ctx.send(f"{len(respects[username])} person paid their respect to {username}.")    
    elif len(respects[username])==0:
        await ctx.send(f"No one paid their respects to {username} :(")
    else:
        await ctx.send(f"{len(respects[username])} people paid their respects to {username}.")

# Yes/No Command
@bot.command(name="yn")
async def yes_no(ctx, *, question: str):
    response = random.choice([["🇾", "🇪", "🇸"], ["🇳", "🇴"]])  # Random Yes or No
    await ctx.message.delete()  # Delete the user's message

    # Send a message with the question and user's mention
    message = await ctx.send(f":crystal_ball: {ctx.author.mention} asked: *{question}*")

    # React with separate letters for the chosen response
    for letter in response:
        await message.add_reaction(letter)


# Pop Command
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name="pop")
async def pop(ctx):
    hidden_index = random.randint(0, 8)  # Randomly choose a button to hide the ring
    tries = 3  # Number of tries allowed
    emos = ["😎", "🤯", "🧨", "🥵", "👽", "🎗", "🧶", "👔"]  # Emojis to use for wrong attempts
    buttons = []
    row = 0
    # Create buttons and assign custom_id
    for i in range(9):
        if i in [0, 1, 2]:
            row = 0
        if i in [3, 4, 5]:
            row = 1
        if i in [6, 7, 8]:
            row = 2
        button = discord.ui.Button(emoji="⬛", row=row)  # Initially set to a black square
        if i == hidden_index:
            button.custom_id = "ring"  # This button has the ring
        else:
            button.custom_id = f"empty_{i}"  # These are empty buttons

        # The on_click function for handling reactions to button presses
        async def on_click(interaction, b=button):
            nonlocal tries
            if b.custom_id == "ring":
                try:
                    update_count('pop_wins', str(interaction.user.id))
                except:
                    print(traceback.format_exc())
                await interaction.response.send_message(f"🎉 You found the 💍!", ephemeral=True)
                for btn in buttons:
                    btn.disabled = True  # Disable all buttons once the ring is found
                await interaction.message.edit(content=f"🎉 {interaction.user.name} found the 💍!", view=view)
            else:
                tries -= 1
                b.emoji = random.choice(emos)  # Change emoji to show the wrong guess
                if tries == 0:
                    for btn in buttons:
                        btn.disabled = True  # Disable all buttons if no tries left
                    await interaction.message.edit(content="Game Over!", view=None)
                else:
                    await interaction.response.send_message(f"❌ Try again! {tries} tries left.", ephemeral=True)
                    await interaction.message.edit(view=view)  # Update the message with the new button state

        button.callback = on_click
        buttons.append(button)

    # Create the view and add the buttons in 3x3 grid layout
    view = discord.ui.View()
    for i in buttons:  # Add rows of 3 buttons each
        view.add_item(i)
    await ctx.send("Find the 💍!", view=view)

# Cooldown error handling
@pop.error
async def pop_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = round(error.retry_after, 2)
        em = discord.Embed(
            title="Cooldown Active",
            description=f"You're on cooldown! Try again in **{remaining_time} seconds**.",
            color=discord.Color.red()
        )
        await ctx.reply(embed=em)

# RPS Command
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name="rps")
async def rps(ctx):
    # Choices for RPS
    choices = ["🪨", "📄", "✂️"]
    bot_choice = random.choice(choices)  # Bot randomly selects one choice

    # Define the buttons for each choice
    rock_button = discord.ui.Button(emoji="🪨", custom_id="rock")
    paper_button = discord.ui.Button(emoji="📄", custom_id="paper")
    scissors_button = discord.ui.Button(emoji="✂️", custom_id="scissors")

    # Define the result calculation function
    async def on_button_click(interaction, button):
        user_choice = button.custom_id
        if user_choice == "rock":
            user_choice_emoji = "🪨"
        elif user_choice == "paper":
            user_choice_emoji = "📄"
        else:
            user_choice_emoji = "✂️"

        # Determine the result of the game
        if user_choice == "rock":
            if bot_choice == "🪨":
                result = "It's a tie! Both chose 🪨"
            elif bot_choice == "📄":
                result = "You lose! Paper beats rock."
            else:
                result = "You win! Rock beats scissors."
        elif user_choice == "paper":
            if bot_choice == "🪨":
                result = "You win! Paper beats rock."
            elif bot_choice == "📄":
                result = "It's a tie! Both chose 📄"
            else:
                result = "You lose! Scissors beats paper."
        else:  # user_choice == "scissors"
            if bot_choice == "🪨":
                result = "You lose! Rock beats scissors."
            elif bot_choice == "📄":
                result = "You win! Scissors beats paper."
            else:
                result = "It's a tie! Both chose ✂️"

        # Send the result and disable the buttons
        await interaction.response.send_message(f"You chose {user_choice_emoji}, and I chose {bot_choice}.\n{result}", ephemeral=True)

        # Disable buttons and update the view
        for button in view.children:
            button.disabled = True
        if "You win" in result:
            try:
                update_count('rps_wins', str(ctx.message.author.id))
            except:
                print(traceback.format_exc())
            winner_text = f"{interaction.user.mention} wins!"
        elif "You lose" in result:
            winner_text = f"I win!"
        else:
            winner_text = "It's a tie!"

        await interaction.message.edit(content=winner_text, view=view)

    # Add the on_click function to buttons
    rock_button.callback = partial(on_button_click, button=rock_button)
    paper_button.callback = partial(on_button_click, button=paper_button)
    scissors_button.callback = partial(on_button_click, button=scissors_button)

    # Add buttons to a view and send the message
    view = discord.ui.View()
    view.add_item(rock_button)
    view.add_item(paper_button)
    view.add_item(scissors_button)
    await ctx.send("Choose your move!", view=view)

@rps.error
async def rps_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = round(error.retry_after, 2)
        em = discord.Embed(
            title="Cooldown Active",
            description=f"You're on cooldown! Try again in **{remaining_time} seconds**.",
            color=discord.Color.red()
        )
        await ctx.reply(embed=em)

@bot.command(name="setbirthday")
async def set_birthday(ctx, date: str):
    """
    Allows users to set their birthday in DD-MM format.

    :param date: The user's birthday in DD-MM format.
    """
    try:
        # Validate the date format
        datetime.strptime(date, "%d-%m")
    except ValueError:
        await ctx.send("Invalid date format! Please use `DD-MM`.")
        return

    # Save the birthday in MongoDB
    client["miscellaneous"]["birthdays"].update_one(
        {"user_id": ctx.author.id},
        {"$set": {"day": date}},
        upsert=True
    )

    await ctx.message.delete()
    await ctx.send(f"🎉 {ctx.author.mention}, your birthday has been saved!", delete_after=3)


wished_birthdays = []

# Background task to check birthdays
@tasks.loop(hours=12)
async def check_birthdays():
    """
    Daily task to check if it's someone's birthday and send a message.
    """
    global wished_birthdays
    # Get the current date in UTC in DD-MM format
    today = datetime.now(timezone("Asia/Kolkata")).strftime("%d-%m")

    # Find users whose birthday matches today's date
    birthdays = client["miscellaneous"]["birthdays"].find({"day": today})

    # Get the announcement channel
    channel = bot.get_channel(1312083452077801524)  ######################################################################################

    # Send birthday wishes
    for user in birthdays:
        user_id = user["user_id"]
        if user_id not in wished_birthdays:
            await channel.send(f"🎂 It's <@{user_id}> birthday ({today} in IST)! 🎉🥳")
            wished_birthdays.append(user_id)


# Before loop starts, ensure the bot is ready
@check_birthdays.before_loop
async def before_check_birthdays():
    """
    Wait until the bot is ready before starting the birthday check loop.
    """
    await bot.wait_until_ready()
    
async def get_leaderboard(action: str):

    db = client["CommandCounts"]
    collection = db[action]
    
    # Fetch top 10 users sorted by count in descending order
    top_users = collection.find().sort("count", -1).limit(10)
    
    # Create a leaderboard embed
    embed = discord.Embed(
        title=f"Leaderboard for {action.capitalize()}",
        description="",
        color=0x00FF00
    )
    
    # Add users to the embed
    for i, user in enumerate(top_users, start=1):
        username = user.get("username", "Unknown User") # In the DB, "username" is actually the user ID
        count = user.get("count", 0)

        try:
            await bot.fetch_user(int(username))
            member = bot.get_user(int(username))
        except:
            member = None

        # Mention or fallback to Unknown User
        if member:
            mention = member.mention
        else:
            mention = f"Unknown User ({username})"
        
        embed.add_field(name=f"#{i}", value=f"{mention}: {count}", inline=False)
    if len(embed.fields) == 0:
        embed = discord.Embed(
        title=f"Leaderboard for {action.capitalize()}",
        description="This command has not been used by anyone before. Why not be the first one?",
        color=0x00FF00
    )
    return embed

@bot.command(name="leaderboard")
async def leaderboard(ctx, action: str = None):
    if action == None:
        await ctx.send("Mention the particular command, the leaderboard of which you wanna check.")
        return
    action = action.lower()
    validactions = list(gif_actions.gifs.keys()) + ["rps_wins", "pop_wins", "firefly_wins"]
    if not (action in validactions):
        await ctx.send(f"'{action}' is not a valid leaderboard option, valid ones are: {', '.join(validactions)}.")
        return
    try:
        embed = await get_leaderboard(action)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error fetching leaderboard: {str(e)}")


async def old_perform_action(ctx, action, user):
    if action not in gif_actions.gifs or action not in gif_actions.messages:
        await ctx.send("Unknown action!")
        return

    acttext, actgif = gif_actions.action_message(action)
    acttext = acttext.format(user=ctx.author.display_name, user2=user.display_name)
    update_count(action, str(ctx.author.id), 1)
    em = discord.Embed(title=acttext, description="")
    em.set_image(url=actgif)
    actcount = client["CommandCounts"][action.lower()].find_one({"username": str(ctx.author.id)})['count']
    em.set_footer(text=f"That's {actcount} {action}s!")
    await ctx.message.channel.send(embed=em)


# Function to update or create entry in the collection
def update_count_user(collection_name: str, username: str, user2: str, count: int = 1):
    """
    Updates or creates an entry in the given MongoDB collection for the specified username.

    :param collection_name: The name of the MongoDB collection.
    :param username: The username whose count to increment.
    :param count: The number to increment (default is 1).
    """
    db = client["GifActions"]  # Replace <dbname> with your database name
    collection = db[collection_name]

    result = collection.update_one(
        {"username": username},
        {
            "$inc": {f"count.{user2}": count}  # Increment the count for the specific user2
        },
        upsert=True
    )
    
async def perform_action(ctx, action, user):
    if action not in gif_actions.gifs or action not in gif_actions.messages:
        await ctx.send("Unknown action!")
        return

    acttext, actgif = gif_actions.action_message(action)
    acttext = acttext.format(user=ctx.author.display_name, user2=user.display_name)
    update_count(action, str(ctx.author.id))
    update_count_user(action, str(ctx.author.id), str(user.id))
    em = discord.Embed(title=acttext, description="")
    em.set_image(url=actgif)
    actcount = client["GifActions"][action.lower()].find_one({"username": str(ctx.author.id)})['count'].get(str(user.id), 0)
    if int(actcount) == 1:
        em.set_footer(text=f"That's {actcount} {action}!")
    elif int(actcount) > 1:
        em.set_footer(text=f"That's {actcount} {action}s!")
    await ctx.message.channel.send(embed=em)

@bot.command(name="hug")
async def hug(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "hug", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to hug.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "hug", user)
        return

@bot.command(name="pat")
async def pat(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "pat", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to pat.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "pat", user)
        return

@bot.command(name="poke")
async def poke(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "poke", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to poke.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "poke", user)
        return

@bot.command(name="punch")
async def punch(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "punch", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to punch.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "punch", user)
        return

@bot.command(name="bite")
async def bite(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "bite", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to bite.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "bite", user)
        return

@bot.command(name="bonk")
async def bonk(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "bonk", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to bonk.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "bonk", user)
        return

@bot.command(name="wag")
async def wag(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "wag", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to wag at.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "wag", user)
        return

@bot.command(name="stare")
async def stare(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "stare", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to stare at.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "stare", user)
        return

@bot.command(name="wave")
async def wave(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "wave", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to wave to.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "wave", user)
        return

@bot.command(name="kill")
async def kill(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "kill", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to kill.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "kill", user)
        return

@bot.command(name="lick")
async def lick(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "lick", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to lick.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "lick", user)
        return

@bot.command(name="kiss")
async def kiss(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "kiss", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to kiss.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "kiss", user)
        return

@bot.command(name="spank")
async def spank(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "spank", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to spank.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "spank", user)
        return

@bot.command(name="kick")
async def kick(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "kick", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to kick.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "kick", user)
        return

@bot.command(name="stab")
async def stab(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "stab", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to stab.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "stab", user)
        return

@bot.command(name="slap")
async def slap(ctx, user: discord.Member = None):
    if user: # if arg
        await perform_action(ctx, "slap", user)
        return
    if not ctx.message.reference: # if no user arg and no reply
        await ctx.send("You need to mention or reply to the user you want to slap.")
        return
    if ctx.message.reference: # if no arg but reply
        user = ctx.message.reference.resolved.author
        await perform_action(ctx, "slap", user)
        return

# self explanatory
bot.run(BOT_TOKEN)
