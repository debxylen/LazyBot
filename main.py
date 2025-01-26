import re
import traceback
from typing import Optional
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord import app_commands
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
from gifapproval import GifApprovalCog
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
    await bot.add_cog(GifApprovalCog(bot, client))
    await bot.tree.sync()
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
    elif 'rps lb' in message.content.lower():  # Case-insensitive match for rps lb
        message.content = re.sub(r"(?i)rps lb", "rps_lb", message.content, 1) #convert to rps_lb
        await bot.process_commands(message)
    else:
        await bot.process_commands(message)

@bot.command()
async def sync(ctx):
    fmt = await bot.tree.sync()
    await ctx.send(f"{len(fmt)} commands synced.")


# Function to update or create entry in the collection
def update_respect(userid: str, count):
    db = client["miscellaneous"]
    collection = db["respects"]

    return collection.update_one(
        {"user": userid},
        {
            "$set": {'count': count, 'date': str(datetime.now(timezone("Asia/Kolkata")).strftime("%B %d, %Y"))}
        },
        upsert=True
    )

# Function to update or create entry in the collection
def get_respect(userid: str):
    db = client["miscellaneous"]
    collection = db["respects"]

    result = collection.find_one({"user": userid})
    return result if result else {}

# F Command
@bot.hybrid_command(name='f', with_app_command=True)
async def f(ctx, *, member: discord.Member):
    username = str(member.mention)
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

    past_respects_record = get_respect(str(member.id)).get('respects', 0)
    if len(respects[username]) > past_respects_record:
        update_respect(str(member.id), len(respects[username]))

    if len(respects[username])==1:
        await ctx.send(f"{len(respects[username])} person paid their respect to {username}.")    
    elif len(respects[username])==0:
        await ctx.send(f"No one paid their respects to {username} :(")
    else:
        await ctx.send(f"{len(respects[username])} people paid their respects to {username}.")

# Yes/No Command
@bot.hybrid_command(name='yn', with_app_command=True)
async def yes_no(ctx, *, question):
    response = random.choice([["🇾", "🇪", "🇸"], ["🇳", "🇴"]])  # Random Yes or No

    # Send a message with the question and user's mention
    message = await ctx.send(f":crystal_ball: {ctx.author.mention} asked: *{question}*")
    await ctx.message.delete()  # Delete the user's message

    # React with separate letters for the chosen response
    for letter in response:
        await message.add_reaction(letter)

# Pop Command
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.hybrid_command(name='pop', with_app_command=True)
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
    else:
        print(traceback.format_exc())

# Define moves and winner logic
MOVES = ["rock", "paper", "scissors"]

def determine_winner(choice1, choice2, p1, p2):
    if choice1 == choice2:
        return f"It's a tie between {p1.mention} and {p2.mention}!", None, None
    if (choice1 == "rock" and choice2 == "scissors") or \
       (choice1 == "paper" and choice2 == "rock") or \
       (choice1 == "scissors" and choice2 == "paper"):
        return f"{p1.mention} wins!", p1, p2
    return f"{p2.mention} wins!", p2, p1

async def bot_rps(ctx):
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
                await update_rps_stats(str(ctx.message.author), str(bot))
                update_count('rps_wins', str(ctx.message.author.id))
            except:
                print(traceback.format_exc())
            winner_text = f"{interaction.user.mention} wins!"
        elif "You lose" in result:
            winner_text = f"I win!"
            await update_rps_stats(str(bot), str(ctx.message.author))
        else:
            winner_text = "It's a tie!"
            await update_tie(ctx.author, opponent)

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

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.hybrid_command(name='rps', with_app_command=True)
async def rps(ctx, opponent: discord.Member):
    if opponent == ctx.author:
        await ctx.send("You can't challenge yourself!", delete_after=5)
        return
    elif opponent == bot:
        await bot_rps(ctx)
        return

    # Create buttons for both players
    class MoveButton(Button):
        def __init__(self, emoji, player, parent, cid):
            super().__init__(emoji=emoji, custom_id=cid, style=discord.ButtonStyle.primary)
            self.player = player  # This will track the player the button belongs to
            self.parent = parent

        async def callback(self, interaction: discord.Interaction):
            nonlocal player1_locked, player2_locked, player1_choice, player2_choice
            # Check if the interaction is from the correct player
            await interaction.response.defer()
            if interaction.user == self.player:
                choice = self.custom_id
                if self.player == ctx.author:
                    player1_choice = choice
                    player1_locked = True
                elif self.player == opponent:
                    player2_choice = choice
                    player2_locked = True

            # Once both players have chosen, determine the winner
            if player1_locked and player2_locked:
                await challenge_message1.delete() #edit(view=View())
                await challenge_message2.delete() #edit(view=View())
                await self.parent.reply(f"Moves locked.")
                time.sleep(1)
                emojimapping = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
                result, winner, loser = determine_winner(player1_choice, player2_choice, ctx.author, opponent)
                await self.parent.reply(f"{ctx.author} chose {emojimapping[player1_choice]}, {opponent} chose {emojimapping[player2_choice]}. {result}")
                if winner:
                    update_count('rps_wins', str(winner.id))
                    await update_rps_stats(winner, loser)
                elif winner is None:
                    await update_tie(ctx.author, opponent)

    # Send the challenge message
    challenge_message = await ctx.send(f"{ctx.author.mention} challenged {opponent.mention} to a game of Rock, Paper, Scissors!")

    # Add buttons for both players
    view1 = View(timeout=None)
    view1.add_item(MoveButton("🪨", ctx.author, challenge_message, 'rock'))  # Rock button for the challenger
    view1.add_item(MoveButton("📄", ctx.author, challenge_message, 'paper'))  # Paper button for the challenger
    view1.add_item(MoveButton("✂️", ctx.author, challenge_message, 'scissors'))  # Scissors button for the challenger

    view2 = View(timeout=None)
    view2.add_item(MoveButton("🪨", opponent, challenge_message, 'rock'))  # Rock button for the opponent
    view2.add_item(MoveButton("📄", opponent, challenge_message, 'paper'))  # Paper button for the opponent
    view2.add_item(MoveButton("✂️", opponent, challenge_message, 'scissors'))  # Scissors button for the opponent

    challenge_message1 = await ctx.send(f"{ctx.author.mention}, choose your move.", view=view1)
    challenge_message2 = await ctx.send(f"{opponent.mention}, choose your move.", view=view2)

    # Initialize move variables and locked states
    player1_locked = False
    player2_locked = False
    player1_choice = None
    player2_choice = None

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
    else:
        print(traceback.format_exc())

async def update_rps_stats(winner, loser):
    # Get winner's document or create a new one
    global client
    client = client if client else MongoClient(mongo_uri)
    winner_doc = client["GameWins"]["Rps"].find_one({"user_id": str(winner.id)})
    if not winner_doc:
        winner_doc = {"user_id": str(winner.id), "opponents": {}}

    # Update the winner's opponent stats
    opponent_entry = winner_doc["opponents"].get(str(loser.id), {"wins": 0, "losses": 0, "ties": 0})
    opponent_entry["wins"] += 1
    winner_doc["opponents"][str(loser.id)] = opponent_entry  # Update the opponent's stats in the dictionary

    # Save or update winner document
    client["GameWins"]["Rps"].replace_one({"user_id": str(winner.id)}, winner_doc, upsert=True)

    # Get loser's document or create a new one
    loser_doc = client["GameWins"]["Rps"].find_one({"user_id": str(loser.id)})
    if not loser_doc:
        loser_doc = {"user_id": str(loser.id), "opponents": {}}

    # Update the loser's opponent stats
    opponent_entry = loser_doc["opponents"].get(str(winner.id), {"wins": 0, "losses": 0, "ties": 0})
    opponent_entry["losses"] += 1
    loser_doc["opponents"][str(winner.id)] = opponent_entry  # Update the opponent's stats in the dictionary

    # Save or update loser document
    client["GameWins"]["Rps"].replace_one({"user_id": str(loser.id)}, loser_doc, upsert=True)

async def update_tie(player1, player2):
    global client
    client = client if client else MongoClient(mongo_uri)
    # Update player1's stats
    player_doc = client["GameWins"]["Rps"].find_one({"user_id": str(player1.id)})
    if not player_doc:
        player_doc = {"user_id": str(player1.id), "opponents": {}}
    
    opponent_entry = player_doc["opponents"].get(str(player2.id), {"wins": 0, "losses": 0, "ties": 0})
    opponent_entry["ties"] += 1
    player_doc["opponents"][str(player2.id)] = opponent_entry
    
    client["GameWins"]["Rps"].replace_one({"user_id": str(player1.id)}, player_doc, upsert=True)

    # Update player2's stats
    player_doc = client["GameWins"]["Rps"].find_one({"user_id": str(player2.id)})
    if not player_doc:
        player_doc = {"user_id": str(player2.id), "opponents": {}}
    
    opponent_entry = player_doc["opponents"].get(str(player1.id), {"wins": 0, "losses": 0, "ties": 0})
    opponent_entry["ties"] += 1
    player_doc["opponents"][str(player1.id)] = opponent_entry
    
    client["GameWins"]["Rps"].replace_one({"user_id": str(player2.id)}, player_doc, upsert=True)


async def get_rps_leaderboard(sender, opponent):
    global client
    # Get sender's document
    sender_doc = client["GameWins"]["Rps"].find_one({"user_id": str(sender.id)})
    if not sender_doc:
        return None

    # Find the opponent in the sender's opponents list
    opponent_stats = sender_doc["opponents"].get(str(opponent.id), None)
    if not (opponent_stats == None or all(v == 0 for k,v in opponent_stats.items())):
        return opponent_stats
    else:
        return None

challenging_lines = [
    "**{0}**: You scared? Let's do RPS, I'll still win, **{1}**!",
    "**{0}** challenges **{1}** to a match of RPS, ready to lose?",
    "**{0}**: C'mon **{1}**, show me what you got in RPS... if you can!",
    "**{0}**: I bet you can't even beat me at rock, paper, scissors, **{1}**!",
    "**{0}** dares **{1}** to an RPS showdown! Think you can win?",
    "**{0}**: I'm already winning this, **{1}**. Wanna try me in RPS?",
    "**{0}**: Let's settle this like legends—RPS style! Come at me, **{1}**!",
    "**{0}**: Think you're the boss, **{1}**? Prove it in an RPS battle!",
    "**{0}**: Time to dethrone you, **{1}**. Rock, paper, scissors, now!",
    "**{0}**: I'm feeling lucky, **{1}**. You game for an RPS match?",
    "**{0}**: RPS me, **{1}**. Or are you too chicken to lose?",
    "**{0}**: Hey **{1}**, I need someone to beat in RPS. You available?",
    "**{0}**: Can't wait to crush you in RPS, **{1}**. Let's go!",
    "**{0}**: Only one of us walks away victorious, **{1}**. RPS me!",
    "**{0}**: If you think you're good, **{1}**, prove it in RPS!"
]

@bot.hybrid_command(name="rps_lb", with_app_command=True)
async def rps_lb(ctx, opponent: discord.Member):
    if opponent == ctx.author:
        await ctx.send(embed=discord.Embed(title="That's you.", description="The competition is always with yourself, but you can't play against yourself."))
        return
    await ctx.send('Fetching leaderboard data...')
    # Get the leaderboard stats
    leaderboard = await get_rps_leaderboard(ctx.author, opponent)
    if leaderboard == None:
        await ctx.send(embed=discord.Embed(title=f"There has been no RPS match between you and {opponent.display_name}...", description = f"No data found, Challenge the user to store data.\n\n{random.choice(challenging_lines).format(ctx.author.display_name, opponent.display_name)}"))
        return
    # Create the embed
    embed = discord.Embed(
        title=f"RPS Leaderboard: {ctx.author.display_name} vs {opponent.display_name}",
        description=f"{ctx.author.mention}'s **Wins**: {leaderboard['wins']}\n**Losses**: {leaderboard['losses']}\n**Ties**: {leaderboard['ties']}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

wished_birthdays = []

@bot.hybrid_command(name='setbirthday', with_app_command=True)
async def set_birthday(ctx, *, date):
    """Allows users to set their birthday in DD-MM format.
    :param date: The user's birthday in DD-MM format.
    """
    
    # Send the "Please wait..." message
    waitmsg = await ctx.send('Please wait...')

    try:
        # Validate the date format
        datetime.strptime(date, "%d-%m")
    except ValueError:
        await ctx.send("Invalid date format! Please use `DD-MM`.")
        await waitmsg.delete()  # Delete the wait message if an error occurs
        return
    
    # Save the birthday in MongoDB
    client["miscellaneous"]["birthdays"].update_one(
        {"user_id": ctx.author.id},
        {"$set": {"day": date}},
        upsert=True
    )
    
    # Delete the wait message once the operation is done
    await waitmsg.delete()

    # Confirm to the user that their birthday has been saved
    await ctx.send(f"🎉 {ctx.author.mention}, your birthday has been saved!", delete_after=3)

    today = datetime.now(timezone("Asia/Kolkata")).strftime("%d-%m")
    
    if date == today:
        global wished_birthdays
        user_id = ctx.author.id
        user_name = ctx.author.name
        today_human = datetime.strptime(today, "%d-%m").strftime("%-d %B")
        
        # Send a birthday message in a specific channel
        await bot.get_channel(1298215054633861124).send(
            f"🎂 <@&1298162816922161162>, It's <@{user_id}>'s ({user_name}) birthday ({today_human} in IST)! 🎉🥳"
        )
        
        wished_birthdays.append(user_id)
    await ctx.message.delete()

# Background task to check birthdays
@tasks.loop(hours=12)
async def check_birthdays():
    """
    Daily task to check if it's someone's birthday and send a message.
    """
    global wished_birthdays
    # Get the current date in UTC in DD-MM format
    today = datetime.now(timezone("Asia/Kolkata")).strftime("%d-%m")
    today_human = datetime.strptime(today, "%d-%m").strftime("%d %B")

    # Find users whose birthday matches today's date
    birthdays = client["miscellaneous"]["birthdays"].find({"day": today})

    # Get the announcement channel
    channel = bot.get_channel(1298215054633861124)
    
    # Send birthday wishes
    for user in birthdays:
        user_id = user["user_id"]
        user_name = bot.get_user(user_id).name
        if user_id not in wished_birthdays:
            await channel.send(f"🎂 <@&1298162816922161162>, It's <@{user_id}>'s ({user_name}) birthday ({today_human} in IST)! 🎉🥳")
            wished_birthdays.append(user_id)


# b4 loop starts, ensure the bot is ready
@check_birthdays.before_loop
async def before_check_birthdays():
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

async def get_respectlb():
    db = client["miscellaneous"]
    collection = db['respects']
    
    # Fetch top 10 users sorted by count in descending order
    top_users = collection.find().sort("count", -1).limit(10)
    
    # Create a leaderboard embed
    embed = discord.Embed(
        title=f"Leaderboard for Respects",
        description="",
        color=0x00FF00
    )
    
    # Add users to the embed
    for i, user in enumerate(top_users, start=1):
        username = user.get("user", "Unknown User")
        count = user.get("count", 0)
        date = user.get("date", "Unknown Date")

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
        
        embed.add_field(name=f"#{i}", value=f"{mention}: {count}, {date}", inline=False)
    if len(embed.fields) == 0:
        embed = discord.Embed(
        title=f"Leaderboard for Respects",
        description="It's crazy how no one has made a record for respects till now.",
        color=0x00FF00
    )
    return embed


@bot.hybrid_command(name='leaderboard', with_app_command=True)
@app_commands.choices(command=[app_commands.Choice(name=x,value=x) for x in list(gif_actions.gifs.keys()) + ["respects", "rps", "pop", "firefly"]])
async def leaderboard(ctx, command):
    lbmsg = await ctx.send('Fetching leaderboard...')
    if type(command) == app_commands.Choice[str]:
        action = command.value
    else:
        action = command
    if action == 'None' or action == None:
        await lbmsg.edit(content="Mention the particular command, the leaderboard of which you wanna check.")
        return
    action = action.lower()
    if action in ["rps", "pop", "firefly"]:
        action = action + '_wins'
    validactions = list(gif_actions.gifs.keys()) + ["respects", "rps_wins", "pop_wins", "firefly_wins"]
    if not (action in validactions):
        await lbmsg.edit(content=f"{action!r} is not a valid leaderboard option, valid ones are: {', '.join(validactions)}.")
        return
    try:
        if not (action == 'respects'):
            embed = await get_leaderboard(action)
        else:
            embed = await get_respectlb()
        await lbmsg.edit(content='', embed=embed)
    except Exception as e:
        await lbmsg.edit(content=f"Error fetching leaderboard: {str(e)}")

@bot.hybrid_command(name='lb', with_app_command=True)
@app_commands.choices(command=[app_commands.Choice(name=x,value=x) for x in list(gif_actions.gifs.keys()) + ["respects", "rps", "pop", "firefly"]])
async def lb(ctx, command):
    lbmsg = await ctx.send('Fetching leaderboard...')
    if type(command) == app_commands.Choice[str]:
        action = command.value
    else:
        action = command
    if action == 'None' or action == None:
        await lbmsg.edit(content="Mention the particular command, the leaderboard of which you wanna check.")
        return
    action = action.lower()
    if action in ["rps", "pop", "firefly"]:
        action = action + '_wins'
    validactions = list(gif_actions.gifs.keys()) + ["respects", "rps_wins", "pop_wins", "firefly_wins"]
    if not (action in validactions):
        await lbmsg.edit(content=f"{action!r} is not a valid leaderboard option, valid ones are: {', '.join(validactions)}.")
        return
    try:
        if not (action == 'respects'):
            embed = await get_leaderboard(action)
        else:
            embed = await get_respectlb()
        await lbmsg.edit(content='', embed=embed)
    except Exception as e:
        await lbmsg.edit(content=f"Error fetching leaderboard: {str(e)}")

@leaderboard.error
async def leaderboard_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mention the particular command, the leaderboard of which you wanna check.")
        return
@lb.error
async def lb_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mention the particular command, the leaderboard of which you wanna check.")
        return

# Function to update or create entry in the collection
def update_count_user(collection_name: str, username: str, user2: str, count: int = 1):
    """
    Updates or creates an entry in the given MongoDB collection for the specified username.

    :param collection_name: The name of the MongoDB collection.
    :param username: The username whose count to increment.
    :param count: The number to increment (default is 1).
    """
    db = client["GifActions"] 
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
    await ctx.send(embed=em)

@bot.hybrid_command(name='pat', with_app_command=True)
async def pat(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='poke', with_app_command=True)
async def poke(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='punch', with_app_command=True)
async def punch(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='bite', with_app_command=True)
async def bite(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='bonk', with_app_command=True)
async def bonk(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='wag', with_app_command=True)
async def wag(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='stare', with_app_command=True)
async def stare(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='wave', with_app_command=True)
async def wave(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='kill', with_app_command=True)
async def kill(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='lick', with_app_command=True)
async def lick(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='kiss', with_app_command=True)
async def kiss(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='spank', with_app_command=True)
async def spank(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='kick', with_app_command=True)
async def kick(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='stab', with_app_command=True)
async def stab(ctx, *, user: discord.Member = None):
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

@bot.hybrid_command(name='slap', with_app_command=True)
async def slap(ctx, *, user: discord.Member = None):
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

@bot.event
async def on_command_error(ctx, error):
    command = ctx.command.name

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Error in command {command!r}: Missing argument {error.param!r}!")

# self explanatory
bot.run(BOT_TOKEN)
