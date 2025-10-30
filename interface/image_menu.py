from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class ImageMenu(QMenu):
    def __init__(self, parent, image_controller):
        super().__init__("Image", parent)

        brightness = QAction("Brightness", self)
        brightness.triggered.connect(image_controller.open_brightness_panel)
        self.addAction(brightness)

        contrast = QAction("Contrast", self)
        contrast.triggered.connect(image_controller.apply_contrast)
        self.addAction(contrast)

        self.addSeparator()

        threshold = QAction("Threshold", self)
        threshold.triggered.connect(image_controller.open_threshold_panel)
        self.addAction(threshold)

        log = QAction("Logarithmic", self)
        log.triggered.connect(image_controller.open_log_panel)
        self.addAction(log)

        gamma = QAction("Gamma Correction", self)
        gamma.triggered.connect(image_controller.open_gamma_panel)
        self.addAction(gamma)

        self.addSeparator()

        functions_menu = self.addMenu("Functions Transformations")

        intensity_level = QAction("Intensity Level Slicing", self)
        intensity_level.triggered.connect(image_controller.open_intensity_level_panel)
        functions_menu.addAction(intensity_level)

        piecewise_linear = QAction("Piecewise Linear", self)
        piecewise_linear.triggered.connect(image_controller.open_piecewise_linear_panel)
        functions_menu.addAction(piecewise_linear)

        filters_menu = self.addMenu("Filters")

        negative = QAction("Negative", self)
        negative.triggered.connect(image_controller.apply_negative)
        filters_menu.addAction(negative)

        sepia = QAction("Sepia", self)
        sepia.triggered.connect(image_controller.apply_sepia)
        filters_menu.addAction(sepia)
