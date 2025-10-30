from PySide6.QtWidgets import QMainWindow, QMessageBox, QLabel, QSlider, QDoubleSpinBox, QPushButton
from PySide6.QtCore import Qt

from core.basic_operations import (
    brightness,
    gamma,
    negative,
    threshold,
    log
)
from core.colored_operations import rgb_contrast, sepia
from core.image_handler import to_byte, to_double
from controller.image_controller import update_image

class ImageMenuController:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window

    def _check_image(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Aviso", "Nenhuma imagem aberta.")
            return False
        return True

    def open_brightness_panel(self):
        if self._check_image() is False:
            return
        
        panel = self.main_window.side_panel
        panel.clear_panel()

        label_multiplier = QLabel("Multiplier:")
        slider_multiplier = QSlider(Qt.Horizontal)
        slider_multiplier.setMinimum(1)
        slider_multiplier.setMaximum(100)
        slider_multiplier.setValue(50)
        slider_multiplier.valueChanged.connect(lambda v: self._apply_brightness(v/50.0))

        panel.add_widget(label_multiplier)
        panel.add_widget(slider_multiplier)

    def _apply_brightness(self, value):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(brightness(img, value))
        update_image(self.main_window, result)

    def apply_contrast(self):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(rgb_contrast(img))
        update_image(self.main_window, result)

    def open_threshold_panel(self):
        if self._check_image() is False:
            return
        
        panel = self.main_window.side_panel
        panel.clear_panel()

        label_threshold = QLabel("Threshold:")
        slider_threshold = QSlider(Qt.Horizontal)
        slider_threshold.setMinimum(0)
        slider_threshold.setMaximum(255)
        slider_threshold.setValue(128)
        slider_threshold.valueChanged.connect(lambda v: self._apply_threshold(v/255.0))

        panel.add_widget(label_threshold)
        panel.add_widget(slider_threshold)

    def _apply_threshold(self, value):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(threshold(img, value))
        update_image(self.main_window, result)  

    def open_log_panel(self):
        if self._check_image() is False:
            return
        panel = self.main_window.side_panel
        panel.clear_panel()

        panel.add_widget(QLabel("Multiplier:"))

        k_input = QDoubleSpinBox()
        k_input.setRange(0.1, 2.0)
        k_input.setSingleStep(0.01)
        k_input.setValue(1.0)
        panel.add_widget(k_input)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self._apply_log(float(k_input.value())))
        panel.add_widget(apply_btn)

    def _apply_log(self, value):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(log(img, value))
        update_image(self.main_window, result)

    def open_gamma_panel(self):
        if self._check_image() is False:
            return
        panel = self.main_window.side_panel
        panel.clear_panel()

        panel.add_widget(QLabel("Lambda:"))
        y_input = QDoubleSpinBox()
        y_input.setRange(0.1, 5.0)
        y_input.setSingleStep(0.05)
        y_input.setValue(1.0)
        panel.add_widget(y_input)

        panel.add_widget(QLabel("Multiplier:"))
        k_input = QDoubleSpinBox()
        k_input.setRange(0.1, 2.0)
        k_input.setSingleStep(0.01)
        k_input.setValue(1.0)
        panel.add_widget(k_input)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self._apply_gamma(
            float(y_input.value()), float(k_input.value())))
        panel.add_widget(apply_btn)

    def _apply_gamma(self, y, c):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(gamma(img, y, c))
        update_image(self.main_window, result)

    def open_intensity_level_panel(self):
        if self._check_image() is False:
            return
        print("Opening Intensity Level Panel")
    
    def open_piecewise_linear_panel(self):
        if self._check_image() is False:
            return
        print("Opening Piecewise Linear Panel")

    def apply_negative(self):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(negative(img))
        update_image(self.main_window, result)

    def apply_sepia(self):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        img_array = to_byte(sepia(img))
        update_image(self.main_window, img_array)

