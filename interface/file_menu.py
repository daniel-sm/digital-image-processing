from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class FileMenu(QMenu):
    def __init__(self, parent, file_controller):
        super().__init__("File", parent)

        open_action = QAction("Open Image...", self)
        open_action.triggered.connect(file_controller.open_image)
        self.addAction(open_action)

        self.addSeparator()

        reset_action = QAction("Reset Image", self)
        reset_action.triggered.connect(file_controller.reset_image)
        self.addAction(reset_action)

        close_action = QAction("Close Image", self)
        close_action.triggered.connect(file_controller.close_image)
        self.addAction(close_action)

        self.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(file_controller.exit_application)
        self.addAction(exit_action)
