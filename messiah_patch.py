import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import shutil

# Class de notre application


class Application(tk.Tk):
    # Constructeur
    def __init__(self):
        tk.Tk.__init__(self)
        self.create_widgets()

    # Créer les widgets
    def create_widgets(self):
        # Créer un champ texte
        self.info = tk.Label(
            self, text="Ce patch remplace les textes et voix anglaises par  les françaises")
        self.label = tk.Label(
            self, text="Cliquer sur le bouton et sélectionner le chemin où est installé `Messiah`")
        # Créer un bouton
        self.button = tk.Button(
            self, text="Chemin d'installation", command=self.copy_resource)
        # Ajoute le bouton et le label à notre fenêtre
        self.info.pack()
        self.label.pack()
        self.button.pack()

    # Créer une fonction qui ouvre une popup une fois les fichiers copiés
    def open_popup(self, destination_folder):
        pop = Toplevel(self)
        pop.geometry("400x50")
        pop.title("MessageBox")
        pop.label = tk.Label(
            pop, text=f"Les ressources ont été copiées dans {destination_folder}")
        pop.button = tk.Button(
            pop, text="Quitter", command=pop.quit)
        pop.label.pack()
        pop.button.pack()

    # Créer une fonction qui sera appelée lorsque vous appuyez sur le bouton

    def copy_resource(self):
        # Contient le dossier de destination final
        destination_folder = filedialog.askdirectory()
        print(f"Dossier sélectionné: {destination_folder}")
        # Contient le lien du dossier de package/resource
        package_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'resources', 'PatchFR')
        # Vérifie si le chemin du dossier cible a été sélectionné
        if destination_folder:
            for root, dirs, files in os.walk(package_folder):
                for file in files:
                    # Contient le chemin de chaque fichier
                    source_path = os.path.join(root, file)
                    if file == "Messiah.fra":
                        source_path = source_path.replace(file, "Messiah.eng")
                    if file == "fspeek.dta":
                        source_path = source_path.replace(file, "espeek.dta")
                    if file == "fspeek.idx":
                        source_path = source_path.replace(file, "espeek.idx")
                    # Remplace le chemin du package par le chemin de destination
                    dest_path = source_path.replace(
                        package_folder, destination_folder)
                    # Vérifiez si le répertoire de destination existe, sinon créez-lepip3
                    if not os.path.exists(os.path.dirname(dest_path)):
                        os.makedirs(os.path.dirname(dest_path))
                    # Copiez chaque élément dans le dossier de destination
                    shutil.copy(os.path.join(root, file), dest_path)
            self.open_popup(destination_folder)
            print(f"Les ressources ont été copiées dans {destination_folder}")
        else:
            print("Aucun dossier cible n'a été sélectionné.")


if __name__ == "__main__":
    # Instancie notre class
    app = Application()
    # Modifie le titre de la fenêtre
    app.title("Messiah Patch VF :-)")
    # app.iconbitmap(os.path.join(
    #   os.path.dirname(os.path.abspath(__file__)), "resources", 'messiah.ico'))
    # icon = tk.PhotoImage(file='messiah.gif')
    # app.iconphoto(True, icon)
    app.geometry("600x120")
    # Démarre la boucle d'événements Tkinter
    app.mainloop()
