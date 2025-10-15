"""
Bot Discord principal
"""

import os
import logging
import asyncio
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .utils.config_loader import ConfigLoader
from .utils.logger import setup_logging

# Charger les variables d'environnement
load_dotenv()

class DiscordBot(commands.Bot):
    """Classe principale du bot Discord"""
    
    def __init__(self):
        # Configuration des intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guild_messages = True
        intents.guilds = True
        intents.members = True
        
        # Initialisation du bot
        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            help_command=None,  # Désactiver l'aide par défaut
            case_insensitive=True
        )
        
        # Configuration
        self.config = ConfigLoader()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Variables du bot
        self.start_time = None
        self.owner_id = int(os.getenv('OWNER_ID')) if os.getenv('OWNER_ID') else None
        
    async def get_prefix(self, message):
        """Récupère le préfixe pour les commandes"""
        if not message.guild:
            return self.config.get('default_prefix', '!')
        
        return self.config.get('default_prefix', '!')
    
    async def setup_hook(self):
        """Configuration initiale du bot"""
        self.logger.info("Configuration du bot en cours...")
        
        # Charger les cogs (modules de commandes)
        await self.load_cogs()
    
    async def load_cogs(self):
        """Charge tous les cogs (modules de commandes)"""
        cogs_to_load = [
            'src.commands.general',
            'src.commands.moderation',
            'src.commands.crous',
            'src.commands.fun',
            'src.events.on_ready'
        ]
        
        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                self.logger.info(f"Cog chargé: {cog}")
            except Exception as e:
                self.logger.error(f"Erreur lors du chargement de {cog}: {e}")
    
    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""
        self.logger.info(f'{self.user} est connecté!')
        self.logger.info(f'ID: {self.user.id}')
        self.logger.info(f'Serveurs: {len(self.guilds)}')
        
        # Définir le statut du bot
        await self.change_presence(
            activity=discord.Game(name=self.config.get('status_message', 'En développement'))
        )
    
    async def on_command_error(self, ctx, error):
        """Gestion globale des erreurs de commandes"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignorer les commandes inexistantes
        
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Vous n'avez pas les permissions nécessaires pour cette commande.")
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Argument manquant: `{error.param.name}`")
        
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Argument invalide. Vérifiez votre syntaxe.")
        
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏰ Commande en cooldown. Réessayez dans {error.retry_after:.1f}s")
        
        else:
            self.logger.error(f"Erreur de commande: {error}")
            await ctx.send("❌ Une erreur inattendue s'est produite.")
    
    async def start_bot(self):
        """Démarre le bot"""
        token = os.getenv('DISCORD_TOKEN')
        
        if not token:
            self.logger.error("Token Discord non trouvé dans les variables d'environnement!")
            return
        
        try:
            await self.start(token)
        except discord.LoginFailure:
            self.logger.error("Token Discord invalide!")
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage: {e}")
