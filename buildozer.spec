[app]

# Titre de l'application
title = Orange Money

# Nom du package (doit être unique)
package.name = orange.money

# Nom du domaine (inverse du package.name)
package.domain = org.orange

# Version de l'application (format: 1.0.0)
version = 1.0.0

# Numéro de version (doit être incrémenté à chaque mise à jour)
version.regex = __version__ = '(.*)'
version.filename = %(source.dir)s/main.py

# Chemin vers l'application principale
source.dir = .

# Fichier principal de l'application
source.include_exts = py,png,jpg,kv,atlas,ttf

# Version de Python à utiliser
requirements = python3,kivy,sqlite3

# Configuration Android
android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 33
android.arch = arm64-v8a