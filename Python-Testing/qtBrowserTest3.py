import sys
from PySide6.QtCore import QUrl 
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import *
from PySide6.QtGui import *
from urllib.parse import urlparse
from pathlib import Path
import urllib.request
import os
from PIL import Image, ImageOps
import json


#Icon cache 
icon_cache_dir = Path(__file__).parent / "icon_cache"
icon_cache_dir.mkdir(exist_ok=True)

inv = True

#pull icons and insert into cache
def get_favicon(name, favicon_url):
    """Download and cache favicon, return QIcon"""
    icon_path = icon_cache_dir / f"{name}.ico"
    
    # Download icon if not cached
    if not icon_path.exists():
        try:
            urllib.request.urlretrieve(favicon_url, icon_path)
        except:
            return QIcon()  # Return empty icon if download fails
            
    return QIcon(str(icon_path))

def get_normIcon(name, inv):
    if inv == True:
        icon_path = icon_cache_dir / f"inv_{name}.ico"
    else:
        icon_path = icon_cache_dir / f"{name}.ico"

    return QIcon(str(icon_path))

engines = {
    "ecosia": ("https://www.ecosia.org/search?q=", "https://www.ecosia.org/favicon.ico"),
    "google": ("https://www.google.com/search?q=", "https://www.google.com/favicon.ico"),
    "brave": ("https://search.brave.com/search?q=", "https://brave.com/favicon.ico"),
    "duckduckgo": ("https://duckduckgo.com/search?q=", "https://duckduckgo.com/favicon.ico")
}

#starter engine
engine = engines['brave'][0]

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Midnight Engine")
        self.resize(1200, 800)
        self.url_bar = QLineEdit()

        home_path = Path(__file__).parent / "homepage.html"
        self.tabs  = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.switch_tab)
        self.setCentralWidget(self.tabs)
        self.add_new_tab(QUrl.fromLocalFile(str(home_path)), "Home")

        self.nav_bar = QToolBar("Navigation")
        self.addToolBar(self.nav_bar)
        self.nav_bar.setMovable(False)
        self.nav_bar.setStyleSheet("background:rgb(1, 1, 100)")

        #buttons
        self.back_btn = QToolButton(self)
        self.back_btn.setToolTip("Back")
        self.nav_bar.addWidget(self.back_btn)

        self.reload_btn = QToolButton(self)
        self.reload_btn.setToolTip("Reload")
        self.nav_bar.addWidget(self.reload_btn)

        self.forward_btn = QToolButton(self)
        self.forward_btn.setToolTip("Forward")
        self.nav_bar.addWidget(self.forward_btn)

        self.home_btn = QToolButton(self)
        self.home_btn.setToolTip("Home")
        self.nav_bar.addWidget(self.home_btn)

        self.newtab_btn = QToolButton(self)
        self.newtab_btn.setToolTip("NewTab")
        self.nav_bar.addWidget(self.newtab_btn)

        self.colourtheme_btn = QToolButton(self)
        self.colourtheme_btn.setToolTip("ColourTheme")
        self.nav_bar.addWidget(self.colourtheme_btn)

        self.engine = engine
        self.engine_btn = QToolButton(self)
        self.engine_btn.setText("Search With...")
        menu = QMenu(self)

        for key, (search_url, favicon_url) in engines.items():
            # Create widget for menu item
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(5, 2, 5, 2)
            layout.setSpacing(5)
            
            # Add icon
            icon_label = QLabel()
            icon = get_favicon(key, favicon_url)
            icon_label.setPixmap(icon.pixmap(16, 16))
            layout.addWidget(icon_label)
            
            # Add text
            text_label = QLabel(key.capitalize())
            layout.addWidget(text_label)
            
            # Create QWidgetAction and set the custom widget
            widget_action = QWidgetAction(self)
            widget_action.setDefaultWidget(widget)
            widget_action.setData((key, search_url))
            widget_action.triggered.connect(lambda checked, v=search_url, k=key: self.set_engine(k, v))
            menu.addAction(widget_action)
            
        self.engine_btn.setMenu(menu)

        initial_engine = [k for k,v in engines.items() if v[0]==self.engine][0]
        self.engine_btn.setIcon(get_favicon(initial_engine, engines[initial_engine][1]))

        self.engine_btn.clicked.connect(lambda: self.current_browser.setUrl(QUrl(self.engine.split('/search?q=')[0])))

        self.engine_btn.setPopupMode(QToolButton.MenuButtonPopup)
        self.nav_bar.addWidget(self.engine_btn)


        self.set_engine([k for k,v in engines.items() if v[0]==self.engine][0], self.engine)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.nav_bar.addWidget(self.url_bar)

        self.current_browser.urlChanged.connect((lambda q: self.url_bar.setText(q.toString())))


    def rotate_reload_icon(self):
        """Rotate the reload icon continuously"""
        self.rotation_angle = (self.rotation_angle + 10) % 360
        base_icon = get_normIcon("reload", inv)
        pixmap = base_icon.pixmap(24, 24)
        
        transform = QTransform().rotate(self.rotation_angle)
        rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.reload_btn.setIcon(QIcon(rotated_pixmap))
    
    def start_reload_animation(self):
        if not self.rotation_timer.isActive():
            self.rotation_timer.start(0.01)  # adjust speed here (ms per frame)
    
    def stop_reload_animation(self):
        if self.rotation_timer.isActive():
            self.rotation_timer.stop()
        # reset icon to upright
        self.rotation_angle = 0
        self.reload_btn.setIcon(get_normIcon("reload", inv))

    def current_browser(self):
        return self.tabs.currentWidget()

    def add_new_tab(self, qurl=engine, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")
        
        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setStyleSheet("QTabBar::tab { height: 30px; width: 150px;}")
        self.tabs.setCurrentIndex(i)

        # Connect signals
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_tab_title(browser))
        browser.loadStarted.connect(self.start_reload_animation)
        browser.loadFinished.connect(lambda ok, b=browser: (self.stop_reload_animation(), self.on_load_finished()))
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser, title))

        
        if qurl.toString().endswith("homepage.html"):
            self.url_bar.setText("")
        return browser
    
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()  # Exit if last tab closed

    def switch_tab(self, index):
        current_browser = self.tabs.widget(index)
        if current_browser:
            self.current_browser = current_browser
            self.url_bar.setText(current_browser.url().toString())

    def update_tab_title(self, browser, title=None):
        i = self.tabs.indexOf(browser)
        if i != -1:
            # Use provided title or fallback
            if not title:
                title = browser.url().toString()

            # Clean it up a bit for display
            if len(title) > 60:
                title = title[:57] + "..."
            
            if title == 'homepage.html':
                title = 'Home'

            self.tabs.setTabText(i, title)

    def load_url(self):
        url = self.url_bar.text()
        urlparsed = urlparse(url)
        if urlparsed.scheme and urlparsed.netloc:
            print(urlparsed)
            fullurl = url
            pass
        else:
            wordlist = url.split(" ")
            joiner = "+"
            texturlcomp = joiner.join(wordlist)
            fullurl = engine + texturlcomp
            print(fullurl)
        
        self.current_browser.setUrl(QUrl(fullurl))
    
    def set_engine(self, key, value):
        global engine
        self.engine = value
        engine = value
        self.engine_btn.setText(key.capitalize())
        self.engine_btn.setToolTip(value)
        self.engine_btn.setIcon(get_favicon(key, engines[key][1]))
    
if __name__ == "__main__":#
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
