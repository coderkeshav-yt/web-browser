import sys
import qtawesome as qta
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction,
                             QLineEdit, QTabWidget, QStatusBar, QProgressBar,
                             QMenu)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings

# --- Custom Stylesheet (QSS) for a Modern Dark Theme ---
DARK_STYLESHEET = """
QWidget {
    background-color: #2e2e2e;
    color: #e0e0e0;
    font-family: Arial, sans-serif;
}
QMainWindow::separator {
    background-color: #444;
    width: 1px;
    height: 1px;
}
QToolBar {
    background-color: #383838;
    border: none;
    padding: 5px;
}
QToolBar QToolButton {
    background-color: #383838;
    padding: 6px;
    border-radius: 4px;
}
QToolBar QToolButton:hover {
    background-color: #555;
}
QToolBar QToolButton:pressed {
    background-color: #666;
}
QLineEdit {
    background-color: #444;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 5px;
    color: #e0e0e0;
}
QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    background: #383838;
    color: #e0e0e0;
    padding: 8px 15px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #2e2e2e;
}
QTabBar::tab:!selected:hover {
    background: #555;
}
QTabBar::close-button {
    image: url(close.png); /* You might need to provide a close icon */
    subcontrol-position: right;
}
QStatusBar {
    background-color: #383838;
    color: #e0e0e0;
}
QProgressBar {
    border: 1px solid #555;
    border-radius: 4px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #007acc;
    border-radius: 4px;
}
QMenu {
    background-color: #383838;
    border: 1px solid #555;
}
QMenu::item:selected {
    background-color: #007acc;
}
"""

class ProBrowserWindow(QMainWindow):
    def __init__(self):
        super(ProBrowserWindow, self).__init__()

        self.setWindowTitle("python web browser by keshav singh") # <-- MODIFIED LINE
        self.setWindowIcon(qta.icon('fa5s.rocket', color='#007acc'))

        # --- Tabs ---
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        
        # --- Status & Progress Bar ---
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximumWidth(150)
        self.status.addPermanentWidget(self.progress_bar)

        # --- Toolbar ---
        navbar = QToolBar("Navigation")
        navbar.setIconSize(QSize(20, 20))
        self.addToolBar(navbar)

        # --- Actions using qtawesome icons ---
        self.back_btn = QAction(qta.icon('fa5s.arrow-left', color='white'), "Back", self)
        self.forward_btn = QAction(qta.icon('fa5s.arrow-right', color='white'), "Forward", self)
        self.reload_btn = QAction(qta.icon('fa5s.redo', color='white'), "Reload", self)
        self.home_btn = QAction(qta.icon('fa5s.home', color='white'), "Home", self)
        self.stop_btn = QAction(qta.icon('fa5s.stop', color='white'), "Stop", self)
        
        self.back_btn.triggered.connect(lambda: self.current_browser().back())
        self.forward_btn.triggered.connect(lambda: self.current_browser().forward())
        self.reload_btn.triggered.connect(lambda: self.current_browser().reload())
        self.home_btn.triggered.connect(self.navigate_home)
        self.stop_btn.triggered.connect(lambda: self.current_browser().stop())
        
        navbar.addAction(self.back_btn)
        navbar.addAction(self.forward_btn)
        navbar.addAction(self.reload_btn)
        navbar.addAction(self.stop_btn)
        navbar.addAction(self.home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # --- Menu Bar ---
        self.setup_menus()

        # --- Add Initial Tab ---
        self.add_new_tab(QUrl("http://www.google.com"), "Homepage")
        self.showMaximized()

    # --- Helper & Slot Functions ---

    def add_new_tab(self, qurl: QUrl, label: str = "New Tab"):
        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        browser.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

        # Enable context menu
        browser.setContextMenuPolicy(Qt.CustomContextMenu)
        browser.customContextMenuRequested.connect(self.page_context_menu)
        
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Connect signals
        browser.urlChanged.connect(lambda q, browser=browser: self.update_urlbar(q, browser))
        browser.loadFinished.connect(lambda _, browser=browser, i=i: self.tabs.setTabText(i, browser.page().title()))
        browser.loadProgress.connect(self.update_progress)
        browser.titleChanged.connect(lambda title, browser=browser: self.update_window_title(title, browser))
        browser.page().profile().downloadRequested.connect(self.handle_download)

    def page_context_menu(self, pos):
        browser = self.sender()
        menu = QMenu()
        
        back_action = menu.addAction("Back")
        forward_action = menu.addAction("Forward")
        reload_action = menu.addAction("Reload")
        menu.addSeparator()
        inspect_action = menu.addAction("Inspect Element")

        back_action.triggered.connect(browser.back)
        forward_action.triggered.connect(browser.forward)
        reload_action.triggered.connect(browser.reload)
        inspect_action.triggered.connect(lambda: browser.page().triggerAction(browser.page().InspectElement))

        menu.exec_(browser.mapToGlobal(pos))
        
    def setup_menus(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        new_tab_action = QAction(qta.icon('fa5s.plus-circle', color='white'), "New Tab", self)
        new_tab_action.triggered.connect(lambda: self.add_new_tab(QUrl("http://www.google.com")))
        file_menu.addAction(new_tab_action)
        
        view_menu = menu_bar.addMenu("&View")
        zoom_in_action = QAction(qta.icon('fa5s.search-plus', color='white'), "Zoom In", self)
        zoom_in_action.triggered.connect(lambda: self.current_browser().setZoomFactor(self.current_browser().zoomFactor() + 0.1))
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction(qta.icon('fa5s.search-minus', color='white'), "Zoom Out", self)
        zoom_out_action.triggered.connect(lambda: self.current_browser().setZoomFactor(self.current_browser().zoomFactor() - 0.1))
        view_menu.addAction(zoom_out_action)

        zoom_reset_action = QAction(qta.icon('fa5s.search', color='white'), "Reset Zoom", self)
        zoom_reset_action.triggered.connect(lambda: self.current_browser().setZoomFactor(1.0))
        view_menu.addAction(zoom_reset_action)
        
    def handle_download(self, download):
        print(f"Downloading: {download.url().toDisplayString()}")
        print(f"Save to: {download.path()}")
        download.accept()
        download.finished.connect(lambda: print("Download finished."))

    def tab_open_doubleclick(self, i):
        if i == -1: # Double-click on empty tab space
            self.add_new_tab(QUrl("http://www.google.com"))

    def current_tab_changed(self, i):
        browser = self.current_browser()
        self.update_urlbar(browser.url(), browser)
        self.update_window_title(browser.page().title(), browser)

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            self.close()
        else:
            self.tabs.removeTab(i)

    def current_browser(self) -> QWebEngineView:
        return self.tabs.currentWidget()

    def update_progress(self, p):
        self.progress_bar.setValue(p)
        self.progress_bar.setVisible(p > 0 and p < 100)

    def update_window_title(self, title, browser):
        if browser != self.current_browser():
            return
        self.setWindowTitle(f"{title} - python web browser by keshav singh") # <-- MODIFIED LINE

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        text = self.url_bar.text()
        if '.' not in text:
            # Assume it's a search query
            url = "https://www.google.com/search?q=" + text.replace(" ", "+")
            self.current_browser().setUrl(QUrl(url))
        else:
            # Assume it's a URL
            q = QUrl.fromUserInput(text)
            if q.scheme() == "":
                q.setScheme("http")
            self.current_browser().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.current_browser():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

# --- Main Execution ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLESHEET)
    window = ProBrowserWindow()
    sys.exit(app.exec_())