"""
Commandes générales du bot
"""

import discord
from discord.ext import commands
from discord import app_commands
import time
import platform

class General(commands.Cog):
    """Commandes générales et utilitaires"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping")
    @app_commands.describe()
    async def ping(self, ctx):
        """Affiche la latence du bot"""
        start_time = time.time()
        message = await ctx.send("🏓 Pong!")
        end_time = time.time()
        
        latency = round((end_time - start_time) * 1000)
        api_latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            color=0x00ff00
        )
        embed.add_field(name="Latence du message", value=f"{latency}ms", inline=True)
        embed.add_field(name="Latence API", value=f"{api_latency}ms", inline=True)
        
        await message.edit(content="", embed=embed)
       
    @commands.command(name="info", aliases=["botinfo"])
    async def info_command(self, ctx):
        """Informations sur le bot"""
        embed = discord.Embed(
            title="📊 Informations du Bot",
            color=0x3498db
        )
        
        embed.add_field(
            name="👑 Développeur",
            value=f"<@{self.bot.owner_id}>" if self.bot.owner_id else "Non défini",
            inline=True
        )
        embed.add_field(
            name="📊 Serveurs",
            value=len(self.bot.guilds),
            inline=True
        )
        embed.add_field(
            name="👥 Utilisateurs",
            value=sum(guild.member_count for guild in self.bot.guilds),
            inline=True
        )
        embed.add_field(
            name="🐍 Version Python",
            value=platform.python_version(),
            inline=True
        )
        embed.add_field(
            name="📚 Version Discord.py",
            value=discord.__version__,
            inline=True
        )
        
        embed.set_footer(text=f"Bot ID: {self.bot.user.id}")
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="help")
    async def help_command(self, ctx, *, command=None):
        """Système d'aide personnalisé"""
        if command:
            # Aide pour une commande spécifique
            cmd = self.bot.get_command(command)
            if cmd:
                embed = discord.Embed(
                    title=f"Aide - {cmd.name}",
                    description=cmd.help or "Aucune description disponible",
                    color=0x3498db
                )
                if cmd.aliases:
                    embed.add_field(name="Aliases", value=", ".join(cmd.aliases), inline=False)
                embed.add_field(name="Usage", value=f"`{ctx.prefix}{cmd.name} {cmd.signature}`", inline=False)
            else:
                embed = discord.Embed(
                    title="❌ Erreur",
                    description=f"La commande `{command}` n'existe pas.",
                    color=0xe74c3c
                )
        else:
            # Liste générale des commandes
            embed = discord.Embed(
                title="📋 Liste des commandes",
                description="Voici toutes les commandes disponibles:",
                color=0x3498db
            )
            
            # Grouper les commandes par cog
            for cog_name, cog in self.bot.cogs.items():
                commands_list = [cmd.name for cmd in cog.get_commands() if not cmd.hidden]
                if commands_list:
                    embed.add_field(
                        name=f"📁 {cog_name}",
                        value=", ".join(f"`{cmd}`" for cmd in commands_list),
                        inline=False
                    )
            
            embed.set_footer(text=f"Utilisez {ctx.prefix}help <commande> pour plus d'informations")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))