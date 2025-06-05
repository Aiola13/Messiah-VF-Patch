"""
Application principale Messiah Patch VF
"""

import sys
import logging
import customtkinter as ctk

from .config import APP_CONFIG, COLORS, get_resource_path
from .backup_manager import BackupManager
from .patch_installer import PatchInstaller
from .ui import InstallationTab, BackupTab, InfoTab


class MessiahPatchApp(ctk.CTk):
    """Application principale de patch français pour Messiah"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration de l'application
        self._setup_app()
        self._setup_logging()
        
        # Variables d'état
        self.destination_path = None
        
        # Gestionnaires
        self.backup_manager = BackupManager()
        self.patch_installer = PatchInstaller()
        
        # Interface utilisateur
        self._create_ui()
    
    def _setup_app(self):
        """Configuration de base de l'application"""
        self.title(APP_CONFIG['title'])
        self.geometry(APP_CONFIG['geometry'])
        self.resizable(APP_CONFIG['resizable'], APP_CONFIG['resizable'])
        self.minsize(APP_CONFIG['min_width'], APP_CONFIG['min_height'])
        
        # Configuration du thème
        ctk.set_appearance_mode(APP_CONFIG['theme_mode'])
        ctk.set_default_color_theme(APP_CONFIG['color_theme'])
        
        # Icône (avec gestion d'erreur)
        try:
            self.iconbitmap(get_resource_path("resources/icons/messiah.ico"))
        except Exception as e:
            logging.warning(f"Impossible de charger l'icône: {e}")
    
    def _setup_logging(self):
        """Configuration du système de logs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _create_ui(self):
        """Création de l'interface utilisateur"""
        # Conteneur principal avec padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête
        self._create_header(main_container)
        
        # Système d'onglets
        self._create_tabview(main_container)
    
    def _create_header(self, parent):
        """Création de l'en-tête
        
        :param parent: the parent widget
        :return: returns nothing
        """
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Titre principal
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎮 Messiah Patch Français",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=COLORS['primary']
        )
        title_label.pack()
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Traduction française complète avec sauvegarde automatique",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Indicateur de statut
        self.status_indicator = ctk.CTkLabel(
            header_frame,
            text="🔵 Prêt",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['success']
        )
        self.status_indicator.pack(pady=(5, 0))
    
    def _create_tabview(self, parent):
        """Création du système d'onglets
        
        :param parent: the parent widget
        :return: returns nothing
        """
        self.tabview = ctk.CTkTabview(parent, width=600, height=400)
        self.tabview.pack(fill="both", expand=True, pady=(0, 15))
        
        # Création des onglets
        self.tabview.add("🚀 Installation")
        self.tabview.add("💾 Sauvegarde")
        self.tabview.add("📋 Informations")
        
        # Initialisation des onglets
        self.installation_tab = InstallationTab(self.tabview, self)
        self.backup_tab = BackupTab(self.tabview, self)
        self.info_tab = InfoTab(self.tabview, self)
        
        # Sélectionner l'onglet installation par défaut
        self.tabview.set("🚀 Installation")
    
    def _update_ui_state(self, installing=False):
        """Met à jour l'état de l'interface utilisateur
        
        :param installing: bool, True si l'installation est en cours
        :return: returns nothing
        """
        if installing:
            self.installation_tab.install_button.configure(
                text="⏳ Installation en cours...",
                state="disabled"
            )
            self.installation_tab.browse_button.configure(state="disabled")
            self.installation_tab.close_button.configure(state="disabled")
            self.status_indicator.configure(text="🟡 Installation...", text_color="orange")
        else:
            self.installation_tab.install_button.configure(
                text="🚀 Installer le Patch",
                state="normal"
            )
            self.installation_tab.browse_button.configure(state="normal")
            self.installation_tab.close_button.configure(state="normal")
            self.status_indicator.configure(text="🔵 Prêt", text_color=COLORS['success'])


def main():
    """Point d'entrée principal de l'application"""
    try:
        app = MessiahPatchApp()
        app.mainloop()
    except Exception as e:
        print(f"Erreur fatale: {e}")
        logging.error(f"Erreur fatale: {e}")


if __name__ == "__main__":
    main()