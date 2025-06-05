"""
Onglet d'informations sur le patch
"""

import customtkinter as ctk

from .base_tab import BaseTab
from ..config import MESSAGES


class InfoTab(BaseTab):
    """Onglet pour les informations sur le patch"""
    
    def __init__(self, parent_tabview, app_instance):
        self.app = app_instance
        super().__init__(parent_tabview, "📋 Informations")
    
    def setup_tab(self):
        """Configure le contenu de l'onglet d'informations"""
        # Section d'information principale
        info_frame = self.create_frame(self.tab)
        info_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        info_title = self.create_title_label(
            info_frame,
            "📋 À propos de ce patch"
        )
        info_title.pack(fill="x", padx=20, pady=(15, 10))
        
        info_text = ctk.CTkLabel(
            info_frame,
            text=MESSAGES['info_text'],
            font=ctk.CTkFont(size=13),
            justify="left",
            anchor="nw"
        )
        info_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))