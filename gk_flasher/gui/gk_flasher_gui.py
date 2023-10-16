import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu
from PySide6.QtGui import QAction

class GKFlasherMainWindow(QMainWindow):

    menu_bar: QMenuBar

    def __init__(self):
        super().__init__()

        # Create the menubar
        self.create_menu_bar()
       
        self.setWindowTitle("GK Flasher")
        self.resize(800, 600)

    def create_menu_bar(self):
        self.menu_bar = QMenuBar(self)

        # Create the "File" menu and add some actions to it
        file_menu = QMenu("File", self.menu_bar)
        open_action = QAction("Open GK Package", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addActions([open_action, exit_action])

        # Create the "Tools" menu and add some actions to it
        tools_menu = QMenu("Tools", self.menu_bar)
        settings_action = QAction("Settings", self)
        tools_menu.addAction(settings_action)

        # Create the "Help" menu and add some actions to it
        help_menu = QMenu("Help", self.menu_bar)
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        # Add the menus to the menubar
        self.menu_bar.addMenu(file_menu)
        self.menu_bar.addMenu(tools_menu)
        self.menu_bar.addMenu(help_menu)

        # Set the menubar to the main window
        self.setMenuBar(self.menu_bar)


def run_gui():
    app = QApplication(sys.argv)
    window = GKFlasherMainWindow()
    window.show()
    sys.exit(app.exec())
