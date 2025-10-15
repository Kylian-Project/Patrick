"""
Module CROUS pour récupérer et afficher les menus du restaurant universitaire de Illkirch
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import asyncio
from datetime import datetime, timedelta, time
import logging

class Crous(commands.Cog):
    """Commandes pour récupérer les menus CROUS"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configuration CROUS
        self.restaurant_id = 1392
        self.api_url = f"https://api.croustillant.menu/v1/restaurants/{self.restaurant_id}/menu"
        self.channel_id = 1422877808681554000
        
        # Démarrer la tâche automatique
        self.daily_menu_task.start()
    
    def cog_unload(self):
        """Arrêter les tâches quand le cog est déchargé"""
        self.daily_menu_task.cancel()
    
    async def fetch_menu_data(self):
        """Récupère les données du menu depuis l'API CROUS"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        self.logger.error(f"Erreur API CROUS: {response.status}")
                        return None
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération du menu CROUS: {e}")
            return None
    
    def format_menu_embed(self, menu_data, date_filter=None):
        """Formate les données du menu en embed Discord"""
        if not menu_data or not menu_data.get('success'):
            return None
        
        # Filtrer par date si spécifiée
        menu_items = menu_data.get('data', [])
        if date_filter:
            menu_items = [item for item in menu_items if item.get('date') == date_filter]
        
        if not menu_items:
            return None
        
        # Prendre le premier menu (aujourd'hui ou date spécifiée)
        today_menu = menu_items[0]
        date = today_menu.get('date', 'Date inconnue')
        
        embed = discord.Embed(
            title="🍽️ Menu CROUS",
            description=f"📅 **{date}**",
            color=0xff6b35,
            timestamp=datetime.now()
        )
        
        # Parcourir les repas (généralement midi)
        for repas in today_menu.get('repas', []):
            repas_type = repas.get('type', 'Repas').capitalize()
            
            # Grouper les catégories importantes
            categories_importantes = []
            cafeteria = None
            
            for categorie in repas.get('categories', []):
                libelle = categorie.get('libelle', '')
                
                # Filtrer les catégories importantes (tout ce qui concerne les étudiants)
                if 'etudiants' in libelle.lower() and 'personnel' not in libelle.lower():
                    categories_importantes.append(categorie)
                elif 'cafeteria' in libelle.lower() and 'personnel' not in libelle.lower():
                    cafeteria = categorie
            
            # Fonction pour déterminer l'ordre d'affichage
            def get_order(categorie):
                libelle = categorie.get('libelle', '').lower()
                if 'entrees' in libelle or 'entrées' in libelle:
                    return 1
                elif 'barbecue' in libelle:
                    return 2
                elif 'plat du jour' in libelle:
                    # Inverser l'ordre des plats du jour (1 avant 2)
                    if 'plat du jour 1' in libelle:
                        return 3
                    elif 'plat du jour 2' in libelle:
                        return 4
                    return 3
                elif 'pates' in libelle or 'pâtes' in libelle:
                    return 5
                elif 'desserts' in libelle:
                    return 6
                else:
                    return 99
            
            # Trier les catégories dans l'ordre logique
            categories_importantes.sort(key=get_order)
            
            embed.add_field(name="─" * 30, value="", inline=False)
            
            # Afficher les catégories importantes
            for categorie in categories_importantes:
                libelle = categorie.get('libelle', 'Catégorie')
                plats = categorie.get('plats', [])
                
                if plats:
                    plats_text = []
                    for plat in plats:
                        plats_text.append(f"• {plat.get('libelle', 'Plat inconnu')}")
                        
                    # Raccourcir le nom de la catégorie pour éviter les limites Discord
                    short_libelle = libelle.replace('Salle des ', '').replace(' - ', ' | ')
                    if len(short_libelle) > 40:
                        short_libelle = short_libelle[:37] + "..."
                    
                    embed.add_field(
                        name=f"📋 {short_libelle.capitalize()}",
                        value='\n'.join(plats_text)[:1024],  # Limite Discord de 1024 caractères
                        inline=False
                    )
                    embed.add_field(name="─" * 30, value="", inline=False)
            
            # Afficher la cafeteria en dernier
            if cafeteria:
                plats = cafeteria.get('plats', [])
                if plats:
                    plats_text = []
                    for plat in plats:
                        plats_text.append(f"• {plat.get('libelle', 'Plat inconnu')}")
                    
                    embed.add_field(
                        name="📋 Cafeteria",
                        value='\n'.join(plats_text)[:1024],
                        inline=False
                    )
                    embed.add_field(name="─" * 30, value="", inline=False)
        
        embed.set_footer(text="🏫 Restaurant Universitaire | Données via API Croustillant")
        
        return embed
    
    @commands.command(name="menu", aliases=["crous"])
    async def menu_command(self, ctx, *, date=None):
        """Affiche le menu CROUS (optionnel: spécifier une date au format JJ-MM-AAAA)"""
        async with ctx.typing():
            menu_data = await self.fetch_menu_data()
            
            if not menu_data:
                embed = discord.Embed(
                    title="❌ Erreur",
                    description="Impossible de récupérer le menu CROUS.",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
                return
            
            # Formater la date si fournie
            date_filter = None
            if date:
                try:
                    # Essayer de parser la date
                    if len(date.split('-')) == 3:
                        date_filter = date
                    else:
                        await ctx.send("❌ Format de date invalide. Utilisez: JJ-MM-AAAA (ex: 01-10-2025)")
                        return
                except:
                    await ctx.send("❌ Format de date invalide. Utilisez: JJ-MM-AAAA (ex: 01-10-2025)")
                    return
            
            embed = self.format_menu_embed(menu_data, date_filter)
            
            if embed:
                await ctx.send(embed=embed)
            else:
                no_menu_embed = discord.Embed(
                    title="📅 Pas de menu",
                    description=f"Aucun menu trouvé pour la date {'demandée' if date_filter else 'du jour'}.",
                    color=0xffa500
                )
                await ctx.send(embed=no_menu_embed)
    
    @app_commands.command(name="menu", description="Affiche le menu CROUS du jour")
    @app_commands.describe(date="Date au format JJ-MM-AAAA (optionnel)")
    async def menu_slash(self, interaction: discord.Interaction, date: str = None):
        """Version slash command du menu CROUS"""
        await interaction.response.defer()
        
        menu_data = await self.fetch_menu_data()
        
        if not menu_data:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Impossible de récupérer le menu CROUS.",
                color=0xff0000
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Formater la date si fournie
        date_filter = None
        if date:
            try:
                if len(date.split('-')) == 3:
                    date_filter = date
                else:
                    await interaction.followup.send("❌ Format de date invalide. Utilisez: JJ-MM-AAAA (ex: 01-10-2025)")
                    return
            except:
                await interaction.followup.send("❌ Format de date invalide. Utilisez: JJ-MM-AAAA (ex: 01-10-2025)")
                return
        
        embed = self.format_menu_embed(menu_data, date_filter)
        
        if embed:
            await interaction.followup.send(embed=embed)
        else:
            no_menu_embed = discord.Embed(
                title="📅 Pas de menu",
                description=f"Aucun menu trouvé pour la date {'demandée' if date_filter else 'du jour'}.",
                color=0xffa500
            )
            await interaction.followup.send(embed=no_menu_embed)
    
    @commands.command(name="menu_semaine", aliases=["menus"])
    async def menu_week_command(self, ctx):
        """Affiche tous les menus de la semaine"""
        async with ctx.typing():
            menu_data = await self.fetch_menu_data()
            
            if not menu_data:
                embed = discord.Embed(
                    title="❌ Erreur",
                    description="Impossible de récupérer les menus CROUS.",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
                return
            
            menu_items = menu_data.get('data', [])
            
            if not menu_items:
                await ctx.send("📅 Aucun menu disponible.")
                return
            
            # Créer un embed avec la liste des dates disponibles
            embed = discord.Embed(
                title="📅 Menus CROUS disponibles",
                description="Voici les dates pour lesquelles des menus sont disponibles:",
                color=0xff6b35
            )
            
            dates_list = []
            for i, menu_item in enumerate(menu_items[:10]):  # Limiter à 10 dates
                date = menu_item.get('date', 'Date inconnue')
                dates_list.append(f"**{i+1}.** {date}")
            
            embed.add_field(
                name="🗓️ Dates disponibles",
                value='\n'.join(dates_list),
                inline=False
            )
            
            embed.add_field(
                name="💡 Comment utiliser",
                value="Utilisez `!menu JJ-MM-AAAA` pour voir un menu spécifique",
                inline=False
            )
            
            await ctx.send(embed=embed)
    
    @tasks.loop(time=time(hour=8, minute=0))
    async def daily_menu_task(self):
        """Tâche automatique pour poster le menu du jour à 8h00"""
        try:
            channel = self.bot.get_channel(self.channel_id)
            if not channel:
                self.logger.warning(f"Canal {self.channel_id} introuvable pour le menu automatique")
                return
            
            menu_data = await self.fetch_menu_data()
            if not menu_data:
                return
            
            embed = self.format_menu_embed(menu_data)
            if embed:
                embed.title = "🌅 Menu du jour - CROUS"
                await channel.send("🍽️ **Le menu du jour est arrivé !**", embed=embed)
                self.logger.info("Menu automatique posté avec succès")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'envoi automatique du menu: {e}")
    
    @daily_menu_task.before_loop
    async def before_daily_menu(self):
        """Attendre que le bot soit prêt avant de démarrer la tâche"""
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Crous(bot))
