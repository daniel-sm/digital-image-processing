from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

from core.basic_operations import negative
from core.colored_operations import sepia
from core.image_handler import to_byte, to_double
from controller.image_controller import update_image

class FilterController:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window

    def apply_negative(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        img_array = to_byte(negative(to_double(self.main_window.current_image)))
        update_image(self.main_window, img_array)

    def apply_sepia(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        img_array = to_byte(sepia(to_double(self.main_window.current_image)))
        update_image(self.main_window, img_array)
