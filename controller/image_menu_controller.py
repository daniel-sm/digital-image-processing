from PySide6.QtWidgets import QMainWindow, QMessageBox, QLabel, QSlider
from PySide6.QtCore import Qt

from core.basic_operations import brightness, negative
from core.colored_operations import sepia
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

    def open_contrast_panel(self):
        if self._check_image() is False:
            return
        print("Opening Contrast Panel")

    def open_threshold_panel(self):
        if self._check_image() is False:
            return
        print("Opening Threshold Panel")
    
    def open_log_panel(self):
        if self._check_image() is False:
            return
        print("Opening Log Panel")

    def open_gamma_panel(self):
        if self._check_image() is False:
            return
        print("Opening Gamma Panel")
    
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

