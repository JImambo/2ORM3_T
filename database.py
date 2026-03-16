from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk

COLOR_BG_MAIN = "#1a1a1a"      # Fond sombre principal
COLOR_BG_SIDEBAR = "#252526"   # Fond de la barre latérale
COLOR_ACCENT = "#1f538d"       # Bleu (Actions standards)
COLOR_SUCCESS = "#28a745"      # Vert (Ajouter)
COLOR_DANGER = "#dc3545"       # Rouge (Supprimer)
COLOR_TEXT = "#ffffff"         # Blanc

# Configuration native de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- CONFIGURATION ---
Base_Dir = Path(__file__).resolve().parent
DB_PATH = Base_Dir / "demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()

# --- MODÈLE ---
class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f"Utilisateur(id={self.id}, nom='{self.nom}', email='{self.email}')"

# Création des tables
Base.metadata.create_all(engine)

# --- FONCTIONS SQLALCHEMY (Logique Métier) ---
def ajouter_utilisateur(nom, email):
    with Session(engine) as session:
        existe = session.query(Utilisateur).filter_by(email=email).first()
        if existe:
            return False, f"L'email {email} est déjà utilisé."
        nouveau = Utilisateur(nom=nom, email=email)
        session.add(nouveau)
        session.commit()
        return True, f"{nom} ajouté avec succès."

def modifier_utilisateur(user_id, nouveau_nom=None, nouvel_email=None):
    with Session(engine) as session:
        u = session.get(Utilisateur, user_id)
        if not u: return False, "Utilisateur introuvable."
        if nouveau_nom: u.nom = nouveau_nom
        if nouvel_email: u.email = nouvel_email
        session.commit()
        return True, "Mise à jour réussie."

def supprimer_utilisateur(user_id):
    with Session(engine) as session:
        u = session.get(Utilisateur, user_id)
        if u:
            session.delete(u)
            session.commit()
            return True
        return False

# --- INTERFACE GRAPHIQUE ---
class AppGraphique(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion Utilisateurs - Live")
        self.geometry("950x600")
        
        # Configuration du Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Barre Latérale) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=COLOR_BG_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.label_logo = ctk.CTkLabel(self.sidebar, text="DATABASE MANAGER", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_logo.pack(pady=30)

        self.btn_refresh = ctk.CTkButton(self.sidebar, text="Actualiser Liste", fg_color=COLOR_ACCENT, command=self.ui_lister)
        self.btn_refresh.pack(pady=10, padx=20)

        # --- MAIN CONTENT (Zone Principale) ---
        self.main_content = ctk.CTkFrame(self, fg_color=COLOR_BG_MAIN)
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Recherche Live
        self.entree_recherche = ctk.CTkEntry(self.main_content, placeholder_text=" Rechercher par nom...", width=450)
        self.entree_recherche.pack(pady=15)
        self.entree_recherche.bind("<KeyRelease>", self.filtrer_en_temps_reel)

        # Formulaire
        self.form_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=40, pady=10)
        
        self.entree_nom = ctk.CTkEntry(self.form_frame, placeholder_text="Nom complet")
        self.entree_nom.pack(side="left", expand=True, fill="x", padx=5)
        
        self.entree_email = ctk.CTkEntry(self.form_frame, placeholder_text="Adresse Email")
        self.entree_email.pack(side="left", expand=True, fill="x", padx=5)

        # Boutons d'Action (avec utilisation des variables de couleur)
        self.btns_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.btns_frame.pack(fill="x", padx=40, pady=15)

        self.btn_add = ctk.CTkButton(self.btns_frame, text="AJOUTER", fg_color=COLOR_SUCCESS, hover_color="#218838", command=self.ui_ajouter)
        self.btn_add.pack(side="left", padx=5)

        self.btn_mod = ctk.CTkButton(self.btns_frame, text="MODIFIER", fg_color=COLOR_ACCENT, command=self.ui_modifier)
        self.btn_mod.pack(side="left", padx=5)

        self.btn_del = ctk.CTkButton(self.btns_frame, text="SUPPRIMER", fg_color=COLOR_DANGER, hover_color="#c82333", command=self.ui_supprimer)
        self.btn_del.pack(side="right", padx=5)
        
        # --- TABLEAU DES RÉSULTATS ---
        self.setup_table_style()
        self.tableau = ttk.Treeview(self.main_content, columns=("ID", "Nom", "Email"), show="headings")
        self.tableau.heading("ID", text="ID")
        self.tableau.heading("Nom", text="Nom")
        self.tableau.heading("Email", text="Email")
        self.tableau.column("ID", width=50, anchor="center")
        
        # Affichage dans l'interface
        self.tableau.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Remplir champ selon séléction
        self.tableau.bind("<<TreeviewSelect>>", self.remplir_champs_depuis_selection)
        
        # Chargement des données
        self.ui_lister()

    def setup_table_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=30)
        style.map("Treeview", background=[('selected', COLOR_ACCENT)])
        style.configure("Treeview.Heading", background="#333333", foreground="white", relief="flat")

    # --- MÉTHODES UI ---
    def ui_lister(self):
        self.filtrer_en_temps_reel(None)

    def ui_ajouter(self):
        nom, email = self.entree_nom.get(), self.entree_email.get()
        if nom and email:
            succes, msg = ajouter_utilisateur(nom, email)
            if succes:
                self.ui_lister()
                self.entree_nom.delete(0, 'end'); self.entree_email.delete(0, 'end')
            else: messagebox.showerror("Erreur", msg)
        else: messagebox.showwarning("Champs vides", "Remplissez les deux champs.")

    def ui_modifier(self):
        select = self.tableau.selection()
        if not select: 
            return messagebox.showwarning("Sélection", "Choisissez un utilisateur.")
        
        uid = self.tableau.item(select[0])['values'][0]
        
        if modifier_utilisateur(uid, self.entree_nom.get(), self.entree_email.get()):
            
            self.entree_nom.delete(0, 'end')
            self.entree_email.delete(0, 'end')
            
            self.ui_lister()
        
            messagebox.showinfo("Succès", "Utilisateur mis à jour !")

    def ui_supprimer(self):
        select = self.tableau.selection()
        if not select: return
        uid = self.tableau.item(select[0])['values'][0]
        if messagebox.askyesno("Confirmation", "Supprimer cet utilisateur ?"):
            if supprimer_utilisateur(uid): self.ui_lister()

    def filtrer_en_temps_reel(self, event):
        txt = self.entree_recherche.get().lower()
        for item in self.tableau.get_children(): self.tableau.delete(item)
        with Session(engine) as session:
            utilisateurs = session.query(Utilisateur).filter(Utilisateur.nom.contains(txt)).all()
            for u in utilisateurs:
                self.tableau.insert("", "end", values=(u.id, u.nom, u.email))
    
    def remplir_champs_depuis_selection(self, event):
        select = self.tableau.selection()
        if select:
            # Récupérer les valeurs de la ligne cliquée
            valeurs = self.tableau.item(select[0])['values']
            
            # Remplir les champs (on vide avant pour ne pas accumuler le texte)
            self.entree_nom.delete(0, 'end')
            self.entree_nom.insert(0, valeurs[1]) # Index 1 = Nom
            
            self.entree_email.delete(0, 'end')
            self.entree_email.insert(0, valeurs[2]) # Index 2 = Email

if __name__ == "__main__":
    app = AppGraphique()
    app.mainloop()