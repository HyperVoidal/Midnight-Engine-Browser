import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QToolButton, QMenu, QWidget, QHBoxLayout, QLabel, QWidgetAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from urllib.parse import urlparse
from pathlib import Path
import urllib.request
import os

engines = {
    "ecosia": ("https://www.ecosia.org/search?q=", "https://www.ecosia.org/favicon.ico"),
    "google": ("https://www.google.com/search?q=", "https://www.google.com/favicon.ico"),
    "brave": ("https://search.brave.com/search?q=", "https://brave.com/favicon.ico"),
    "duckduckgo": ("https://duckduckgo.com/search?q=", "https://duckduckgo.com/favicon.ico")
}

#Icon cache 
icon_cache_dir = Path(__file__).parent / "icon_cache"
icon_cache_dir.mkdir(exist_ok=True)

#pull icons and insert into cache
def get_favicon(engine_name, favicon_url):
    """Download and cache favicon, return QIcon"""
    icon_path = icon_cache_dir / f"{engine_name}.ico"
    
    # Download icon if not cached
    if not icon_path.exists():
        try:
            urllib.request.urlretrieve(favicon_url, icon_path)
        except:
            return QIcon()  # Return empty icon if download fails
            
    return QIcon(str(icon_path))

#change this to change search browser for normal text entry. MAKE A DROPDOWN TO CHANGE THIS LATER
engine = engines['duckduckgo'][0]

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Browser")
        self.resize(1200, 800)


        self.browser = QWebEngineView()
        home_path = Path(__file__).parent / "homepage.html"
        self.browser.setUrl(QUrl.fromLocalFile(str(home_path)))
        self.setCentralWidget(self.browser)


        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)


        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)


        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)


        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)


        home_btn = QAction("Home", self)
        home_btn.triggered.connect(lambda: self.browser.setUrl(QUrl(engine[:-9])))
        nav_bar.addAction(home_btn)


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

        self.engine_btn.clicked.connect(lambda: self.browser.setUrl(QUrl(self.engine.split('/search?q=')[0])))

        self.engine_btn.setPopupMode(QToolButton.MenuButtonPopup)
        nav_bar.addWidget(self.engine_btn)
        self.set_engine([k for k,v in engines.items() if v[0]==self.engine][0], self.engine)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        nav_bar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()))



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
        
        self.browser.setUrl(QUrl(fullurl))
    
    def set_engine(self, key, value):
        global engine
        self.engine = value
        engine = value
        self.engine_btn.setText(key.capitalize())
        self.engine_btn.setToolTip(value)
        self.engine_btn.setIcon(get_favicon(key, engines[key][1]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
