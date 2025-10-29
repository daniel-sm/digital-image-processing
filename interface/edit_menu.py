from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class EditMenu(QMenu):
    def __init__(self, parent):
        super().__init__("Edit", parent)

        self.addAction(QAction("Undo", self))
        self.addAction(QAction("Redo", self))
        self.addSeparator()
        self.addAction(QAction("Cut", self))
        self.addAction(QAction("Copy", self))
        self.addAction(QAction("Paste", self))
