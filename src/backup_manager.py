"""
Gestionnaire de sauvegarde et restauration des fichiers
"""

import json
import datetime
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Optional

from .config import FILES_TO_BACKUP


class BackupManager:
    """Gestionnaire des sauvegardes de fichiers"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_backup_path(self, destination_path: str) -> Path:
        """Génère le chemin de sauvegarde"""
        backup_dir = Path(destination_path).parent / "Messiah_Backup"
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return backup_dir / f"backup_{timestamp}"
    
    def get_backup_info_path(self, destination_path: str) -> Path:
        """Génère le chemin du fichier d'information de sauvegarde"""
        backup_dir = Path(destination_path).parent / "Messiah_Backup"
        return backup_dir / "backup_info.json"
    
    def create_backup(self, destination_path: str) -> bool:
        """Crée une sauvegarde des fichiers originaux"""
        try:
            backup_path = self.get_backup_path(destination_path)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            backed_up_files = []
            destination = Path(destination_path)
            
            for file_rel_path in FILES_TO_BACKUP:
                source_file = destination / file_rel_path
                if source_file.exists():
                    backup_file = backup_path / file_rel_path
                    backup_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, backup_file)
                    backed_up_files.append(file_rel_path)
                    self.logger.info(f"Fichier sauvegardé: {file_rel_path}")
            
            # Sauvegarde des informations
            backup_info = {
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'backup_path': str(backup_path),
                'destination_path': str(destination_path),
                'files_backed_up': backed_up_files,
                'patch_applied': True
            }
            
            backup_info_path = self.get_backup_info_path(destination_path)
            backup_info_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(backup_info_path, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Sauvegarde créée: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création de la sauvegarde: {e}")
            return False
    
    def restore_backup(self, destination_path: str) -> tuple[bool, int]:
        """
        Restaure les fichiers originaux depuis la sauvegarde
        
        Returns:
            tuple: (success: bool, restored_files_count: int)
        """
        try:
            backup_info_path = self.get_backup_info_path(destination_path)
            
            if not backup_info_path.exists():
                return False, 0
            
            with open(backup_info_path, 'r', encoding='utf-8') as f:
                backup_info = json.load(f)
            
            backup_path = Path(backup_info['backup_path'])
            destination = Path(destination_path)
            
            if not backup_path.exists():
                return False, 0
            
            # Restauration des fichiers
            restored_files = 0
            for file_rel_path in backup_info['files_backed_up']:
                backup_file = backup_path / file_rel_path
                dest_file = destination / file_rel_path
                
                if backup_file.exists():
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, dest_file)
                    restored_files += 1
                    self.logger.info(f"Fichier restauré: {file_rel_path}")
            
            # Mise à jour du statut
            backup_info['patch_applied'] = False
            with open(backup_info_path, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            return True, restored_files
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la restauration: {e}")
            return False, 0
    
    def delete_backup(self, destination_path: str) -> bool:
        """Supprime la sauvegarde"""
        try:
            backup_info_path = self.get_backup_info_path(destination_path)
            
            if not backup_info_path.exists():
                return False
            
            with open(backup_info_path, 'r', encoding='utf-8') as f:
                backup_info = json.load(f)
            
            backup_path = Path(backup_info['backup_path'])
            
            # Suppression du dossier de sauvegarde
            if backup_path.exists():
                shutil.rmtree(backup_path)
            
            # Suppression du fichier d'information
            backup_info_path.unlink()
            
            # Suppression du dossier parent s'il est vide
            backup_dir = backup_info_path.parent
            if backup_dir.exists() and not any(backup_dir.iterdir()):
                backup_dir.rmdir()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression: {e}")
            return False
    
    def get_backup_status(self, destination_path: str) -> Optional[Dict]:
        """Récupère le statut de la sauvegarde"""
        if not destination_path:
            return None
        
        backup_info_path = self.get_backup_info_path(destination_path)
        
        if not backup_info_path.exists():
            return None
        
        try:
            with open(backup_info_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture des informations de sauvegarde: {e}")
            return None
    
    def backup_exists(self, destination_path: str) -> bool:
        """Vérifie si une sauvegarde existe"""
        return self.get_backup_status(destination_path) is not None