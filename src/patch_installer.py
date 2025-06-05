"""
Gestionnaire d'installation des patches
"""

import shutil
import threading
import logging
from pathlib import Path
from typing import Callable, Optional

from .config import FILE_MAPPING, get_source_folder


class PatchInstaller:
    """Gestionnaire d'installation des patches"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_installing = False
        self.progress_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None
    
    def set_callbacks(self, 
                     progress_callback: Optional[Callable] = None,
                     completion_callback: Optional[Callable] = None,
                     error_callback: Optional[Callable] = None):
        """Configure les callbacks pour les événements d'installation
        
        :param progress_callback: Fonction appelée pour mettre à jour la progression
        :param completion_callback: Fonction appelée à la fin de l'installation
        :param error_callback: Fonction appelée en cas d'erreur
        """
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self.error_callback = error_callback
    
    def validate_source_folder(self) -> bool:
        """Vérifie que le dossier source existe
        
        :return: True si le dossier source existe, False sinon"""
        source_folder = get_source_folder()
        return source_folder.exists()
    
    def start_installation(self, destination_path: str) -> bool:
        """Démarre l'installation dans un thread séparé
        
        :param destination_path: Chemin de destination pour l'installation
        :return: True si l'installation a démarré, False si déjà en cours ou en cas d'erreur
        """
        if self.is_installing:
            return False
        
        if not self.validate_source_folder():
            return False
        
        self.is_installing = True
        
        # Lancement du thread d'installation
        install_thread = threading.Thread(
            target=self._perform_installation,
            args=(destination_path,),
            daemon=True
        )
        install_thread.start()
        return True
    
    def _perform_installation(self, destination_path: str):
        """Effectue l'installation dans un thread séparé
        
        :param destination_path: Chemin de destination pour l'installation
        """
        try:
            source_folder = get_source_folder()
            destination_folder = Path(destination_path)
            
            # Calcul du nombre total de fichiers
            all_files = list(source_folder.rglob('*'))
            total_files = len([f for f in all_files if f.is_file()])
            
            if total_files == 0:
                raise Exception("Aucun fichier à copier trouvé")
            
            copied_files = 0
            
            # Copie des fichiers
            for file_path in all_files:
                if not file_path.is_file():
                    continue
                
                # Calcul du chemin de destination
                relative_path = file_path.relative_to(source_folder)
                dest_path = destination_folder / relative_path
                
                # Gestion des fichiers spéciaux (renommage)
                if file_path.name in FILE_MAPPING:
                    new_name = FILE_MAPPING[file_path.name]
                    dest_path = dest_path.parent / new_name
                
                # Création du dossier de destination si nécessaire
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copie du fichier
                shutil.copy2(file_path, dest_path)
                copied_files += 1
                
                # Mise à jour de la progression
                if self.progress_callback:
                    progress = copied_files / total_files
                    self.progress_callback(progress, copied_files, total_files)
            
            # Installation terminée
            self.is_installing = False
            if self.completion_callback:
                self.completion_callback()
            
        except Exception as e:
            self.is_installing = False
            self.logger.error(f"Erreur lors de l'installation: {e}")
            if self.error_callback:
                self.error_callback(str(e))
    
    def stop_installation(self):
        """Arrête l'installation (si possible)"""
        self.is_installing = False
    
    def get_installation_status(self) -> bool:
        """Retourne le statut de l'installation
        
        :return: True si l'installation est en cours, False sinon"""
        return self.is_installing