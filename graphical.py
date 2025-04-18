import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import symmetric_encryption as se
import asymmetric_encryption as ae
import datetime

class MyCipherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MyOmerta")
        self.geometry("1000x650")

        self.mode = "sym"
        self.history = []
        self.sym_key_value = None

        self.build_sidebar()
        self.build_main_area()
        self.show_sym_ui()

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=140)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        logo_image = ctk.CTkImage(Image.open("2-3millionscestpasassez.png"), size=(100, 100))
        ctk.CTkLabel(self.sidebar, image=logo_image, text="").pack(pady=10)

        ctk.CTkButton(self.sidebar, text="🔐 Symétrique", command=self.show_sym_ui).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="🔑 Asymétrique", command=self.show_asym_ui).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="🕓 Historique", command=self.show_history).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="⚙️ Paramètres", command=self.show_settings).pack(padx=10, pady=10)
        ctk.CTkButton(self.sidebar, text="ℹ️ À propos", command=self.show_credits).pack(padx=10, pady=10)

    def build_main_area(self):
        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def create_textbox_with_placeholder(self, parent, placeholder, height):
        textbox = ctk.CTkTextbox(parent, height=height)
        textbox.insert("1.0", placeholder)

        def clear_placeholder(event):
            if textbox.get("1.0", ctk.END).strip() == placeholder:
                textbox.delete("1.0", ctk.END)

        def restore_placeholder(event):
            if textbox.get("1.0", ctk.END).strip() == "":
                textbox.insert("1.0", placeholder)

        textbox.bind("<FocusIn>", clear_placeholder)
        textbox.bind("<FocusOut>", restore_placeholder)
        return textbox

    def show_sym_ui(self):
        self.mode = "sym"
        self.clear_main_area()

        ctk.CTkLabel(self.main_area, text="Chiffrement symétrique", font=("Arial Black", 22)).pack(pady=10)
        self.sym_key_entry = ctk.CTkEntry(self.main_area, placeholder_text="Entrez une clé", width=300)
        self.sym_key_entry.pack(pady=10)
        if self.sym_key_value:
            self.sym_key_entry.delete(0, ctk.END)
            self.sym_key_entry.insert(0, self.sym_key_value)
            self.sym_key_value = None

        action_frame = ctk.CTkFrame(self.main_area)
        action_frame.pack()
        ctk.CTkButton(action_frame, text="📂 Charger .txt", command=self.load_text).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(action_frame, text="🔒 Chiffrer", command=self.encrypt_sym).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(action_frame, text="🔓 Déchiffrer", command=self.decrypt_sym).pack(side="left", padx=10, pady=10)

        self.sym_input = self.create_textbox_with_placeholder(self.main_area, "Entrez ici votre message en clair ou chiffré...", 120)
        self.sym_input.pack(fill="x", padx=20, pady=10)
        self.sym_result = self.create_textbox_with_placeholder(self.main_area, "Le résultat apparaîtra ici...", 120)
        self.sym_result.pack(fill="x", padx=20, pady=10)

        bottom_frame = ctk.CTkFrame(self.main_area)
        bottom_frame.pack(pady=10)
        ctk.CTkButton(bottom_frame, text="📋 Copier le résultat", command=self.copy_result).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(bottom_frame, text="📤 Sauvegarder le résultat", command=self.save_result).pack(side="left", padx=10, pady=10)

    def show_asym_ui(self):
        self.mode = "asym"
        self.clear_main_area()

        ctk.CTkLabel(self.main_area, text="Chiffrement asymétrique (RSA)", font=("Arial Black", 22)).pack(pady=10)

        action_frame = ctk.CTkFrame(self.main_area)
        action_frame.pack()
        ctk.CTkButton(action_frame, text="📂 Charger .txt", command=self.load_text).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(action_frame, text="🔒 Chiffrer", command=self.encrypt_asym).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(action_frame, text="🔓 Déchiffrer", command=self.decrypt_asym).pack(side="left", padx=10, pady=10)

        self.asym_input = self.create_textbox_with_placeholder(self.main_area, "Entrez ici votre message en clair ou chiffré...", 120)
        self.asym_input.pack(fill="x", padx=20, pady=10)
        self.asym_result = self.create_textbox_with_placeholder(self.main_area, "Le résultat apparaîtra ici...", 120)
        self.asym_result.pack(fill="x", padx=20, pady=10)

        bottom_frame = ctk.CTkFrame(self.main_area)
        bottom_frame.pack(pady=10)
        ctk.CTkButton(bottom_frame, text="📋 Copier le résultat", command=self.copy_result).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(bottom_frame, text="📤 Sauvegarder le résultat", command=self.save_result).pack(side="left", padx=10, pady=10)

    def show_history(self):
        self.clear_main_area()
        header_frame = ctk.CTkFrame(self.main_area)
        header_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(header_frame, text="Historique des messages chiffrés", font=("Arial Black", 22)).pack(side="left")
        ctk.CTkButton(header_frame, text="🧹 Vider l'historique", command=self.clear_history).pack(side="right")

        history_slice = list(reversed(self.history[-10:]))
        for i, (text, timestamp) in enumerate(history_slice):
            frame = ctk.CTkFrame(self.main_area)
            frame.pack(fill="x", padx=20, pady=5)
            label = ctk.CTkLabel(frame, text=f"{timestamp} : {text[:40]}...", anchor="w")
            label.pack(side="left", fill="x", expand=True)
            ctk.CTkButton(frame, text="📋 Copier", width=60, command=(lambda t=text: lambda: self.copy_to_clipboard(t))()).pack(side="right", padx=5)

    def show_settings(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Paramètres des clés", font=("Arial Black", 22)).pack(pady=10)
        sym_frame = ctk.CTkFrame(self.main_area)
        sym_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(sym_frame, text="Clé symétrique", font=("Arial", 16)).pack(side="left", padx=10)
        ctk.CTkButton(sym_frame, text="Importer la clé", command=self.import_sym_key).pack(side="left", padx=10)
        ctk.CTkButton(sym_frame, text="Exporter la clé", command=self.export_sym_key).pack(side="left", padx=10)
        asym_frame = ctk.CTkFrame(self.main_area)
        asym_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(asym_frame, text="Clés asymétriques (RSA)", font=("Arial", 16)).pack(side="left", padx=10)
        ctk.CTkButton(asym_frame, text="Importer les clés", command=self.import_asym_keys).pack(side="left", padx=10)
        ctk.CTkButton(asym_frame, text="Exporter les clés", command=self.export_asym_keys).pack(side="left", padx=10)

    def import_sym_key(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                key = f.read().strip()
                if hasattr(self, 'sym_key_entry') and self.mode == "sym":
                    self.sym_key_entry.delete(0, ctk.END)
                    self.sym_key_entry.insert(0, key)
                else:
                    self.sym_key_value = key
                self.show_message("Clé symétrique importée", color="green")

    def export_sym_key(self):
        if hasattr(self, 'sym_key_entry'):
            key = self.sym_key_entry.get().strip()
            if not key:
                self.show_message("Aucune clé symétrique à exporter", color="red")
                return
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(key)
                self.show_message("Clé symétrique exportée", color="green")

    def import_asym_keys(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                if len(lines) >= 2:
                    try:
                        n = int(lines[0])
                        e = int(lines[1])
                        d = int(lines[2]) if len(lines) > 2 else None
                        self.public_key = (n, e)
                        if d:
                            self.private_key = (n, d)
                        self.block_size_bytes = (n.bit_length() + 7) // 8
                        self.show_message("Clés asymétriques importées", color="green")
                    except Exception:
                        self.show_message("Format de clés invalide", color="red")
                else:
                    self.show_message("Fichier de clés incomplet", color="red")

    def export_asym_keys(self):
        if hasattr(self, 'public_key') and hasattr(self, 'private_key'):
            n, e = self.public_key
            _, d = self.private_key
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(f"{n}\n{e}\n{d}")
                self.show_message("Clés asymétriques exportées", color="green")
        else:
            self.show_message("Aucune clé asymétrique à exporter", color="red")

    def show_credits(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="À propos de MyOmerta").pack(pady=20)
        logo_image = ctk.CTkImage(Image.open("singe.jpg"), size=(500, 300))
        ctk.CTkLabel(self.main_area, image=logo_image, text="").pack(pady=5)
        content = (
            "🛠️ Projet scolaire réalisé avec Pap3rClips, Frost, Finoul, S.zzna \n"
            "🔐 Chiffrement symétrique : inspiré de ...\n"
            "🔑 Chiffrement asymétrique : ? connais pas \n"
            "💻 Interface en Python avec CustomTkinter\n\n"
            "Courage à ceux qui voudront audit nos fonctions de chiffrement"
        )
        label = ctk.CTkLabel(self.main_area, text=content, justify="left", font=("Arial", 16), anchor="w", wraplength=700)
        label.pack(padx=20, pady=10, anchor="w")

    def get_entry_text(self, mode):
        default_msg_1 = "Entrez ici votre message en clair ou chiffré..."
        if mode == "sym":
            msg = self.sym_input.get("1.0", ctk.END).strip()
            if not msg or msg == default_msg_1:
                return None
            return msg
        elif mode == "asym":
            msg = self.asym_input.get("1.0", ctk.END).strip()
            if not msg or msg == default_msg_1:
                return None
            return msg

    def encrypt_sym(self):
        key = self.sym_key_entry.get().strip()
        msg = self.get_entry_text("sym")
        if not msg and not key:
            self.show_message("Veuillez entrer un message et une clé.", color="red")
            return
        if not msg:
            self.show_message("Veuillez entrer un message.", color="red")
            return
        if not key:
            self.show_message("Veuillez entrer une clé.", color="red")
            return
        try:
            result = se.chiffre(msg, key)
            self.sym_result.delete("1.0", ctk.END)
            self.sym_result.insert("1.0", result)
            self.add_to_history(result)
        except Exception as e:
            self.show_message(f"Erreur de chiffrement : {str(e)}", color="red")

    def decrypt_sym(self):
        key = self.sym_key_entry.get().strip()
        msg = self.get_entry_text("sym")
        if not key and not msg:
            self.show_message("Veuillez entrer un message et une clé.", color="red")
            return
        if not key:
            self.show_message("Veuillez entrer une clé.", color="red")
            return
        if not msg:
            self.show_message("Veuillez entrer un message.", color="red")
            return
        try:
            result = se.dechiffre(msg, key)
            self.sym_result.delete("1.0", ctk.END)
            self.sym_result.insert("1.0", result)
        except Exception as e:
            self.show_message(f"Erreur de déchiffrement : {str(e)}", color="red")

    def encrypt_asym(self):
        msg = self.get_entry_text("asym")
        if not msg:
            self.show_message("Veuillez entrer un message.", color="red")
            return
        try:
            self.public_key, self.private_key = ae.generer_cles()
            self.block_size_bytes = (self.public_key[0].bit_length() + 7) // 8
            blocs = ae.chiffrer_securise(msg, self.public_key, self.block_size_bytes)
            result = '\n'.join([hex(b) for b in blocs])
            self.asym_result.delete("1.0", ctk.END)
            self.asym_result.insert("1.0", result)
            self.add_to_history(result)
        except Exception as e:
            self.show_message(f"Erreur de chiffrement : {str(e)}", color="red")

    def decrypt_asym(self):
        msg = self.get_entry_text("asym")
        if not msg:
            self.show_message("Veuillez entrer un message.", color="red")
            return
        try:
            blocs = [int(line, 16) for line in msg.strip().splitlines() if line.strip()]
            result = ae.dechiffrer_securise(blocs, self.private_key, self.block_size_bytes)
            self.asym_result.delete("1.0", ctk.END)
            self.asym_result.insert("1.0", result)
        except Exception as e:
            self.show_message(f"Erreur de déchiffrement : {str(e)}", color="red")

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

    def show_message(self, message, color="green", duration=3000):
        for widget in self.main_area.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and getattr(widget, 'is_message_notification', False):
                widget.destroy()
        notif = ctk.CTkLabel(self.main_area, text=message, text_color=color, font=("Arial Black", 16))
        notif.is_message_notification = True
        notif.pack(padx=10, pady=10)
        def fade_out(alpha=1.0):
            if alpha > 0:
                if color == "green":
                    base = (0, 128, 10)
                elif color == "orange":
                    base = (255, 165, 0)
                else:
                    base = (255, 0, 0)
                faded = f"#{int(base[0] + (42-base[0])*(1-alpha)):02x}{int(base[1] + (42-base[1])*(1-alpha)):02x}{int(base[2] + (42-base[2])*(1-alpha)):02x}"
                if notif.winfo_exists():
                    notif.configure(text_color=faded)
                    self.after(50, lambda: fade_out(alpha-0.05))
            else:
                if notif.winfo_exists():
                    notif.destroy()
        self.after(duration, fade_out)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.show_message("Copié dans le presse-papiers 📋")

    def copy_result(self):
        result_box = self.sym_result if self.mode == "sym" else self.asym_result
        text = result_box.get("1.0", ctk.END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.show_message("Copié dans le presse-papiers 📋")

    def clear_history(self):
        self.history.clear()
        self.show_history()
        self.show_message("Historique vidé 🧹", color="red")

if __name__ == "__main__":
    MyCipherApp().mainloop()