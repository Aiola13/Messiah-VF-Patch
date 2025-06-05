"""
Configuration et constantes de l'application
"""

import os
import sys
from pathlib import Path

# Configuration de l'application
APP_CONFIG = {
    'title': 'Messiah Patch VF - Version Améliorée',
    'geometry': '650x550',
    'min_width': 600,
    'min_height': 500,
    'resizable': False,
    'theme_mode': 'dark',
    'color_theme': 'blue'
}

# Couleurs personnalisées
COLORS = {
    'primary': ("#1f538d", "#4a9eff"),
    'primary_hover': ("#164270", "#3d8ce6"),
    'warning': ("#d4851a", "#ff9500"),
    'warning_hover': ("#b8741a", "#e6850a"),
    'success': "green",
    'error': "red",
    'gray': "gray",
    'dark_gray': "darkgray"
}

# Fichiers à sauvegarder lors de l'installation du patch
FILES_TO_BACKUP = [
    "Messiah.eng",
    "pc/sound/espeek.dta",
    "pc/sound/espeek.idx",
    "pc/sound/seffx.dta",
    "pc/sound/seffx.idx",
    # Fichiers d'interface
    "pc/interfce/Menu/new/ControlSetup.tga",
    "pc/interfce/Menu/new/EmptyMenu.tga",
    "pc/interfce/Menu/new/LoadGame.tga",
    "pc/interfce/Menu/new/LoadingScreen.tga",
    "pc/interfce/Menu/new/MDifficultyDisciple1.tga",
    "pc/interfce/Menu/new/MDifficultyMessiah3.tga",
    "pc/interfce/Menu/new/MDifficultySaint2.tga",
    "pc/interfce/Menu/new/MMainAreyouSure.tga",
    "pc/interfce/Menu/new/MMainExit4.tga",
    "pc/interfce/Menu/new/MMainIntro3.tga",
    "pc/interfce/Menu/new/MMainOptions2.tga",
    "pc/interfce/Menu/new/MMainPlayGame1.tga",
    "pc/interfce/Menu/new/MOptionsControlSetup1.tga",
    "pc/interfce/Menu/new/MOptionsSoundSettings3.tga",
    "pc/interfce/Menu/new/MOptionsVideoSettings2.tga",
    "pc/interfce/Menu/new/MStartLoadGame2.tga",
    "pc/interfce/Menu/new/MStartNewGame1.tga",
    "pc/interfce/Menu/new/SoundSettings.tga",
    "pc/interfce/Menu/new/VideoSettings.tga",
    "pc/intro/newintro/box01.tga",
    "pc/intro.mve",
    "pc/sacrifice.mve"
]

# Mapping des fichiers à renommer lors de l'installation
FILE_MAPPING = {
    "Messiah.fra": "Messiah.eng",
    "fspeek.dta": "espeek.dta",
    "fspeek.idx": "espeek.idx"
}

# Chemins
def get_resource_path(relative_path):
    """Obtient le chemin des ressources (compatible PyInstaller)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_source_folder():
    """Retourne le dossier source des fichiers du patch"""
    return Path(__file__).parent.parent / 'resources' / 'PatchFR'

# Messages de l'interface
MESSAGES = {
    'info_text': """🎯 Fonctionnalités du patch :
• Remplace tous les textes anglais par leur traduction française
• Inclut les voix françaises pour une immersion complète
• Installation automatique et sécurisée
• Compatible avec toutes les versions du jeu

🛡️ Sécurité :
• Sauvegarde automatique des fichiers originaux
• Possibilité de restauration complète
• Aucune modification irréversible

⚙️ Installation :
• Sélectionnez le dossier d'installation de Messiah
• Cliquez sur 'Installer le Patch'
• Les fichiers originaux sont automatiquement sauvegardés
• Profitez du jeu en français !""",
    
    'backup_description': """Les fichiers originaux sont automatiquement sauvegardés avant l'installation du patch.
Vous pouvez restaurer les fichiers originaux à tout moment.""",
    
    'installation_success': """Le patch français a été installé avec succès dans :
{path}

✅ Sauvegarde créée automatiquement
🔄 Vous pouvez restaurer les fichiers originaux depuis l'onglet Sauvegarde

Profitez maintenant de Messiah en français !""",
    
    'restore_confirmation': """Êtes-vous sûr de vouloir restaurer les fichiers originaux ?
Cette action remplacera tous les fichiers du patch français.""",
    
    'delete_backup_confirmation': """Êtes-vous sûr de vouloir supprimer définitivement la sauvegarde ?
Cette action est irréversible !"""
}