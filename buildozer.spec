[app]
title = Instagram
package.name = insta_v5_pro
package.domain = com.aark.v5
source.dir = .
version = 0.5
requirements = python3, kivy==2.3.0, requests, pyjnius, android
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, CAMERA
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.0
android.accept_sdk_license = True
android.enable_androidx = True
orientation = portrait
fullscreen = 1
icon.filename = %(source.dir)s/icon.png
