import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QTabWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        layout = QVBoxLayout()
        self.label = QLabel("happyOS web browser")
        self.label2 = QLabel("ver: PRE DEV NOT FOR FULL USE 0.0.2")
        self.label3 = QLabel("copyright by happyplay.inc 2020 - 2026")
        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        self.setLayout(layout)

# soo will be adding settings inteal now enjoy using it
class Settingswindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setings")
    
class BrowserTab(QWidget):
    def __init__(self, url="http://google.com"):
        super().__init__()
        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(30)

        self.go_btn = QPushButton("explore")
        self.go_btn.setMaximumHeight(30)
        self.back_btn = QPushButton("<-")
        self.back_btn.setMaximumHeight(30)
        self.forward_btn = QPushButton("->")
        self.forward_btn.setMaximumHeight(30)

        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)

        self.browser = QWebEngineView()

        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.toPlainText().strip()))
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.titleChanged.connect(self.update_title)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)
        self.browser.setUrl(QUrl(url))

        self.title_changed_callback = None  # will be set by main window

    def navigate(self, url):
        url = url.strip()
        if url == "about":
            self.show_about_window()
            return
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, url):
        self.url_bar.setText(url.toString())

    def update_title(self, title):
        if self.title_changed_callback:
            self.title_changed_callback(self, title)

    def show_about_window(self):
        self.about = AboutWindow()
        self.about.show()


class happyOSmainwebbrowserwindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(happyOSmainwebbrowserwindow, self).__init__(*args, **kwargs)
        self.window = QWidget()
        self.window.setWindowTitle("HappyOS web browser predev")
        self.main_layout = QVBoxLayout()

        # Tab bar buttons
        self.tab_bar_layout = QHBoxLayout()
        self.new_tab_btn = QPushButton("+ New Tab")
        self.new_tab_btn.setMaximumWidth(100)
        self.new_tab_btn.clicked.connect(self.add_tab)
        self.tab_bar_layout.addWidget(self.new_tab_btn)
        self.tab_bar_layout.addStretch()

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.main_layout.addLayout(self.tab_bar_layout)
        self.main_layout.addWidget(self.tabs)

        self.window.setLayout(self.main_layout)

        # Open first tab
        self.add_tab()

        self.window.show()

    def add_tab(self, url=None):
        if url is None or isinstance(url, bool):  # ignore the bool from clicked signal
            url = "http://google.com"
        tab = BrowserTab(url)
        tab.title_changed_callback = self.update_tab_title
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:          # keep at least 1 tab open
            self.tabs.removeTab(index)
        else:
            self.window.close()             # close app if last tab is closed

    def update_tab_title(self, tab, title):
        index = self.tabs.indexOf(tab)
        if index != -1:
            short_title = title[:20] + "..." if len(title) > 20 else title
            self.tabs.setTabText(index, short_title)


app = QApplication(sys.argv)
window = happyOSmainwebbrowserwindow()
app.exec_()