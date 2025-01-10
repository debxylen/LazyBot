import discord
from discord.ext import commands
from discord.ui import Button, View
from predefined_gifs import gifs as pgifs

class GifApprovalCog(commands.Cog):
    def __init__(self, bot, mongo_client):
        self.bot = bot
        self.db = mongo_client

    # List of whitelisted user IDs
    whitelisted_users = [413154673403363328, 651824112942972964, 514422004951154698]  # Replace with actual user IDs

    @commands.command(name="gif")
    async def approve_gif(self, ctx, param1):
        if ctx.author.id not in self.whitelisted_users:
            return
        if param1 not in pgifs: # pgifs contains all gifs name as keys so if param1 is not one of them, its not a valid action.
            await ctx.send("No such GIF action.")
            return
        # Get the list of URLs from the original collection
        original_gif_list = self.db["GifApprovals"][param1].find_one({}, {"urls": 1})  # Get first document's 'url' field
        if not original_gif_list or not original_gif_list.get('urls'):
            await ctx.send(f"No GIFs available for approval in '{param1}'.")
            return

        gif_urls = original_gif_list['urls']

        if not gif_urls:
            await ctx.send(f"No GIFs found in the list for '{param1}'.")
            return

        # Get the first URL
        gif_url = gif_urls[0]

        # Create an embed for the GIF
        embed = discord.Embed(title="GIF Approval", description=f"Approve or reject this GIF for '{param1}'.", color=0x00FF00)
        embed.set_image(url=gif_url)
        
        # Create approve and reject buttons
        async def approve(interaction):
            # Add the GIF to the ApprovedGifs collection
            self.db["ApprovedGifs"][param1].update_one(
                {}, {'$addToSet': {'urls': gif_url}}, upsert=True
            )
            # Remove from the original list
            self.db["GifApprovals"][param1].update_one(
                {}, {'$pull': {'urls': gif_url}}
            )
            # await interaction.response.send_message(f"GIF approved and moved to '{param1}' approved list.", ephemeral=True)
            await interaction.message.delete()
            await self.show_next_gif(ctx, param1)

        async def reject(interaction):
            # Remove from the original list
            self.db["GifApprovals"][param1].update_one(
                {}, {'$pull': {'urls': gif_url}}
            )
            # await interaction.response.send_message(f"GIF rejected and removed from the list.", ephemeral=True)
            await interaction.message.delete()
            await self.show_next_gif(ctx, param1)

        # Create the buttons
        approve_button = Button(label="✔", style=discord.ButtonStyle.green)
        reject_button = Button(label="❌", style=discord.ButtonStyle.red)

        approve_button.callback = approve
        reject_button.callback = reject

        # Create a view for the buttons
        view = View(timeout=10)
        view.add_item(approve_button)
        view.add_item(reject_button)

        # Send the embed and the buttons
        await ctx.send(embed=embed, view=view, delete_after=10)

    # Function to loop and show the next GIF
    async def show_next_gif(self, ctx, param1):
        await self.approve_gif(ctx, param1)

