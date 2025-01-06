import discord
from discord.ext import commands
from discord.ui import View

class Button(discord.ui.Button):
    def __init__(self, label=None, custom_id=None):
        super().__init__(label=label, style=discord.ButtonStyle.secondary, custom_id=custom_id)
        self.custom_id = custom_id

    async def callback(self, interaction: discord.Interaction):
        """Handle button interaction."""

        if self.custom_id == "actions":
            embed = discord.Embed(
                title="Actions Commands",
                description="These are the action-related commands. Click on them to use.",
                color=discord.Color.green()
            )

            embed.add_field(name="bite", value="Bite your target!", inline=False)
            embed.add_field(name="hug", value="Hug someone with love!", inline=False)
            embed.add_field(name="kick", value="Kick your target for fun!", inline=False)
            embed.add_field(name="kill", value="Self explanatory.", inline=False)
            embed.add_field(name="kiss", value="A sweet kiss for someone special.", inline=False)
            embed.add_field(name="lick", value="Lick your target.", inline=False)
            embed.add_field(name="spank", value="Spank someone for fun.", inline=False)
            embed.add_field(name="wave", value="Wave to everyone!", inline=False)
            await interaction.response.edit_message(embed=embed, view=view)

        elif self.custom_id == "games":
            embed = discord.Embed(
                title="Games Commands",
                description="Enjoy these game-related commands!",
                color=discord.Color.orange()
            )
            embed.add_field(name="rps", value="Play Rock, Paper, Scissors!", inline=False)
            embed.add_field(name="firefly", value="Catch the firefly before it flies away.", inline=False)
            embed.add_field(name="pop", value="Find the ring in 3 attempts!", inline=False)
            await interaction.response.edit_message(embed=embed, view=view)
        
        elif self.custom_id == "fun":
            embed = discord.Embed(
                title="Fun Commands",
                description="Get your fun dose with these commands.",
                color=discord.Color.purple()
            )

            embed.add_field(name="yn", value="Using AI and Machine Learning, a rational answer to the question is given.", inline=False)
            embed.add_field(name="F", value="Pay your respects to someone.", inline=False)
            await interaction.response.edit_message(embed=embed, view=view)
        
        elif self.custom_id == "utility":
            embed = discord.Embed(
                title="Miscellaneous Commands",
                description="These are the Miscellaneous or Utility commands.",
                color=discord.Color.red()
            )
            embed.add_field(name="setbirthday", value="Set your birthday in DD-MM format", inline=False)
            embed.add_field(name="leaderboard", value="View the leaderboard for different activities and commands.", inline=False)
            await interaction.response.edit_message(embed=embed, view=view)

view = None
class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        global view
        # Create a main embed with buttons for categories
        embed = discord.Embed(
            title="Help Menu",
            description="Click on a category to see the commands in that category.",
            color=discord.Color.blue()
        )

        # Buttons for each category
        buttons = [
            Button(label="Actions", custom_id="actions"),
            Button(label="Games", custom_id="games"),
            Button(label="Fun", custom_id="fun"),
            Button(label="Miscellaneous", custom_id="utility"),
        ]
        
        view = View()
        for button in buttons:
            view.add_item(button)
        
        await ctx.send(embed=embed, view=view)
	