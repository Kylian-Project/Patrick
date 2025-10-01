"""
Événement on_ready - Quand le bot est prêt
"""

import discord
from discord.ext import commands
from datetime import datetime

class OnReady(commands.Cog):
    """Gère l'événement de démarrage du bot"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Événement déclenché quand le bot est connecté et prêt"""
        print("=" * 50)
        print(f"🤖 Bot connecté: {self.bot.user.name}")
        print(f"🆔 ID: {self.bot.user.id}")
        print(f"📊 Serveurs: {len(self.bot.guilds)}")
        print(f"👥 Utilisateurs: {sum(guild.member_count for guild in self.bot.guilds)}")
        print(f"⏰ Heure de connexion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Définir le statut d'activité
        activity = discord.Game(name=self.bot.config.get('status_message', '!help | En développement'))
        await self.bot.change_presence(activity=activity, status=discord.Status.online)
        
        # Log dans le fichier
        self.bot.logger.info(f"Bot {self.bot.user.name} connecté avec succès")
        self.bot.logger.info(f"Présent sur {len(self.bot.guilds)} serveurs")

async def setup(bot):
    await bot.add_cog(OnReady(bot))