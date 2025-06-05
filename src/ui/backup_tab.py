"""
Onglet de gestion des sauvegardes
"""

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from .base_tab import BaseTab
from ..config import COLORS, MESSAGES


class BackupTab(BaseTab):
    """Onglet pour la gestion des sauvegardes"""
    
    def __init__(self, parent_tabview, app_instance):
        """
        Initialise l'onglet de sauvegarde
        :param parent_tabview: Instance de l'onglet parent
        :param app_instance: Instance de l'application principale
        """
        self.app = app_instance
        super().__init__(parent_tabview, "💾 Sauvegarde")
    
    def setup_tab(self):
        """Configure le contenu de l'onglet de sauvegarde"""
        # Section d'information sur les sauvegardes
        self._create_backup_info_section()
        
        # Section de statut des sauvegardes
        self._create_backup_status_section()
        
        # Boutons de gestion des sauvegardes
        self._create_backup_buttons()
        
        # Mise à jour initiale du statut
        self.update_backup_status()
    
    def _create_backup_info_section(self):
        """Crée la section d'information sur les sauvegardes"""
        backup_info_frame = self.create_frame(self.tab)
        backup_info_frame.pack(fill="x", pady=(10, 15), padx=10)
        
        backup_title = self.create_title_label(
            backup_info_frame,
            "💾 Gestion des Sauvegardes"
        )
        backup_title.pack(fill="x", padx=20, pady=(15, 5))
        
        backup_desc = self.create_description_label(
            backup_info_frame,
            MESSAGES['backup_description']
        )
        backup_desc.pack(fill="x", padx=20, pady=(0, 15))
    
    def _create_backup_status_section(self):
        """Crée la section de statut des sauvegardes"""
        self.backup_status_frame = self.create_frame(self.tab)
        self.backup_status_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        status_title = self.create_title_label(
            self.backup_status_frame,
            "📊 Statut des Sauvegardes",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        status_title.pack(fill="x", padx=20, pady=(15, 10))
        
        self.backup_status_label = ctk.CTkLabel(
            self.backup_status_frame,
            text="Aucune sauvegarde trouvée",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        self.backup_status_label.pack(fill="x", padx=20, pady=(0, 15))
    
    def _create_backup_buttons(self):
        """Crée les boutons de gestion des sauvegardes"""
        backup_buttons_frame = ctk.CTkFrame(self.tab, fg_color="transparent")
        backup_buttons_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        self.restore_button = self.create_button(
            backup_buttons_frame,
            text="🔄 Restaurer les Fichiers Originaux",
            command=self._restore_backup,
            fg_color=COLORS['warning'],
            hover_color=COLORS['warning_hover'],
            state="disabled"
        )
        self.restore_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.delete_backup_button = self.create_button(
            backup_buttons_frame,
            text="🗑️ Supprimer la Sauvegarde",
            command=self._delete_backup,
            width=200,
            fg_color=COLORS['gray'],
            hover_color=COLORS['dark_gray'],
            state="disabled"
        )
        self.delete_backup_button.pack(side="right")
    
    def update_backup_status(self):
        """Met à jour le statut des sauvegardes"""
        if not self.app.destination_path:
            self.backup_status_label.configure(
                text="Sélectionnez d'abord un dossier d'installation",
                text_color="gray"
            )
            self.restore_button.configure(state="disabled")
            self.delete_backup_button.configure(state="disabled")
            return
        
        backup_info = self.app.backup_manager.get_backup_status(self.app.destination_path)
        
        if backup_info:
            backup_date = backup_info.get('date', 'Date inconnue')
            patch_applied = backup_info.get('patch_applied', False)
            
            status_text = f"✅ Sauvegarde disponible\nDate: {backup_date}\nStatut: {'Patch appliqué' if patch_applied else 'Fichiers originaux'}"
            
            self.backup_status_label.configure(
                text=status_text,
                text_color=COLORS['success']
            )
            self.restore_button.configure(state="normal" if patch_applied else "disabled")
            self.delete_backup_button.configure(state="normal")
        else:
            self.backup_status_label.configure(
                text="ℹ️ Aucune sauvegarde trouvée pour ce dossier",
                text_color="gray"
            )
            self.restore_button.configure(state="disabled")
            self.delete_backup_button.configure(state="disabled")
    
    def _restore_backup(self):
        """Restaure les fichiers originaux depuis la sauvegarde"""
        if not self.app.destination_path:
            CTkMessagebox(
                title="Erreur",
                message="Aucun dossier d'installation sélectionné.",
                icon="warning"
            )
            return
        
        if not self.app.backup_manager.backup_exists(self.app.destination_path):
            CTkMessagebox(
                title="Erreur",
                message="Aucune sauvegarde trouvée pour ce dossier.",
                icon="warning"
            )
            return
        
        # Confirmation
        msg = CTkMessagebox(
            title="Confirmation",
            message=MESSAGES['restore_confirmation'],
            icon="question",
            option_1="Oui, restaurer",
            option_2="Annuler"
        )
        
        if msg.get() != "Oui, restaurer":
            return
        
        # Restauration
        success, restored_files = self.app.backup_manager.restore_backup(self.app.destination_path)
        
        if success:
            self.update_backup_status()
            CTkMessagebox(
                title="Restauration Réussie",
                message=f"Les fichiers originaux ont été restaurés avec succès !\n"
                       f"{restored_files} fichiers restaurés.",
                icon="check"
            )
        else:
            CTkMessagebox(
                title="Erreur de Restauration",
                message="Une erreur est survenue lors de la restauration.",
                icon="cancel"
            )
    
    def _delete_backup(self):
        """Supprime la sauvegarde"""
        if not self.app.destination_path:
            return
        
        if not self.app.backup_manager.backup_exists(self.app.destination_path):
            CTkMessagebox(
                title="Erreur",
                message="Aucune sauvegarde trouvée.",
                icon="warning"
            )
            return
        
        # Confirmation
        msg = CTkMessagebox(
            title="Confirmation",
            message=MESSAGES['delete_backup_confirmation'],
            icon="warning",
            option_1="Oui, supprimer",
            option_2="Annuler"
        )
        
        if msg.get() != "Oui, supprimer":
            return
        
        # Suppression
        if self.app.backup_manager.delete_backup(self.app.destination_path):
            self.update_backup_status()
            CTkMessagebox(
                title="Suppression Réussie",
                message="La sauvegarde a été supprimée avec succès.",
                icon="check"
            )
        else:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur est survenue lors de la suppression.",
                icon="cancel"
            )