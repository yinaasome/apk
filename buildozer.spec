[app]
title = Orange Money
package.name = orange.money
package.domain = org.orange

# Configuration de version (utilise soit version.soit version.regex)
version.regex = __version__ = '(.*)'
version.filename = %(source.dir)s/main.py

# Chemins et inclusions
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

# Requirements
requirements = python3,kivy,sqlite3

# Configuration Android
android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 33
android.arch = arm64-v8a
