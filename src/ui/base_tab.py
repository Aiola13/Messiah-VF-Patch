"""
Classe de base pour les onglets de l'interface utilisateur
"""

import customtkinter as ctk
from abc import ABC, abstractmethod


class BaseTab(ABC):
    """Classe de base pour tous les onglets"""
    
    def __init__(self, parent_tabview, tab_name: str):
        self.parent_tabview = parent_tabview
        self.tab_name = tab_name
        self.tab = parent_tabview.tab(tab_name)
        self.setup_tab()
    
    @abstractmethod
    def setup_tab(self):
        """Configure le contenu de l'onglet"""
        pass
    
    def create_frame(self, parent, **kwargs) -> ctk.CTkFrame:
        """Crée un frame avec des paramètres par défaut"""
        default_kwargs = {
            'corner_radius': 12,
            'fg_color': None
        }
        default_kwargs.update(kwargs)
        return ctk.CTkFrame(parent, **default_kwargs)
    
    def create_title_label(self, parent, text: str, **kwargs) -> ctk.CTkLabel:
        """Crée un label de titre avec un style cohérent"""
        default_kwargs = {
            'font': ctk.CTkFont(size=18, weight="bold"),
            'anchor': "w"
        }
        default_kwargs.update(kwargs)
        return ctk.CTkLabel(parent, text=text, **default_kwargs)
    
    def create_description_label(self, parent, text: str, **kwargs) -> ctk.CTkLabel:
        """Crée un label de description avec un style cohérent"""
        default_kwargs = {
            'font': ctk.CTkFont(size=13),
            'justify': "left",
            'anchor': "w"
        }
        default_kwargs.update(kwargs)
        return ctk.CTkLabel(parent, text=text, **default_kwargs)
    
    def create_button(self, parent, text: str, command=None, **kwargs) -> ctk.CTkButton:
        """Crée un bouton avec un style cohérent"""
        default_kwargs = {
            'font': ctk.CTkFont(size=14, weight="bold"),
            'height': 40
        }
        default_kwargs.update(kwargs)
        return ctk.CTkButton(parent, text=text, command=command, **default_kwargs)