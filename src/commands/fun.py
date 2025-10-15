"""
Commandes fun et divertissantes du bot
"""

import discord
from discord.ext import commands
from discord import app_commands
import random
import os
import time
from pathlib import Path

class Fun(commands.Cog):
    """Commandes fun et divertissantes"""
    
    def __init__(self, bot):
        self.bot = bot
        self.img_folder = Path(__file__).parent.parent / "img"
        self.last_image = None
    
    def get_random_image(self):
        """Récupère une image aléatoire du dossier img (différente de la précédente)"""
        if not self.img_folder.exists():
            return None
        
        images = [f for f in self.img_folder.iterdir() if f.is_file() and f.suffix in ['.png', '.jpg', '.jpeg', '.gif']]
        
        if not images:
            return None
        
        if len(images) == 1:
            return images[0]
        
        if self.last_image and self.last_image in images:
            images.remove(self.last_image)
        
        random.seed(time.time_ns())
        random.shuffle(images)
        
        selected_image = images[0]
        self.last_image = selected_image
        
        return selected_image
    
    def get_random_story(self):
        """Retourne une histoire aléatoire sur l'incident du caillou"""
        stories = [
            "Le voisin du Y décide de tondre sa pelouse. VROOOOOM ! 🚜💨 Le tracteur démarre comme un avion !\n\nSoudain, SHLACK ! Un caillou ÉNORME est propulsé vers la baie vitrée ! Le temps ralentit... CRASH ! 💥\n\nLe Y sursaute tellement qu'il renverse son café ! Son cœur bat à 200 BPM ! Le tracteur rugit + le caillou géant = combo de la mort ! 😱 Il a vécu la peur de sa vie, crois-moi !",
            
            "ALERTE ROUGE ! 🚨 Le voisin du Y monte sur son tracteur-tondeuse. Pas n'importe lequel... LE GROS ! Celui qui fait trembler tout ! 🚜💪\n\nLa machine heurte un caillou PRÉHISTORIQUE ! Un ROCHER de ouf ! 🪨 Il est éjecté avec la force de mille catapultes ! WHOOOOSH !\n\nBAM ! Direction : la vitre du Y ! 💥 Le Y scrollait tranquille sur son tel, il fait un bond de 3 mètres ! Son âme quitte son corps ! 😱💀 Depuis, Le Y vérifie la météo des cailloux ! ☄️",
            
            "Le voisin du Y et son tracteur-tondeuse... Ce monstre qui aurait fait pâlir un T-Rex ! 🦖🚜\n\nDans la pelouse se cachait LE caillou LÉGENDAIRE ! Celui dont on parle dans les légendes ! 🪨✨\n\nBOOOOM ! Le caillou jaillit comme un obus ! Trajectoire parfaite vers la vitre du Y ! 🎯 CRAAAASH ! 💥\n\nLe Y bondit du canapé comme un ressort ! Son cœur explose ! Il perd 10 ans de vie ! 😱💔 Aujourd'hui, Le Y souffre de PTSD (Post-Tracteur Stress Disorder) ! 😂",
            
            "FLASH INFO ! 📰 Le voisin du Y sur son tracteur-tondeuse... Un TANK agricole de ouf ! 🚜🔥\n\nLa bête rencontre LE CAILLOU DU DESTIN ! Un TITAN de pierre ! 🗿 Le choc est terrible !\n\nLe caillou file à vitesse supersonique ! SWOOOOSH ! Comme une fusée SpaceX ! Direction : la vitre du Y ! BOOOOOM ! 💥\n\nLe Y fait le plus grand saut de sa vie ! Le tracteur rugit ! C'est L'ENFER ! 😱🌍 Le Y croit que c'est la fin du monde ! Le voisin continue tranquille comme si de rien... 😎🚜",
            
            "🎬 SCÈNE D'ACTION ! Le voisin du Y dans sa tondeuse TURBO ULTRA MAX 5000 ! Genre Fast & Furious ! VRRROOOOM ! 🚜💨\n\nCONTACT ! Un caillou taille BALLON DE BASKET éjecté ! Trajectoire PARFAITE ! 📐🪨 KABOOOOOM ! 💥 La vitre explose comme dans Matrix !\n\nLe Y fait un backflip involontaire ! Son âme fait le tour de la pièce ! Il hurle tellement fort que les voisins croient à une invasion alien ! 👽😱 Résultat : Le Y a peur des pelouses maintenant ! 🌱😰",
            
            "⚠️ BREAKING NEWS ! 📡 Le voisin du Y sur son tracteur NUCLÉAIRE ! Il siffle tranquille 🎵🚜\n\nMais dans l'herbe : un caillou ANCESTRAL de 4 milliards d'années ! Celui qui a vu les DINOSAURES ! 🦕🪨\n\nLe tracteur le percute ! CHAOS ! Le caillou file à Mach 5 ! La NASA le détecte ! L'armée s'affole ! 🚨 BOUM ! Dans la vitre du Y ! Les sismographes l'enregistrent ! 💥\n\nLe Y fait un salto arrière ! Son cri brise trois verres ! Le tracteur rugit comme Godzilla ! Le Y se cache sous la table en tremblant ! 😱🙈 Incident APOCALYPTIQUE ! 🌋",
            
            "🎪 CIRQUE DU VOISIN FOU ! Le voisin du Y sur son tracteur CUSTOMISÉ avec des flammes ! 🚜🔥\n\nIl fonce à fond ! Les roues dérapent ! TCHAK ! Un caillou de 5 kilos dans les lames ! GRRRRUUUUUNK ! 🤖💀\n\nLe caillou spin 360° comme un shuriken ninja ! WHOOOOSH ! 🥷🪨 STRIKE PARFAIT ! 💥 La vitre explose !\n\nLe Y saute jusqu'au plafond ! Cœur à 300 BPM ! 💓 Le tracteur rugit comme un dragon ! Le Y appelle sa mère en pleurant ! 😭📞 Score : Tracteur 1 - Le Y 0 ! 🏆",
            
            "🌪️ OURAGAN DE CAILLOUX ! Le voisin du Y avait bu 3 Red Bull. GRAVE ERREUR ! 🤠🚜\n\nLe tracteur devient un RÉACTEUR D'AVION ! Les oiseaux partent en Espagne ! 🐦✈️ Il crée un MINI CYCLONE d'herbe ! 🌪️\n\nKRACK ! Caillou LÉGENDAIRE percuté ! ⚡🪨 Il fait un looping, un tonneau ! JO du lancer de caillou ! 🤸‍♂️\n\nBAM dans la vitre du Y ! KAAAAABOOOOOM ! 💣💥 Le Y : TRAUMATISÉ ! Double-backflip ! Son âme part en vacances ! 😱 Depuis, Le Y porte des protections auditives 24/7 ! 🛡️👂",
            
            "🎮 MISSION IMPOSSIBLE ! Agent : Le Voisin. Objectif : Tondre. État : FAILED ❌\n\nLe voisin du Y aux commandes ! Tracteur militaire ! 🚜⚔️ Opération 'Herbe Rasée' lancée !\n\n14h38 : Caillou HOSTILE détecté ! 🪨⚠️ IMPACT ! 200 km/h ! SONIC BOOM ! 💨💥\n\nLa vitre du Y : DÉTRUITE ! Le Y en mode PANIQUE ! Il court partout ! Alarme de sous-marin ! BWOOOOP ! 🚨\n\n**RÉSULTAT :** Pelouse ✅ Vitre ❌ Le Y traumatisé ✅✅✅ 💣",
            
            "🏴‍☠️ LÉGENDE DU CAILLOU MAUDIT ! Il y a 1000 ans, les druides placèrent un caillou MAUDIT ! 🪨👻\n\nLe voisin du Y démarre son tracteur INFERNAL ! Les ancêtres crient : 'NOOOON !' Trop tard ! ⚰️🚜\n\nLe caillou VIBRE d'énergie maléfique ! CONTACT ! ⚡💥 Il explose de rage ! Éclairs partout ! 'VENGEAAANCE !' 👹\n\nLa vitre du Y : PULVÉRISÉE ! Ciel rouge ! Corbeaux ! 🦅🔥 Le Y voit l'au-delà ! Ses ancêtres : 'Fuis le tracteur !' 👻 Il tremble, transpire, pleure ! 😱💦 Le voisin est BANNI de tondre ! 🚫",
            
            "🎪 GRAND SPECTACLE ! � Le voisin du Y : acrobate principal ! Tracteur TURBO ! (La foule = 3 pigeons) 🚜🕊️\n\nNuméro 1 : Démarrage SPECTACULAIRE !  Numéro 2 : Tonte EXTRÊME genre F1 ! 🏎️\n\nNuméro 3 : Caillou CHAMPION DU MONDE percuté ! 🏅🪨 Numéro 4 : VOL HISTORIQUE ! Triple salto ! 10/10 ! 🤸‍♂️⭐\n\nFINALE ! Le caillou percute la vitre du Y ! BOOOOOM ! 💥 Le Y saute, applaudit de terreur, crie 'BRAVO' de peur ! 👏😰\n\nRésultat : 5 étoiles ⭐ Le Y ne l'oubliera JAMAIS ! (Il est traumatisé) 🎭💀",
            
            "🔬 RAPPORT SCIENTIFIQUE ! Expérience n°666 : Le Projet Caillou 🚜\n\nSujet : Voisin du Y. Tracteur DESTROYER 3000. Niveau sonore : 120 décibels ! 🎸\n\nCONTACT avec 'Caillou Prime' ! Âge : Jurassique ! 🦖🪨 RÉACTION EN CHAÎNE ! 9000 Newtons ! ⚡\n\nLancement à 180 km/h ! Angle 45° parfait ! 📐 IMPACT sur la vitre du Y ! 15 000 Newtons ! 💥\n\n**Résultats sur Le Y :** Saut : 30 cm. Cœur : +300%. Stress : MAX. Cri : 110 dB. Panique ✅ Trauma ✅ Thérapie ✅\n\n**Conclusion :** NE JAMAIS laisser le voisin tondre ! ⚠️☢️",
            
            "🎬 LE Y VS LE CAILLOU ! ULTIMATE SHOWDOWN ! 🥊\n\nCoin gauche : LE Y, 75 kg, paisible, innocent ! 😇 Coin droit : CAILLOU, 2 kg de DESTRUCTION, 500 chevaux ! 😈🪨\n\nLE COMBAT COMMENCE ! VROOOM ! DING DING ! 🔔 Le caillou : NINJA de pierre ! 🥷\n\n3... 2... 1... CONTACT ! ⚡ Coup spécial 'VOL SUPERSONIQUE' ! CRITICAL HIT ! 🎯 BOOOOOM ! K.O. TECHNIQUE ! 💥\n\nLe Y fait une roulade ! Cœur explosé de peur ! DÉFAITE TOTALE ! 😱\n\n**RÉSULTAT :** Caillou : VICTOIRE 🏆 Le Y : K.O., traumatisé 💀 Le Y veut une REVANCHE en vitres TITANE ! 🛡️"
        ]
        
        return random.choice(stories)
    
    @commands.command(name="caillou", aliases=["pierre", "rock"])
    @commands.has_permissions(administrator=True)
    async def caillou(self, ctx):
        """Raconte l'histoire épique du caillou du voisin du Y"""
        image_path = self.get_random_image()
        
        if not image_path:
            await ctx.send("❌ Aucune image de caillou disponible ! 😢")
            return
        
        embed = discord.Embed(
            title="🪨 L'INCIDENT DU CAILLOU VOLANT 🚜",
            description=self.get_random_story(),
            color=discord.Color.from_rgb(139, 69, 19)
        )
        
        embed.add_field(
            name="⚠️ Niveau de danger",
            value="🔴🔴🔴🔴🔴 EXTRÊME",
            inline=True
        )
        embed.add_field(
            name="😱 Peur du Y",
            value="999/10",
            inline=True
        )
        embed.add_field(
            name="🚜 Puissance du tracteur",
            value="OVER 9000 !",
            inline=True
        )
        
        embed.set_footer(text="Histoire véridique | Les caillous sont dangereux")
        embed.timestamp = discord.utils.utcnow()
        
        file = discord.File(image_path, filename=image_path.name)
        embed.set_image(url=f"attachment://{image_path.name}")
        
        await ctx.send(file=file, embed=embed)

    @app_commands.command(name="caillou", description="Raconte l'histoire épique du caillou du voisin du Y")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_caillou(self, interaction: discord.Interaction):
        """Raconte l'histoire épique du caillou du voisin du Y (slash command)"""
        image_path = self.get_random_image()
        
        if not image_path:
            await interaction.response.send_message("❌ Aucune image de caillou disponible ! 😢")
            return
        
        embed = discord.Embed(
            title="🪨 L'INCIDENT DU CAILLOU VOLANT 🚜",
            description=self.get_random_story(),
            color=discord.Color.from_rgb(139, 69, 19)
        )
        
        embed.add_field(
            name="⚠️ Niveau de danger",
            value="🔴🔴🔴🔴🔴 EXTRÊME",
            inline=True
        )
        embed.add_field(
            name="😱 Peur du Y",
            value="999/10",
            inline=True
        )
        embed.add_field(
            name="🚜 Puissance du tracteur",
            value="OVER 9000 !",
            inline=True
        )
        
        embed.set_footer(text="Histoire véridique | Les caillous sont dangereux")
        embed.timestamp = discord.utils.utcnow()
        
        file = discord.File(image_path, filename=image_path.name)
        embed.set_image(url=f"attachment://{image_path.name}")
        
        await interaction.response.send_message(file=file, embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
