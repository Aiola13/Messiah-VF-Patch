"""
Onglet d'installation du patch
"""

import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

from .base_tab import BaseTab
from ..config import COLORS


class InstallationTab(BaseTab):
    """Onglet pour l'installation du patch"""
    
    def __init__(self, parent_tabview, app_instance):
        self.app = app_instance
        super().__init__(parent_tabview, "🚀 Installation")
    
    def setup_tab(self):
        """Configure le contenu de l'onglet d'installation"""
        # Section de sélection du chemin
        self._create_path_section()
        
        # Barre de progression
        self._create_progress_section()
        
        # Boutons d'action
        self._create_action_buttons()
    
    def _create_path_section(self):
        """Création de la section de sélection du chemin"""
        path_frame = self.create_frame(self.tab)
        path_frame.pack(fill="x", pady=(10, 15), padx=10)
        
        path_title = self.create_title_label(
            path_frame,
            "📁 Dossier d'installation de Messiah"
        )
        path_title.pack(fill="x", padx=20, pady=(15, 10))
        
        # Frame pour le chemin et le bouton
        path_input_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Champ de texte pour afficher le chemin
        self.path_entry = ctk.CTkEntry(
            path_input_frame,
            placeholder_text="Aucun dossier sélectionné...",
            font=ctk.CTkFont(size=12),
            state="readonly"
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bouton de sélection
        self.browse_button = self.create_button(
            path_input_frame,
            text="📂 Parcourir",
            command=self._select_installation_path,
            width=120,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.browse_button.pack(side="right")
    
    def _create_progress_section(self):
        """Création de la section de progression"""
        self.progress_frame = self.create_frame(self.tab)
        
        progress_title = self.create_title_label(
            self.progress_frame,
            "📊 Progression de l'installation"
        )
        progress_title.pack(fill="x", padx=20, pady=(15, 10))
        
        # Barre de progression
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=25,
            corner_radius=12
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Label de statut
        self.status_label = ctk.CTkLabel(
            self.progress_frame,
            text="Prêt à installer",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(padx=20, pady=(0, 15))
    
    def _create_action_buttons(self):
        """Création des boutons d'action"""
        button_frame = ctk.CTkFrame(self.tab, fg_color="transparent")
        button_frame.pack(fill="x", pady=(15, 10), padx=10)
        
        # Bouton d'installation
        self.install_button = self.create_button(
            button_frame,
            text="🚀 Installer le Patch",
            command=self._start_installation,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover']
        )
        self.install_button.pack(fill="x", pady=(0, 10))
        
        # Frame pour les boutons secondaires
        secondary_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        secondary_buttons.pack(fill="x")
        
        # Bouton de fermeture
        self.close_button = self.create_button(
            secondary_buttons,
            text="❌ Fermer",
            command=self.app.quit,
            width=120,
            fg_color=COLORS['gray'],
            hover_color=COLORS['dark_gray']
        )
        self.close_button.pack(side="right")
    
    def _select_installation_path(self):
        """Sélection du dossier d'installation"""
        if self.app.patch_installer.get_installation_status():
            return
        
        folder_path = filedialog.askdirectory(
            title="Sélectionnez le dossier d'installation de Messiah"
        )
        
        if folder_path:
            self.app.destination_path = folder_path
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder_path)
            self.path_entry.configure(state="readonly")
            
            self.install_button.configure(state="normal")
            self.app.backup_tab.update_backup_status()
            self.app.logger.info(f"Dossier sélectionné: {folder_path}")
        else:
            self.app.logger.info("Sélection de dossier annulée")
    
    def _start_installation(self):
        """Démarrage de l'installation"""
        if not self.app.destination_path:
            CTkMessagebox(
                title="Erreur",
                message="Veuillez d'abord sélectionner un dossier d'installation.",
                icon="warning"
            )
            return
        
        if self.app.patch_installer.get_installation_status():
            return
        
        # Vérification de l'existence du dossier source
        if not self.app.patch_installer.validate_source_folder():
            CTkMessagebox(
                title="Erreur",
                message="Les fichiers du patch sont introuvables.\nVérifiez l'intégrité de l'installation.",
                icon="cancel"
            )
            return
        
        # Création de la sauvegarde avant installation
        self.progress_frame.pack(fill="x", pady=(0, 20))
        self.status_label.configure(text="Création de la sauvegarde...")
        self.progress_bar.set(0.1)
        
        if not self.app.backup_manager.create_backup(self.app.destination_path):
            CTkMessagebox(
                title="Erreur",
                message="Impossible de créer la sauvegarde des fichiers originaux.\nInstallation annulée.",
                icon="cancel"
            )
            self.progress_frame.pack_forget()
            return
        
        # Configuration des callbacks
        self.app.patch_installer.set_callbacks(
            progress_callback=self._update_progress,
            completion_callback=self._installation_complete,
            error_callback=self._installation_error
        )
        
        # Démarrage de l'installation
        self.app._update_ui_state(installing=True)
        self.app.patch_installer.start_installation(self.app.destination_path)
    
    def _update_progress(self, progress: float, copied_files: int, total_files: int):
        """Met à jour la barre de progression"""
        self.app.after(0, self._update_progress_ui, progress, copied_files, total_files)
    
    def _update_progress_ui(self, progress: float, copied_files: int, total_files: int):
        """Met à jour l'interface de progression"""
        self.progress_bar.set(progress)
        self.status_label.configure(
            text=f"Installation en cours... ({copied_files}/{total_files} fichiers)"
        )
    
    def _installation_complete(self):
        """Traite la fin de l'installation"""
        self.app.after(0, self._installation_complete_ui)
    
    def _installation_complete_ui(self):
        """Met à jour l'interface après installation"""
        self.app._update_ui_state(installing=False)
        
        self.progress_bar.set(1.0)
        self.status_label.configure(
            text="✅ Installation terminée avec succès !",
            text_color=COLORS['success']
        )
        
        # Mise à jour du statut des sauvegardes
        self.app.backup_tab.update_backup_status()
        self.app.status_indicator.configure(text="✅ Patch installé", text_color=COLORS['success'])
        
        # Message de confirmation
        from ..config import MESSAGES
        msg = CTkMessagebox(
            title="Installation Réussie",
            message=MESSAGES['installation_success'].format(path=self.app.destination_path),
            icon="check",
            option_1="Parfait !"
        )
        
        if msg.get() == "Parfait !":
            self.app.quit()
    
    def _installation_error(self, error_message: str):
        """Traite les erreurs d'installation"""
        self.app.after(0, self._installation_error_ui, error_message)
    
    def _installation_error_ui(self, error_message: str):
        """Met à jour l'interface en cas d'erreur"""
        self.app._update_ui_state(installing=False)
        
        self.progress_bar.set(0)
        self.status_label.configure(
            text="❌ Erreur lors de l'installation",
            text_color=COLORS['error']
        )
        
        CTkMessagebox(
            title="Erreur d'Installation",
            message=f"Une erreur est survenue lors de l'installation :\n\n{error_message}",
            icon="cancel"
        )