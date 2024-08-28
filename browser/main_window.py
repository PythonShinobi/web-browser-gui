from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWidgets import (
    QAction,    
    QDialog,        
    QLabel,
    QLineEdit,
    QMainWindow,
    QTabWidget,
    QToolBar,    
)

from paths import Paths
from dialogs.about_dialog import AboutDialog
from .file_operations import open_file, save_file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1024, 768)

        self.tabs = QTabWidget()  # Create a tabbed interface in your application.
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        navigation_bar = QToolBar('Navigation')
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)

        # Back button
        back_btn = QAction(
            QIcon(Paths.icon("arrow-180.png")), "Back", self
        )
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(
            lambda: self.tabs.currentWidget().back()
        )
        navigation_bar.addAction(back_btn)

        # Next button
        next_btn = QAction(
            QIcon(Paths.icon("arrow-000.png")), "Forward", self
        )
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(
            lambda: self.tabs.currentWidget().forward()
        )
        navigation_bar.addAction(next_btn)

        # Reload button
        reload_btn = QAction(
            QIcon(Paths.icon("arrow-circle-315.png")),
            "Reload",
            self,
        )
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(
            lambda: self.tabs.currentWidget().reload()
        )
        navigation_bar.addAction(reload_btn)

        # Home button
        home_btn = QAction(QIcon(Paths.icon("home.png")), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navigation_bar.addAction(home_btn)

        navigation_bar.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(Paths.icon("lock-nossl.png")))
        navigation_bar.addWidget(self.httpsicon)

        # Url bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addWidget(self.urlbar)

        # Stop button
        stop_btn = QAction(
            QIcon(Paths.icon("cross-circle.png")), "Stop", self
        )
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(
            lambda: self.tabs.currentWidget().stop()
        )
        navigation_bar.addAction(stop_btn)

        self.menuBar().setNativeMenuBar(False)
        self.statusBar()

        file_menu = self.menuBar().addMenu("&File")
        new_tab_action = QAction(
            QIcon(Paths.icon("ui-tab--plus.png")),
            "New Tab",
            self,
        )
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(
            QIcon(Paths.icon("disk--arrow.png")),
            "Open file...",
            self,
        )
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(
            QIcon(Paths.icon("disk--pencil.png")),
            "Save Page As...",
            self,
        )
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(
            QIcon(Paths.icon("printer.png")), "Print...", self
        )
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        # Create our system printer instance.
        self.printer = QPrinter()

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(
            QIcon(Paths.icon("question.png")),
            "About Mozzarella Ashbadger",
            self,
        )
        about_action.setStatusTip(
            "Find out more about Mozzarella Ashbadger"
        )
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_mozarella_action = QAction(
            QIcon(Paths.icon("lifebuoy.png")),
            "Mozzarella Ashbadger Homepage",
            self,
        )
        navigate_mozarella_action.setStatusTip(
            "Go to Mozzarella Ashbadger Homepage"
        )
        navigate_mozarella_action.triggered.connect(
            self.navigate_mozarella
        )
        help_menu.addAction(navigate_mozarella_action)

        self.add_new_tab(QUrl("http://www.google.com"), "Homepage")

        self.show()

        self.setCentralWidget(self.tabs)
        self.setWindowTitle("Mozzarella Ashbadger")
        self.setWindowIcon(QIcon(Paths.icon("ma-icon-64.png")))

    def add_new_tab(self, url=None, label='https://www.google.com'):
        if url is None:
            url = QUrl('')  # Handle and manipulate urls.

        tab = QWebEngineView()  #  Enables you to integrate web content into PyQt5 applications.
        tab.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        tab.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        tab.setUrl(url)

        i = self.tabs.addTab(tab, label)
        self.tabs.setCurrentIndex(i)

        # Emitted whenever the URL of the `tab` changes.
        tab.urlChanged.connect(
            lambda url, tab=tab: self.update_urlbar(url, tab)
        )

        # Emitted when a page finishes loading in the `tab`.
        tab.loadFinished.connect(
            lambda _, i=i, tab=tab: self.tabs.setTabText(i, tab.page().title())
        )

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    def current_tab_changed(self, i):
        """Handles what happens when the user switches between tabs in a tabbed 
        browser-like application."""
        url = self.tabs.currentWidget().url()  # Get url of the active tab.
        self.update_urlbar(url, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            # Safeguard to ensure that at least one tab remains open.
            return
        
        self.tabs.removeTab(i)

    def update_title(self, tab):
        if tab != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return
        
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(f'{title} - Mozzarella Ashbadger')

    def navigate_mozarella(self):
        url = QUrl("https://academy.pythonguis.com/")
        self.tabs.currentWidget().setUrl(url)

    def about(self):
        dialog = AboutDialog()
        dialog.exec_()

    def open_file(self):
        open_file(self)

    def save_file(self):
        save_file(self)

    def print_page(self):
        page = self.tabs.currentWidget().page()

        def callback(*args):
            pass

        dlg = QPrintDialog(self.printer)
        dlg.accepted.connect(callback)
        if dlg.exec_() == QDialog.Accepted:
            page.print(self.printer, callback)

    def navigate_home(self):
        # Set the active tab to the given url.
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):  # Does not receive the Url
        url = QUrl(self.urlbar.text())
        if url.scheme() == '':
            url.setScheme('http')

        self.tabs.currentWidget().setUrl(url)

    def update_urlbar(self, url, tab=None):
        """Updates the URL bar and related visual indicators in the user interface when the 
        user navigates to a new webpage in the current tab."""
        if tab != self.tabs.currentWidget():
            # Ensures that the URL bar is only updated if the tab passed to the 
            # method is the currently active tab in the QTabWidget
            return
        
        if url.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(
                QPixmap(Paths.icon("lock-ssl.png"))
            )
        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(
                QPixmap(Paths.icon("lock-nossl.png"))
            )

        self.urlbar.setText(url.toString())
        self.urlbar.setCursorPosition(0)