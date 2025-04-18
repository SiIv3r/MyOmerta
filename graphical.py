import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import app as se
import v5 as ae
import datetime
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SplashScreen(ctk.CTk):
    def __init__(self, callback):
        super().__init__()
        self.title("Chargement...")
        self.geometry("1000x650")
        self.resizable(False, False)
        self.callback = callback
        self.after_id = None


        logo = ctk.CTkImage(Image.open("2-3millionscestpasassez.png"), size=(600, 600))
        ctk.CTkLabel(self, image=logo, text="").pack(pady=(0, 0))

        self.progress = ctk.CTkProgressBar(self, width=500)
        self.progress.pack(pady=(0, 0))
        self.progress.set(0)

        self.loading_label = ctk.CTkLabel(self, text="Chargement en cours...", font=("Arial", 14))
        self.loading_label.pack(pady=(0, 0))

        self.after(50, self.animate)
        self.step = 0

    def animate(self):
        if not self.winfo_exists():
            return
        if self.step <= 100:
            self.progress.set(self.step / 100)
            self.step += 2
            self.after_id = self.after(80, self.animate)
        else:
            self.safe_close()
    
    def safe_close(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        if self.winfo_exists():
            self.destroy()
        self.callback()





class MyCipherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MyOmerta ✨")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.mode = "sym"
        self.history = []

        self.build_sidebar()
        self.build_main_area()
        self.show_sym_ui()

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=140)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        logo_image = ctk.CTkImage(Image.open("2-3millionscestpasassez.png"), size=(100, 100))
        ctk.CTkLabel(self.sidebar, image=logo_image, text="").pack(pady=10)


        ctk.CTkButton(self.sidebar, text="🔐 Symétrique", command=self.show_sym_ui).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="🔑 Asymétrique", command=self.show_asym_ui).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="🕓 Historique", command=self.show_history).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="ℹ️ À propos / Crédits", command=self.show_credits).pack(pady=10, fill="x")

    def build_main_area(self):
        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def create_textbox_with_placeholder(self, parent, placeholder, height):
        textbox = ctk.CTkTextbox(parent, height=height)
        textbox.insert("1.0", placeholder)
        textbox.configure(fg_color="#2a2a2a", text_color="gray")

        def clear_placeholder(event):
            if textbox.get("1.0", ctk.END).strip() == placeholder:
                textbox.delete("1.0", ctk.END)
                textbox.configure(text_color="white")

        def restore_placeholder(event):
            if textbox.get("1.0", ctk.END).strip() == "":
                textbox.insert("1.0", placeholder)
                textbox.configure(text_color="gray")

        textbox.bind("<FocusIn>", clear_placeholder)
        textbox.bind("<FocusOut>", restore_placeholder)
        return textbox

    def show_sym_ui(self):
        self.mode = "sym"
        self.clear_main_area()

        ctk.CTkLabel(self.main_area, text="Chiffrement Symétrique", font=("Arial Black", 22)).pack(pady=10)
        self.sym_key_entry = ctk.CTkEntry(self.main_area, placeholder_text="Entrez une clé", width=300)
        self.sym_key_entry.pack(pady=10)

        action_frame = ctk.CTkFrame(self.main_area)
        action_frame.pack()
        ctk.CTkButton(action_frame, text="📂 Charger .txt", command=self.load_text).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="🔒 Chiffrer", command=self.encrypt_sym).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="🔓 Déchiffrer", command=self.decrypt_sym).pack(side="left", padx=10)

        self.sym_input = self.create_textbox_with_placeholder(self.main_area, "Entrez ici votre message clair ou chiffré...", 120)
        self.sym_input.pack(fill="x", padx=20, pady=10)
        self.sym_result = self.create_textbox_with_placeholder(self.main_area, "Le résultat apparaîtra ici...", 120)
        self.sym_result.pack(fill="x", padx=20, pady=10)

        bottom_frame = ctk.CTkFrame(self.main_area)
        bottom_frame.pack(pady=10)
        ctk.CTkButton(bottom_frame, text="📋 Copier le résultat", command=self.copy_result).pack(side="left", padx=10)
        ctk.CTkButton(bottom_frame, text="📤 Sauvegarder le résultat", command=self.save_result).pack(side="left", padx=10)

    def show_asym_ui(self):
        self.mode = "asym"
        self.clear_main_area()
        self.public_key, self.private_key = ae.generer_cles()
        self.block_size_bytes = (self.public_key[0].bit_length() + 7) // 8

        ctk.CTkLabel(self.main_area, text="Chiffrement Asymétrique (RSA)", font=("Arial Black", 22)).pack(pady=10)

        action_frame = ctk.CTkFrame(self.main_area)
        action_frame.pack()
        ctk.CTkButton(action_frame, text="📂 Charger .txt", command=self.load_text).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="🔒 Chiffrer", command=self.encrypt_asym).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="🔓 Déchiffrer", command=self.decrypt_asym).pack(side="left", padx=10)

        self.asym_input = self.create_textbox_with_placeholder(self.main_area, "Entrez ici votre message clair ou chiffré...", 120)
        self.asym_input.pack(fill="x", padx=20, pady=10)
        self.asym_result = self.create_textbox_with_placeholder(self.main_area, "Le résultat apparaîtra ici...", 120)
        self.asym_result.pack(fill="x", padx=20, pady=10)

        bottom_frame = ctk.CTkFrame(self.main_area)
        bottom_frame.pack(pady=10)
        ctk.CTkButton(bottom_frame, text="📋 Copier le résultat", command=self.copy_result).pack(side="left", padx=10)
        ctk.CTkButton(bottom_frame, text="📤 Sauvegarder le résultat", command=self.save_result).pack(side="left", padx=10)

    def show_history(self):
        self.clear_main_area()
        header_frame = ctk.CTkFrame(self.main_area)
        header_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(header_frame, text="Historique des messages chiffrés", font=("Arial Black", 22)).pack(side="left")
        ctk.CTkButton(header_frame, text="🧹 Vider l'historique", command=self.clear_history).pack(side="right")

        for i, (text, timestamp) in enumerate(reversed(self.history[-10:])):
            frame = ctk.CTkFrame(self.main_area)
            frame.pack(fill="x", padx=20, pady=5)
            label = ctk.CTkLabel(frame, text=f"{timestamp} : {text[:40]}...", anchor="w")
            label.pack(side="left", fill="x", expand=True)
            ctk.CTkButton(frame, text="📋 Copier", width=60, command=lambda t=text: self.copy_to_clipboard(t)).pack(side="right", padx=5)

    def show_credits(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="À propos de MyOmerta", font=("Arial Black", 24)).pack(pady=20)
        logo_image = ctk.CTkImage(Image.open("singe.jpg"), size=(500, 300))
        ctk.CTkLabel(self.main_area, image=logo_image, text="").pack(pady=5)
        content = (
            "🛠️ Projet scolaire réalisé avec grace à Pap3rClips, Frost, Finoul, S.zzna \n"
            "🔐 Chiffrement symétrique : inspiré de ...\n"
            "🔑 Chiffrement asymétrique : ? connais pas \n"
            "💻 Interface en Python avec CustomTkinter\n\n"
            "Courage à ceux qui voudront audit nos fonctions de chiffrement"
        )
        label = ctk.CTkLabel(self.main_area, text=content, justify="left", font=("Arial", 16), anchor="w", wraplength=700)
        label.pack(padx=20, pady=10, anchor="w")

    def encrypt_sym(self):
        msg = self.sym_input.get("1.0", ctk.END).strip()
        key = self.sym_key_entry.get().strip()
        if not msg or not key:
            return
        result = se.chiffre(msg, key)
        self.sym_result.delete("1.0", ctk.END)
        self.sym_result.insert("1.0", result)
        self.add_to_history(result)

    def decrypt_sym(self):
        msg = self.sym_input.get("1.0", ctk.END).strip()
        key = self.sym_key_entry.get().strip()
        if not msg or not key:
            return
        result = se.dechiffre(msg, key)
        self.sym_result.delete("1.0", ctk.END)
        self.sym_result.insert("1.0", result)

    def encrypt_asym(self):
        msg = self.asym_input.get("1.0", ctk.END).strip()
        blocs = ae.chiffrer_securise(msg, self.public_key, self.block_size_bytes)
        result = '\n'.join([hex(b) for b in blocs])
        self.asym_result.delete("1.0", ctk.END)
        self.asym_result.insert("1.0", result)
        self.add_to_history(result)

    def decrypt_asym(self):
        text = self.asym_input.get("1.0", ctk.END).strip()
        try:
            blocs = [int(line, 16) for line in text.strip().splitlines() if line.strip()]
            result = ae.dechiffrer_securise(blocs, self.private_key, self.block_size_bytes)
            self.asym_result.delete("1.0", ctk.END)
            self.asym_result.insert("1.0", result)
        except:
            self.asym_result.insert("1.0", "[ERREUR : Format invalide ou clé incorrecte]")

    def load_text(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                if self.mode == "sym":
                    self.sym_input.delete("1.0", ctk.END)
                    self.sym_input.insert("1.0", content)
                else:
                    self.asym_input.delete("1.0", ctk.END)
                    self.asym_input.insert("1.0", content)

    def save_result(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if path:
            content = self.sym_result.get("1.0", ctk.END) if self.mode == "sym" else self.asym_result.get("1.0", ctk.END)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.strip())

    def add_to_history(self, text):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append((text, timestamp))

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        notif = ctk.CTkLabel(self.main_area, text=" Copié dans le presse-papiers", text_color="green")
        notif.pack(pady=10)
        self.after(1500, notif.destroy)

    def copy_result(self):
        result_box = self.sym_result if self.mode == "sym" else self.asym_result
        text = result_box.get("1.0", ctk.END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            notif = ctk.CTkLabel(self.main_area, text="Résultat copié 📋", text_color="green")
            notif.pack(pady=10)
            self.after(1500, notif.destroy)

    def clear_history(self):
        self.history.clear()
        self.show_history()
        notif = ctk.CTkLabel(self.main_area, text="Historique vidé 🧹", text_color="orange")
        notif.pack(pady=10)
        self.after(1500, notif.destroy)

if __name__ == "__main__":
    SplashScreen(lambda: MyCipherApp().mainloop()).mainloop()


#
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒░       ░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒▒▒▒▒░▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒        ▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒            ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▓▒▒░ ░▓░ ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒▒           ▒░▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒ ░▒▒▓▓▓▓▒▒  ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▓▒▓▓▓▒▓▓▒░  ░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒░▒▒  ▓▓▒ ░▓▓▒  ▒ ▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒░   ░▒   ░░    ░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░ ▓░▓▓▒  ░▒▒░  ░   ▒▒▒▒▒▒▒▒▒▒░▒▒▒  ░░   ░░   ░  ░▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒  ░▓▒▒░░░▒▒  ░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ▒▓▒▒░░░▒░  ▒▒     ▒▒▒▒▒▒▒▒░   ▒ ░▒▒░░▒░▒▒░  ▒  ░▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒░  ░▓░▒░▒▒▒   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓▓▓▒▓▒          ░▒▒▒▒▒▒   ░▒ ░▒░▒░░▒▒░   ▒▒  ░▒▒▒▒▒
#▒▒▒▒▒▒▒▒  ░▒▒▒░▒▒▒░▓     ░▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ░░   ░░░░          ░▒▒▒▒▒   ░▒   ▒▓▒▒▓▒▒  ░ ▒▒  ░▒▒▒▒
#▒▒▒▒▒░    ▒▒▓▓▓▒           ▒▒▒▒▒▒▒▒▒▒▒▒    ▓▒  ░▒▓░           ░▒▒▒░ ░░ ▒  ░▓▒▒▒▒▒▒  ░       ▒▒▒
#▒▒▒░      ░▒▓▓▓░           ░▒▒▒▒▒▒▒▒        ▒▓▓▓▒              ░▒          ▒░▒▒▒░░           ▒▒
#▒▒         ░▒▒▒░░░░░  ░     ▒▒▒▒░          ▓░   ░▒▓░                        ▒▒▒▒▒            ░▒
#▒░          ▒░▒▒▒▒▓▓ ░       ▒▒▒           ▓▓▒▒▒▒▓▓                       ▒      ░░           ▒
#▒           ▓▓▒▒▒▓▓▒          ▒░           ░▓▓▒▒▒▓▓                       ░▓▒▒▒▒▒▒            ░
#▒           ░▓▒▒▒▒▓                         ▓▒▒▒▒▓                         ▒▓▒▒▒▒▒            ░
#▒            ▒▒▒▒▒▒                         ▒▒▒▒▒▒                          ▒▒▒▒▒              
#▒            ░▒▒▒▒                          ▒▒▒▒▒░                          ▒▒▒▒▒              
#░             ▒▒▒░                           ▒▒▒▒                            ▒▒▒               
#▒             ▒▒▒                            ▒▒▒░                            ░▒▒               
#▒              ▒░                            ░▒▒                              ▒                
#▒              ▒                              ▒░                                               
#▒                                             ░                                                
#▒▒                                                                                             
#▒░░                                                                                            
#▒▒▒░                                                                                           

#                                       LOI DES 3 SINGES