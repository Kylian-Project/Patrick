# 🤖 Discord Bot Python

Un bot Discord moderne et modulaire développé en Python avec discord.py.

## 📋 Prérequis

- Python 3.8 ou plus récent

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone URL
cd Patrick
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. (Optionnel) Modifiez la configuration dans `config/config.json`

### 4. Lancer le bot
```bash
python main.py
```

## 📁 Structure du projet

```
discord-bot/
├── main.py                   # Point d'entrée principal
├── requirements.txt          # Dépendances Python
├── .gitignore                # Fichiers à ignorer par Git
├── README.md                 # Ce fichier
├── src/                      # Code source du bot
│   ├── __init__.py
│   ├── bot.py                # Classe principale du bot
│   ├── commands/             # Modules de commandes
│   │   ├── __init__.py
│   │   ├── moderation.py     # Commandes de modération
│   │   └── general.py        # Commandes générals
│   ├── events/               # Gestionnaires d'événements
│   │   ├── __init__.py
│   │   └── on_ready.py       # Événement bot prêt
│   └── utils/                # Utilitaires
│       ├── __init__.py
│       ├── config_loader.py  # Chargeur de configuration
│       └── logger.py         # Configuration des logs
├── config/                   # Fichiers de configuration
│   └── config.json           # Configuration principale
└── logs/                     # ichiers de logs
```

## ⚙️ Configuration

### Variables d'environnement (.env)
- `DISCORD_TOKEN` : Token de votre bot Discord (obligatoire)
- `OWNER_ID` : Votre ID Discord (optionnel)
- `ENVIRONMENT` : Environnement (development/production)
- `LOG_LEVEL` : Niveau de logging (DEBUG/INFO/WARNING/ERROR)

### Configuration JSON (config/config.json)
```json
{
  "default_prefix": "!",
  "status_message": "En développement | !help",
  "embed_color": 2067276,
  "log_level": "INFO",
  "features": {
    "moderation": true
  }
}
```

## 🎯 Fonctionnalités

### Commandes générales
- `!ping` - Teste la latence du bot
- `!info` - Informations sur le bot
- `!help` - Aide et liste des commandes

### Commandes de modération
- `!clear [nombre]` - Supprimer des messages

## 🔧 Développement

### Ajouter une nouvelle commande
1. Créez un nouveau fichier dans `src/commands/`
2. Utilisez le template suivant :

```python
import discord
from discord.ext import commands

class VotreCategorie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="votre_commande")
    async def votre_commande(self, ctx):
        await ctx.send("Votre réponse")

async def setup(bot):
    await bot.add_cog(VotreCategorie(bot))
```

3. Ajoutez le module dans `src/bot.py` dans la liste `cogs_to_load`

### Ajouter un événement
1. Créez un fichier dans `src/events/`
2. Utilisez le template d'événement Discord

### Logs
Les logs sont automatiquement sauvegardés dans le dossier `logs/` avec rotation quotidienne.

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Si vous avez des questions ou des problèmes :
- Ouvrez une issue sur GitHub
- Contactez-moi sur Discord

---
Fait avec ❤️ en Python
