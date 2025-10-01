"""
Configuration du système de logging
"""

import logging
import os
from datetime import datetime

def setup_logging(log_level: str = "INFO") -> None:
    """Configure le système de logging"""
    
    # Créer le dossier logs s'il n'existe pas
    os.makedirs("logs", exist_ok=True)
    
    # Configuration du niveau de log
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler pour fichier
    file_handler = logging.FileHandler(
        f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    # Configuration du logger principal
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Réduire le niveau de logging de discord.py
    logging.getLogger('discord').setLevel(logging.WARNING)
    logging.getLogger('discord.http').setLevel(logging.WARNING)
