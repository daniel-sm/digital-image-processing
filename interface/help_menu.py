from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class HelpMenu(QMenu):
    def __init__(self, parent):
        super().__init__("Help", parent)

        self.addAction(QAction("Documentation", self))
        self.addAction(QAction("About", self))
