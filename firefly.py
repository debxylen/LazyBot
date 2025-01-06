import discord
from discord.ext import commands
import random
import json
import asyncio

# Function to update or create entry in the collection
def update_count(collection_name: str, username: str, count: int = 1):
    """
    Updates or creates an entry in the given MongoDB collection for the specified username.

    :param collection_name: The name of the MongoDB collection.
    :param username: The username whose count to increment.
    :param count: The number to increment (default is 1).
    """
    db = client["CommandCounts"]  # Replace <dbname> with your database name
    collection = db[collection_name]

    # Use MongoDB's `update_one` with upsert to update or create the entry
    result = collection.update_one(
        {"username": username},
        {"$inc": {"count": count}},
        upsert=True
    )

class Firefly(commands.Cog):
    def __init__(self, bot, mongoclient):
        self.bot = bot
        global client
        client = mongoclient

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def firefly(self, ctx):
        """Firefly catching game command."""

        if random.choice(['1','0']) == '0':
            em = discord.Embed(
                title='um...',
                description='Guess there were no fireflies in the sky... at least... in your vision...'
            )
            await ctx.reply(embed=em)
            return

        # Firefly emoji
        empty_label = '⬛'

        # Buttons
        view = FireflyView(self, self.bot, ctx)
        embed_message = discord.Embed(title='Catch The Firefly', description='yes')

        # Send embed with the button view
        msg = await ctx.send(embed=embed_message, view=view)

        # Wait for the interaction to complete (via timeout in the view)
        await view.wait()

        if not view.interaction_occurred:
            await self.handle_timeout(ctx, msg)

    @firefly.error
    async def firefly_error(self, ctx, error):
        """Error handler for the firefly command."""
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = round(error.retry_after, 2)
            em = discord.Embed(
                title="Cooldown Active",
                description=f"You're on cooldown! Try again in **{remaining_time} seconds**.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=em)
        else:
            raise error

    async def handle_timeout(self, ctx, msg):
        """Handle timeout scenario when the user does not click a button in time."""
        await msg.delete()
        embed = discord.Embed(
            title='...',
            description='You couldn\'t catch the firefly in time.'
        )
        await ctx.reply(embed=embed)

    async def catch_firefly(self, ctx, msg):
        """Handle successful firefly catch."""
        embed = discord.Embed(
            title='Caught a Firefly',
            description='+1 <:firefly:997182476084596767> firefly',
            color=0x05ed05
        )
        user_id = str(ctx.message.author.id)

        if msg:
            await msg.delete()
        await ctx.send(embed=embed)
        update_count('firefly_wins', str(ctx.message.author.id))


class FireflyView(discord.ui.View):
    def __init__(self, cog, bot, ctx):
        super().__init__(timeout=5)  # Set timeout
        self.cog = cog
        self.ctx = ctx
        self.bot = bot
        self.interaction_occurred = False

        # Generate buttons
        self.add_buttons()

    def add_buttons(self):
        """Add buttons to the view."""
        empty_label = '⬛'
        firefly_emoji = self.bot.get_emoji(997182476084596767)
        win_pos = random.randint(0, 8)

        for i in range(3):
            if i == win_pos:
                self.add_item(FireflyButton(label='', emoji=firefly_emoji, custom_id=f'firefly_catch', cog=self.cog, ctx = self.ctx, row = 0))
            else:
                self.add_item(FireflyButton(label='', emoji=empty_label, custom_id=f'firefly_{i}', cog=self.cog, ctx = self.ctx, row = 0))

        for i in range(3, 6):
            if i == win_pos:
                self.add_item(FireflyButton(label='', emoji=firefly_emoji, custom_id=f'firefly_catch', cog=self.cog, ctx = self.ctx, row = 1))
            else:
                self.add_item(FireflyButton(label='', emoji=empty_label, custom_id=f'firefly_{i}', cog=self.cog, ctx = self.ctx, row = 1))

        for i in range(6, 9):
            if i == win_pos:
                self.add_item(FireflyButton(label='', emoji=firefly_emoji, custom_id=f'firefly_catch', cog=self.cog, ctx = self.ctx, row = 2))
            else:
                self.add_item(FireflyButton(label='', emoji=empty_label, custom_id=f'firefly_{i}', cog=self.cog, ctx = self.ctx, row = 2))


class FireflyButton(discord.ui.Button):
    def __init__(self, label=None, emoji=None, custom_id=None, cog=None, ctx = None, row = None):
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.secondary, custom_id=custom_id, row = row)
        self.cog = cog
        self.ctx = ctx
        self.row = row

    async def callback(self, interaction: discord.Interaction):
        """Handle button interaction."""
        self.view.interaction_occurred = True
        await interaction.response.defer()

        if self.custom_id == 'firefly_catch':
            # Successful catch
            await self.cog.catch_firefly(self.ctx, interaction.message)
        else:
            # Failed attempt
            embed = discord.Embed(
                title='F',
                description='You failed to catch the firefly. Nothing else happened. Except pure disappointment.',
                color=0xed0505
            )
            await interaction.message.delete()
            await self.ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Firefly(bot))
