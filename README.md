# Messiah-VF-Patch
Messiah-VF-Patch est un projet Python visant à fournir les voix et textes en français pour le jeu `Messiah`.

[![OS - Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows&logoColor=white)](https://www.microsoft.com/ "Go to Microsoft homepage")
[![GitHub tag](https://img.shields.io/github/tag/Aiola13/Messiah-VF-Patch?include_prereleases=&sort=semver&color=blue)](https://github.com/Aiola13/Messiah-VF-Patch/releases/)
[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
![visitors](https://visitor-badge.glitch.me/badge?page_id=aiola13.Messiah-VF-Patch)
![Files](https://img.shields.io/github/directory-file-count/Aiola13/Messiah-VF-Patch?type=file&?style=flat-square)
![Size](https://img.shields.io/github/repo-size/Aiola13/Messiah-VF-Patch?style=flat-square)

[![Made with GH Actions](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=github-actions&logoColor=white)](https://github.com/features/actions "Go to GitHub Actions homepage")
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![stars - Messiah-VF-Patch](https://img.shields.io/github/stars/Aiola13/Messiah-VF-Patch?style=social)](https://github.com/Aiola13/Messiah-VF-Patch)
[![forks - Messiah-VF-Patch](https://img.shields.io/github/forks/Aiola13/Messiah-VF-Patch?style=social)](https://github.com/Aiola13/Messiah-VF-Patch)

## Overview

Il suffit de cliquer sur le bouton et de fournir le dossier d'installation de `Messiah`.
Le logiciel s'occupe de copier les fichiers dans le répertoire d'installation sélectionné.

<div align="center">

  ![Alt text](overview.png)
  
  <a href="https://github.com/Aiola13/Messiah-VF-Patch/releases/latest">
    <b>Télécharger le patch</b>
  </a>
</div>

## Attention
Le patch ne sauvegarde pas les fichiers originaux. Si un problème se produit, vous devrez re-télécharger le jeu complet.

Une mise à jour viendra ajouter la sauvegarde et la récupération des fichiers originaux.

Il se peut qu'avec certains Anti-virus, le programme soit détecté comme étant un faux positif.

Pour tous bogues, merci d'ouvrir une [`Issue`](https://github.com/Aiola13/Messiah-VF-Patch/issues/new/choose).

## Features

- Tous les textes en français
- Vidéos en français
- Voix en français

### To do

- Menu pause en anglais
- Video de fin en anglais
- Remap touche clavier azerty
  
## Usage

### EXE
Vous pouvez directement télécharger la [release](https://github.com/Aiola13/Messiah-VF-Patch/releases/latest), compilée à partir de Github et l'utiliser sans librairie.


### PY
Pour utiliser le patch, vous aurez besoin de Python 3 et des bibliothèques suivantes :

- [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter) (Evolution de [`tkinter`](https://docs.python.org/fr/3/library/tkinter.html))
- [`CTkMessageBox`](https://github.com/Akascape/CTkMessagebox)
  
Pour installer ces dépendances, utiliser la commande pip :

```bash
pip install customtkinter
pip install CTkMessageBox
```

Pour lancer l'application, utiliser la commande `python` : 

```bash
python messiah_patch.py
```
OU
```bash
python3 messiah_patch.py
```

Pour regrouper le script `py` et l'ensemble de ses dépendances dans un paquet, vous aurez besoin d'installer :

-  `pysintaller`

Pour installer cette dépendace, utilisez la commande pip :

```bash
pip install pyinstaller
```

Pour compiler le script sans icones, utiliser la commande suivante : 

```bash
pyinstaller --onefile --windowed messiah_patch.py
```

ou avec les icones :

```bash
pyinstaller --onefile --windowed --add-data "messiah.ico:." --add-data "icons8-search-50-dark-theme.png:." messiah_patch.py
```

Les options `--onefile` et `--windowed` signifient respectivement 'un seul fichier EXE' et 'sans ouvrir de terminal' (synonymes `-w` and `--noconsole`).



## Contribution
J'apprécie toute contribution à ce projet. Si vous souhaitez contribuer, veuillez suivre les étapes suivantes :

- Forker le projet
- Créer une nouvelle branche (git checkout -b my-feature)
- Committer vos modifications (git commit -am 'Add some feature')
- Pusher la branche (git push origin my-feature)
- Créer une nouvelle Pull Request

## Logiciels et ressources

Les logiciels utilisés et les informations utiles pour comprendre le format .MVE : 

- [Forum nma-fallout](https://www.nma-fallout.com)
  - [https://www.nma-fallout.com/threads/converting-video-to-mve.218520/](https://www.nma-fallout.com/threads/converting-video-to-mve.218520/)
  - [https://www.nma-fallout.com/threads/new-beta-of-avi2mve-converter.155987/#post-3088840](https://www.nma-fallout.com/threads/new-beta-of-avi2mve-converter.155987/#post-3088840)
  - [https://www.nma-fallout.com/threads/avi2mve.220407/#post-4432138](https://www.nma-fallout.com/threads/avi2mve.220407/#post-4432138)
- [Forum fforum.kochegarov](https://fforum.kochegarov.com/)
- [Applications](http://www.teamx.ru/site_arc/utils/index.html) de la [TeamX](http://www.teamx.ru) qui permettent de convertir du format `.mve` à `.avi`
  - [avi2mve](http://www.teamx.ru/site_arc/utils/avi2mve_040919.rar) (Lien direct vers le rar)
    ```
    .\avi2mve.exe .\intro.avi -w .\track26.wav -size 60 -hq
    ```
  - [mve2avi](http://www.teamx.ru/site_arc/utils/mve2avi2.4h.rar) (Lien direct vers le rar)
    ```
    .\fsp.exe .\intro.mve .\intro.avi
    ```
- [VirtualDub](https://virtualdub.org) qui permet d'ajouter l'audio et de conserver le codec utilisé par les logiciels précédents


## License
Messiah-VF-Patch est sous licence [MIT](/LICENSE) by [@Aiola13](https://github.com/Aiola13).
Pour plus d'informations, consultez le fichier LICENSE.