#!/usr/bin/env python3
"""
Discord Bot - Point d'entrée principal
"""

import asyncio
import logging
import os
from pathlib import Path

from src.bot import DiscordBot

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Fonction principale pour lancer le bot"""
    try:
        if not os.path.exists('.env'):
            logger.error("Fichier .env non trouvé !")
            return
        
        # Initialiser et démarrer le bot
        bot = DiscordBot()
        await bot.start_bot()
        
    except KeyboardInterrupt:
        logger.info("Arrêt du bot demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
    finally:
        logger.info("Bot arrêté")

if __name__ == "__main__":
    # Créer le dossier logs s'il n'existe pas
    Path("logs").mkdir(exist_ok=True)
    
    # Lancer le bot
    asyncio.run(main())
