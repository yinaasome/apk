[app]

title = MobileMoney
package.name = mobilemoney
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,matplotlib,numpy,pandas,plyer,openssl
orientation = portrait
fullscreen = 1

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Icone
icon.filename = %(source.dir)s/icon.png

# Éviter les erreurs matplotlib
android.meta_data = android.webkit.WebView.EnableSafeBrowsing=false

# Inclure les fichiers CSV/DB si besoin
android.presplash = %(source.dir)s/presplash.png
android.add_assets = assets/

# Pour sqlite et SSL
android.api = 31
android.minapi = 21
android.ndk = 23b
android.ndk_api = 21
android.private_storage = True

# Autoriser le multitouch (utile pour les apps Kivy)
android.enable_multiprocessing = True

# Arch support
android.archs = armeabi-v7a,arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
