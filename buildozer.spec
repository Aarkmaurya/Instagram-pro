[app]
title = Instagram Pro V4
package.name = instav4_tracker
package.domain = com.aark.v4
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.4

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Requirements
requirements = python3, kivy==2.3.0, requests, urllib3, charset-normalizer, idna, certifi, pyjnius

# 🚩 VERSION LOCK (Error Fix Karne Ke Liye)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.0
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.enable_androidx = True

icon.filename = %(source.dir)s/icon.png
orientation = portrait
p4a.branch = master
