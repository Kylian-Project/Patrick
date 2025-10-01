"""
Commandes de modération
"""

import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Moderation(commands.Cog):
    """Commandes de modération du serveur"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 1):
        """Supprime un nombre spécifié de messages"""
        if amount < 1:
            await ctx.send("❌ Le nombre doit être supérieur à 0!")
            return
        
        if amount > 100:
            await ctx.send("❌ Vous ne pouvez pas supprimer plus de 100 messages à la fois!")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 pour inclure la commande
            
            embed = discord.Embed(
                title="🧹 Messages supprimés",
                description=f"{len(deleted) - 1} messages ont été supprimés par {ctx.author.mention}",
                color=0x00ff00
            )
            
            confirmation = await ctx.send(embed=embed)
            
            # Supprimer le message de confirmation après 5 secondes
            await asyncio.sleep(5)
            await confirmation.delete()
            
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas la permission de supprimer des messages!")
        except discord.HTTPException:
            await ctx.send("❌ Erreur lors de la suppression des messages!")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
