from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class SteganographyMenu(QMenu):
    def __init__(self, parent, steganography_controller):
        super().__init__("Steganography", parent)

        write = QAction("Write", self)
        write.triggered.connect(steganography_controller.write_message)
        self.addAction(write)

        read = QAction("Read", self)
        read.triggered.connect(steganography_controller.read_message)
        self.addAction(read)
