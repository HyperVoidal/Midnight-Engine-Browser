import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from urllib.parse import urlparse
from pathlib import Path

engines = {
    "ecosia": "https://www.ecosia.org/search?q=",
    "google": "https://www.google.com/search?q=",
    "brave": "https://search.brave.com/search?q=",
    "duckduckgo": "https://duckduckgo.com/?q="
}

#change this to change search browser for normal text entry. MAKE A DROPDOWN TO CHANGE THIS LATER
engine = engines['brave']

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
        home_btn.triggered.connect(lambda: self.browser.setUrl(QUrl(engine)))
        nav_bar.addAction(home_btn)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
