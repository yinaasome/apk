[app]

# Nom de l'application
title = MobileMoney

# Nom du package interne (doit être unique sur un téléphone)
package.name = mobilemoney
package.domain = org.example

# Répertoire source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Fichier principal (renomme apk3.py en main.py)
main.py = main.py

# Version de l'appli
version = 1.0

# Orientation (portrait ou landscape)
orientation = portrait

# Utilisation plein écran
fullscreen = 1

# Modules requis
requirements = python3,kivy,matplotlib,numpy,pandas,plyer,openssl

# Permissions Android (important pour accès fichiers)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Architecture Android supportée
android.archs = armeabi-v7a, arm64-v8a

# API Android cible (31 recommandé)
android.api = 31
android.minapi = 21
android.ndk = 23b
android.ndk_api = 21

# Répertoires/ressources à inclure dans l'APK
android.add_assets = assets/

# Désactiver le log de touches clavier dans logcat
log_level = 2

# Pour autoriser le stockage interne
android.private_storage = True

# Activer le support multi-processeur
android.enable_multiprocessing = True

# Icône de l’application (facultatif)
# icon.filename = %(source.dir)s/icon.png

# Splashscreen facultatif
# presplash.filename = %(source.dir)s/presplash.png

# Pour activer les logs dans Android Logcat
# android.logcat_filters = *:S python:D

# Répertoire de sortie de l’APK
dist_name = mobilemoney

[buildozer]
# Ne pas utiliser root
warn_on_root = 1
log_level = 2
