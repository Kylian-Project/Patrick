"""
Utilitaires pour la configuration
"""

import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Classe pour charger et gérer la configuration"""
    
    def __init__(self, config_file: str = "config/config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Configuration par défaut"""
        return {
            "default_prefix": "!",
            "status_message": "En développement",
            "embed_color": 0x00ff00,
            "log_level": "INFO"
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Définit une valeur de configuration"""
        self.config[key] = value
    
    def save_config(self) -> bool:
        """Sauvegarde la configuration dans le fichier"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
