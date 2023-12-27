import sys, os
import customtkinter as ctk
from tkinter import filedialog
from tkinter import *
from PIL import Image
import shutil
import threading
from CTkMessagebox import CTkMessagebox


# Class de notre application


class Application(ctk.CTk):
    # Constructeur
    def __init__(self):
        super().__init__()

        self.title('Messiah Patch VF')
        self.iconbitmap(self.resource_path("messiah.ico"))

        # Configuration du style
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        # Cadre principal
        self.geometry("400x300")
        self.resizable(False, False)  # Empêche le redimensionnement de la fenêtre
        self.create_widgets()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Créer les widgets
    def create_widgets(self):
        ctk.CTkLabel(master=self, text="Messiah en français", font=("Arial Bold", 20), justify="left").pack(anchor="w",
                                                                                                   pady=(43, 18),
                                                                                                   padx=(56, 0))

        self.general_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.general_frame.pack(padx=(54, 0), pady=(18, 0), anchor="nw")

        # Créer des widget
        self.frame = ctk.CTkFrame(self.general_frame, fg_color="#3f4243", border_color="#FFCC70", border_width=2, corner_radius=8, width=300, height=70)
        # Ajoute le bouton, le label et le widget à notre fenêtre
        self.frame.pack_propagate(False)
        self.frame.pack(anchor="w", side="left", padx=(0, 20))

        # Créer un champ texte
        self.info = ctk.CTkLabel(
            self.frame, text="Ce patch remplace les textes et voix anglaises par  les françaises", text_color="#F3D9FF", justify="center", font=("Arial Bold",12), corner_radius=52, wraplength=250)
        self.info.pack(anchor="center", pady=(15, 0))

        img = Image.open(self.resource_path("icons8-search-50-dark-theme.png"))
        #img = Image.open("./icons8-search-50-dark-theme.png")
        # Créer un bouton
        self.button = ctk.CTkButton(
            self, text="Chemin d'installation", fg_color="#8D6F3A", hover_color="darkorange", command=self.copy_resource, font=("Arial Bold", 12), image=ctk.CTkImage(dark_image=img))
        self.button.pack(padx=(10,0),pady=(30,0))

        # Créer une barre de progression
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack_forget()
        self.progress_bar.set(0)  # Initialisation de la barre de progression à 0

    # Mettre à jour la barre de progression
    def update_progress_bar(self, value):
        self.progress_bar.set(value)

    # La tâche de copie effectuée dans un thread séparé
    def perform_copy(self, destination_folder):
        package_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'PatchFR')
        total_files = sum([len(files) for r, d, files in os.walk(package_folder)])
        copied_files = 0
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
                # Vérifiez si le répertoire de destination existe, sinon créez-le
                if not os.path.exists(os.path.dirname(dest_path)):
                    os.makedirs(os.path.dirname(dest_path))
                # Copiez chaque élément dans le dossier de destination
                shutil.copy(os.path.join(root, file), dest_path)

                copied_files += 1
                progress = (copied_files / total_files) * 100
                self.update_progress_bar(progress)

        self.open_popup(destination_folder)
        print(f"Les ressources ont été copiées dans {destination_folder}")

    # Créer une fonction qui ouvre une popup une fois les fichiers copiés
    def open_popup(self, destination_folder):
        self.msg = CTkMessagebox(title="Installé", message=f"Les ressources ont été copiées dans {destination_folder}",
                      icon="check", option_1="Merci")
        response = self.msg.get()
        if response == "Merci":
            app.quit()


    # Créer une fonction qui sera appelée lorsque vous appuyez sur le bouton
    def copy_resource(self):
        destination_folder = filedialog.askdirectory()
        if destination_folder:
            self.progress_bar.pack(pady=20)
            threading.Thread(target=self.perform_copy, args=(destination_folder,)).start()
        else:
            print("Aucun dossier cible n'a été sélectionné.")


if __name__ == "__main__":
    # Instancie notre class
    app = Application()
    # Démarre la boucle d'événements Tkinter
    app.mainloop()
