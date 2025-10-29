from PySide6.QtWidgets import QMainWindow, QMessageBox

from core.colored_operations import (
    plot_colored_histogram,
    colored_histogram, 
    plot_intensity_histogram,
    intensity_histogram,
    colored_histogram_equalization
)
from core.image_handler import to_byte, to_double
from controller.image_controller import update_image

class HistogramController:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window

    def show_histogram(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return
        # mostrando histograma colorido
        plot_colored_histogram(colored_histogram(self.main_window.current_image))

    def show_intensity_histogram(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return
        # mostrando histograma de intensidade
        plot_intensity_histogram(intensity_histogram(to_double(self.main_window.current_image)))

    def apply_histogram_equalization(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return
        # aplicando equalização de histograma
        img_array = to_byte(colored_histogram_equalization(to_double(self.main_window.current_image)))
        update_image(self.main_window, img_array)
