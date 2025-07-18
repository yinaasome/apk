#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Orange Money - Version simplifiée qui fonctionne
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import sqlite3
from datetime import datetime

# =============================================================================
# GESTIONNAIRE DE BASE DE DONNÉES
# =============================================================================

class DatabaseManager:
    """Gestionnaire pour toutes les opérations de base de données"""
    
    @staticmethod
    def init_database():
        """Initialise la base de données avec les tables nécessaires"""
        conn = sqlite3.connect("orange_money.db")
        cursor = conn.cursor()
        
        # Table des utilisateurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des opérations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                numero TEXT NOT NULL,
                cnib TEXT NOT NULL,
                reseau TEXT NOT NULL,
                montant REAL NOT NULL,
                operation TEXT NOT NULL,
                date DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insérer un utilisateur par défaut si la table est vide
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("admin", "admin123")
            )
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def verify_user(username, password):
        """Vérifie les identifiants d'un utilisateur"""
        conn = sqlite3.connect("orange_money.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    @staticmethod
    def save_operation(nom, prenom, numero, cnib, reseau, montant, operation):
        """Enregistre une opération dans la base de données"""
        conn = sqlite3.connect("orange_money.db")
        cursor = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO operations (nom, prenom, numero, cnib, reseau, montant, operation, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, prenom, numero, cnib, reseau, montant, operation, date))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_statistics():
        """Récupère les statistiques des opérations"""
        conn = sqlite3.connect("orange_money.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT reseau, operation, COUNT(*), SUM(montant)
            FROM operations 
            GROUP BY reseau, operation
            ORDER BY reseau, operation
        """)
        stats = cursor.fetchall()
        conn.close()
        return stats

# =============================================================================
# ÉCRANS DE L'APPLICATION
# =============================================================================

class LoginScreen(Screen):
    """Écran de connexion"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Construit l'interface de connexion"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Titre
        title = Label(text='ORANGE MONEY', font_size='32sp', size_hint_y=None, height=60)
        title.color = [1, 0.5, 0, 1]  # Orange
        main_layout.add_widget(title)
        
        # Champ utilisateur
        main_layout.add_widget(Label(text='Nom d\'utilisateur:', size_hint_y=None, height=30))
        self.username_input = TextInput(hint_text='Entrez votre nom d\'utilisateur', 
                                       size_hint_y=None, height=40, multiline=False)
        main_layout.add_widget(self.username_input)
        
        # Champ mot de passe
        main_layout.add_widget(Label(text='Mot de passe:', size_hint_y=None, height=30))
        self.password_input = TextInput(hint_text='Entrez votre mot de passe', 
                                       size_hint_y=None, height=40, multiline=False, password=True)
        main_layout.add_widget(self.password_input)
        
        # Message d'erreur
        self.message_label = Label(text='', color=[1, 0, 0, 1], size_hint_y=None, height=30)
        main_layout.add_widget(self.message_label)
        
        # Bouton connexion
        login_btn = Button(text='SE CONNECTER', size_hint_y=None, height=50)
        login_btn.background_color = [1, 0.5, 0, 1]  # Orange
        login_btn.bind(on_press=self.verifier_login)
        main_layout.add_widget(login_btn)
        
        # Espace
        main_layout.add_widget(Label())
        
        self.add_widget(main_layout)
    
    def verifier_login(self, instance):
        """Vérifie les identifiants de connexion"""
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username or not password:
            self.message_label.text = "Veuillez remplir tous les champs"
            return
        
        if DatabaseManager.verify_user(username, password):
            self.manager.current = "menu"
            self.username_input.text = ""
            self.password_input.text = ""
            self.message_label.text = ""
        else:
            self.message_label.text = "Identifiants incorrects"

class MenuScreen(Screen):
    """Écran du menu principal"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Construit l'interface du menu"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Titre
        title = Label(text='MENU PRINCIPAL', font_size='28sp', size_hint_y=None, height=60)
        title.color = [1, 0.5, 0, 1]  # Orange
        main_layout.add_widget(title)
        
        # Bouton nouvelle opération
        new_op_btn = Button(text='NOUVELLE OPERATION', size_hint_y=None, height=50)
        new_op_btn.background_color = [0.2, 0.7, 0.2, 1]  # Vert
        new_op_btn.bind(on_press=self.aller_vers_saisie)
        main_layout.add_widget(new_op_btn)
        
        # Bouton statistiques
        stats_btn = Button(text='STATISTIQUES', size_hint_y=None, height=50)
        stats_btn.background_color = [0.2, 0.5, 0.8, 1]  # Bleu
        stats_btn.bind(on_press=self.aller_vers_stats)
        main_layout.add_widget(stats_btn)
        
        # Bouton déconnexion
        logout_btn = Button(text='DECONNEXION', size_hint_y=None, height=50)
        logout_btn.background_color = [0.8, 0.3, 0.3, 1]  # Rouge
        logout_btn.bind(on_press=self.deconnecter)
        main_layout.add_widget(logout_btn)
        
        # Espace
        main_layout.add_widget(Label())
        
        self.add_widget(main_layout)
    
    def aller_vers_saisie(self, instance):
        """Navigue vers l'écran de saisie"""
        self.manager.current = "saisie"
    
    def aller_vers_stats(self, instance):
        """Navigue vers l'écran des statistiques"""
        self.manager.current = "stats"
    
    def deconnecter(self, instance):
        """Déconnecte l'utilisateur"""
        self.manager.current = "login"

class SaisieScreen(Screen):
    """Écran de saisie des opérations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Construit l'interface de saisie"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Titre
        title = Label(text='NOUVELLE OPERATION', font_size='24sp', size_hint_y=None, height=50)
        title.color = [1, 0.5, 0, 1]  # Orange
        main_layout.add_widget(title)
        
        # Champs de saisie
        main_layout.add_widget(Label(text='Nom:', size_hint_y=None, height=25))
        self.nom_input = TextInput(hint_text='Entrez le nom', size_hint_y=None, height=35, multiline=False)
        main_layout.add_widget(self.nom_input)
        
        main_layout.add_widget(Label(text='Prenom:', size_hint_y=None, height=25))
        self.prenom_input = TextInput(hint_text='Entrez le prenom', size_hint_y=None, height=35, multiline=False)
        main_layout.add_widget(self.prenom_input)
        
        main_layout.add_widget(Label(text='Numero:', size_hint_y=None, height=25))
        self.numero_input = TextInput(hint_text='Ex: 70123456', size_hint_y=None, height=35, multiline=False)
        main_layout.add_widget(self.numero_input)
        
        main_layout.add_widget(Label(text='CNIB:', size_hint_y=None, height=25))
        self.cnib_input = TextInput(hint_text='Numero CNIB', size_hint_y=None, height=35, multiline=False)
        main_layout.add_widget(self.cnib_input)
        
        main_layout.add_widget(Label(text='Reseau:', size_hint_y=None, height=25))
        self.reseau_spinner = Spinner(text='Choisir reseau', values=['Orange', 'Moov', 'Telecel'], 
                                     size_hint_y=None, height=35)
        main_layout.add_widget(self.reseau_spinner)
        
        main_layout.add_widget(Label(text='Operation:', size_hint_y=None, height=25))
        self.operation_spinner = Spinner(text='Choisir operation', values=['Retrait', 'Depot', 'Unite'], 
                                        size_hint_y=None, height=35)
        main_layout.add_widget(self.operation_spinner)
        
        main_layout.add_widget(Label(text='Montant:', size_hint_y=None, height=25))
        self.montant_input = TextInput(hint_text='Ex: 5000', size_hint_y=None, height=35, multiline=False)
        main_layout.add_widget(self.montant_input)
        
        # Message de confirmation
        self.confirmation_label = Label(text='', size_hint_y=None, height=30)
        main_layout.add_widget(self.confirmation_label)
        
        # Boutons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        retour_btn = Button(text='RETOUR')
        retour_btn.background_color = [0.6, 0.6, 0.6, 1]  # Gris
        retour_btn.bind(on_press=self.retour_menu)
        btn_layout.add_widget(retour_btn)
        
        save_btn = Button(text='ENREGISTRER')
        save_btn.background_color = [0.2, 0.7, 0.2, 1]  # Vert
        save_btn.bind(on_press=self.enregistrer)
        btn_layout.add_widget(save_btn)
        
        main_layout.add_widget(btn_layout)
        
        self.add_widget(main_layout)
    
    def enregistrer(self, instance):
        """Enregistre une nouvelle opération"""
        # Récupération des données
        nom = self.nom_input.text.strip().upper()
        prenom = self.prenom_input.text.strip().title()
        numero = self.numero_input.text.strip()
        cnib = self.cnib_input.text.strip()
        reseau = self.reseau_spinner.text
        montant = self.montant_input.text.strip()
        operation = self.operation_spinner.text
        
        # Validation
        if not all([nom, prenom, numero, cnib]) or not montant.strip():
            self.confirmation_label.text = "Veuillez remplir tous les champs"
            self.confirmation_label.color = [1, 0, 0, 1]
            return
        
        if reseau in ['Choisir reseau'] or operation in ['Choisir operation']:
            self.confirmation_label.text = "Veuillez selectionner reseau et operation"
            self.confirmation_label.color = [1, 0, 0, 1]
            return
        
        try:
            montant_float = float(montant)
            if montant_float <= 0:
                self.confirmation_label.text = "Le montant doit etre positif"
                self.confirmation_label.color = [1, 0, 0, 1]
                return
        except ValueError:
            self.confirmation_label.text = "Montant invalide"
            self.confirmation_label.color = [1, 0, 0, 1]
            return
        
        # Enregistrement
        try:
            DatabaseManager.save_operation(nom, prenom, numero, cnib, reseau, montant_float, operation)
            self.confirmation_label.text = "Operation enregistree avec succes"
            self.confirmation_label.color = [0, 1, 0, 1]
            self.reinitialiser_champs()
        except Exception as e:
            self.confirmation_label.text = f"Erreur: {str(e)}"
            self.confirmation_label.color = [1, 0, 0, 1]
    
    def reinitialiser_champs(self):
        """Réinitialise tous les champs"""
        self.nom_input.text = ""
        self.prenom_input.text = ""
        self.numero_input.text = ""
        self.cnib_input.text = ""
        self.reseau_spinner.text = "Choisir reseau"
        self.montant_input.text = ""
        self.operation_spinner.text = "Choisir operation"
    
    def retour_menu(self, instance):
        """Retourne au menu principal"""
        self.manager.current = "menu"

class StatsScreen(Screen):
    """Écran des statistiques"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Construit l'interface des statistiques"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Titre
        title = Label(text='STATISTIQUES', font_size='24sp', size_hint_y=None, height=50)
        title.color = [1, 0.5, 0, 1]  # Orange
        main_layout.add_widget(title)
        
        # Bouton actualiser
        refresh_btn = Button(text='ACTUALISER', size_hint_y=None, height=40)
        refresh_btn.background_color = [0.2, 0.5, 0.8, 1]  # Bleu
        refresh_btn.bind(on_press=self.afficher_stats)
        main_layout.add_widget(refresh_btn)
        
        # Zone d'affichage
        self.stats_label = Label(text='Cliquez sur ACTUALISER pour voir les statistiques', 
                                text_size=(None, None), valign='top')
        main_layout.add_widget(self.stats_label)
        
        # Bouton retour
        retour_btn = Button(text='RETOUR AU MENU', size_hint_y=None, height=40)
        retour_btn.background_color = [0.6, 0.6, 0.6, 1]  # Gris
        retour_btn.bind(on_press=self.retour_menu)
        main_layout.add_widget(retour_btn)
        
        self.add_widget(main_layout)
    
    def afficher_stats(self, instance):
        """Affiche les statistiques"""
        try:
            stats = DatabaseManager.get_statistics()
            
            if not stats:
                self.stats_label.text = "Aucune donnee disponible"
                return
            
            # Formatage des statistiques
            affichage = "STATISTIQUES DES OPERATIONS\n"
            affichage += "=" * 30 + "\n\n"
            
            total_operations = 0
            total_montant = 0
            
            for reseau, operation, count, montant in stats:
                affichage += f"{reseau} - {operation}:\n"
                affichage += f"  Nombre: {count} operations\n"
                affichage += f"  Montant: {montant:,.0f} FCFA\n\n"
                total_operations += count
                total_montant += montant
            
            affichage += "=" * 30 + "\n"
            affichage += f"TOTAL: {total_operations} operations\n"
            affichage += f"MONTANT TOTAL: {total_montant:,.0f} FCFA"
            
            self.stats_label.text = affichage
            
        except Exception as e:
            self.stats_label.text = f"Erreur: {str(e)}"
    
    def retour_menu(self, instance):
        """Retourne au menu principal"""
        self.manager.current = "menu"

# =============================================================================
# APPLICATION PRINCIPALE
# =============================================================================

class OrangeApp(App):
    """Application principale Orange Money"""
    
    def build(self):
        """Construit l'application"""
        # Initialiser la base de données
        DatabaseManager.init_database()
        
        # Créer le gestionnaire d'écrans
        sm = ScreenManager()
        
        # Ajouter les écrans
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SaisieScreen(name='saisie'))
        sm.add_widget(StatsScreen(name='stats'))
        
        return sm

if __name__ == "__main__":
    OrangeApp().run()