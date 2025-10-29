from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class GeometricMenu(QMenu):
    def __init__(self, parent, geometric_controller):
        super().__init__("Geometric", parent)

        scale_action = QAction("Scale", self)
        scale_action.triggered.connect(geometric_controller.open_scale_panel)
        self.addAction(scale_action)

        rotate_action = QAction("Rotate", self)
        rotate_action.triggered.connect(geometric_controller.open_rotate_panel)
        self.addAction(rotate_action)
