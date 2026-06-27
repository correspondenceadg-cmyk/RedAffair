[app]
title = Red Affair
package.name = redaffair
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,ttf,wav
version = 0.1
requirements = python3,kivy
orientation = all
icon.filename=%(source.dir)s/RAlogos.png
osx.python_version = 3
osx.kivy_version = 2.3.0
fullscreen = 0
log_level = 2
warn_on_root = 1

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 30
android.arch = arm64-v8a
android.accept_sdk_license = True
android.build_tools_version = 34.0.0
android.allow_backup = True
android.permissions = INTERNET

android.release_artifact = aab
android.sign = 0

[buildozer]
log_level = 2
