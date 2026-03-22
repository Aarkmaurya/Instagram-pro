[app]
title = Instagram Pro
package.name = insta_tracker_v4
package.domain = com.aarkmaurya.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.4

# Permissions (Zaroori hain!)
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE

# Requirements (WebView ke liye jnius aur requests zaroori hain)
requirements = python3, kivy==2.3.0, requests, urllib3, charset-normalizer, idna, certifi, pyjnius

orientation = portrait
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# WebView Settings
android.enable_androidx = True
p4a.branch = master

