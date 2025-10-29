from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class FilterMenu(QMenu):
    def __init__(self, parent, filter_controller):
        super().__init__("Filters", parent)

        negative_action = QAction("Negative", self)
        negative_action.triggered.connect(filter_controller.apply_negative)
        self.addAction(negative_action)

        sepia_action = QAction("Sepia", self)
        sepia_action.triggered.connect(filter_controller.apply_sepia)
        self.addAction(sepia_action)
