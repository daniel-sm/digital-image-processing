from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class ColorMenu(QMenu):
    def __init__(self, parent, color_controller):
        super().__init__("Color", parent)

        adjust_hsv = QAction("Adjust HSV", self)
        adjust_hsv.triggered.connect(color_controller.open_adjust_hsv_panel)
        self.addAction(adjust_hsv)

        adjust_hsi = QAction("Adjust HSI", self)
        adjust_hsi.triggered.connect(color_controller.open_adjust_hsi_panel)
        self.addAction(adjust_hsi)

        adjust_rgb = QAction("Adjust RGB", self)
        adjust_rgb.triggered.connect(color_controller.open_adjust_rgb_panel)
        self.addAction(adjust_rgb)

        self.addSeparator()

        # Submenu de tons de cinza
        grayscale_menu = self.addMenu("Grayscale")

        gray_simple = QAction("Simple Mean", self)
        gray_simple.triggered.connect(color_controller.convert_to_grayscale_simple_mean)
        grayscale_menu.addAction(gray_simple)

        gray_weighted = QAction("Weighted Mean", self)
        gray_weighted.triggered.connect(color_controller.convert_to_grayscale_weighted_mean)
        grayscale_menu.addAction(gray_weighted)
