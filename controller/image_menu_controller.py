from PySide6.QtWidgets import QMainWindow, QMessageBox

from core.basic_operations import negative
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
        print("Opening Brightness Panel")
    
    def open_contrast_panel(self):
        print("Opening Contrast Panel")
    
    def open_threshold_panel(self):
        print("Opening Threshold Panel")
    
    def open_log_panel(self):
        print("Opening Log Panel")

    def open_gamma_panel(self):
        print("Opening Gamma Panel")
    
    def open_intensity_level_panel(self):
        print("Opening Intensity Level Panel")
    
    def open_piecewise_linear_panel(self):
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

