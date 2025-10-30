from PySide6.QtWidgets import QMessageBox
from core.image_handler import to_double, to_byte
from controller.image_controller import update_image

from core.frequency_transformations import (
    colored_fourier,
    colored_inverse_fourier,
    colored_fast_fourier,
    colored_inverse_fast_fourier,
    view_fourier_transform,
)

class FourierController:
    def __init__(self, main_window):
        self.main_window = main_window

        self.fourier = None
        self.fast_fourier = None

    def _check_image(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Aviso", "Nenhuma imagem aberta.")
            return False
        return True

    def apply_fourier_transform(self):
        if not self._check_image():
            return
        if not (self.fast_fourier is None):
            QMessageBox.warning(self.main_window, "Aviso", "Transformada já calculada.")
            return
        img = to_double(self.main_window.current_image)
        # aplica transformada de Fourier
        fourier = colored_fourier(img)
        # armazenando a transformada para inversao posterior
        self.fourier = fourier
        # tornando a transformada visível
        result = view_fourier_transform(fourier)
        update_image(self.main_window, to_byte(result))

    def apply_inverse_fourier_transform(self):
        if self.fourier is None:
            QMessageBox.warning(self.main_window, "Aviso", "Nenhuma transformada de Fourier calculada.")
            return
        result = colored_inverse_fourier(self.fourier)
        self.fourier = None  # limpa apos inversao
        update_image(self.main_window, to_byte(result))

    def apply_fast_fourier_transform(self):
        if not self._check_image():
            return
        if not (self.fast_fourier is None):
            QMessageBox.warning(self.main_window, "Aviso", "Transformada já calculada.")
            return
        img = to_double(self.main_window.current_image)
        fourier = colored_fast_fourier(img)
        # tornando a transformada visível
        result = view_fourier_transform(fourier)
        update_image(self.main_window, to_byte(result))
        self.fast_fourier = fourier

    def apply_inverse_fast_fourier(self):
        if self.fast_fourier is None:
            QMessageBox.warning(self.main_window, "Aviso", "Nenhuma transformada rápida armazenada.")
            return
        result = colored_inverse_fast_fourier(self.fast_fourier)
        self.fast_fourier = None  # limpa apos inversao
        update_image(self.main_window, to_byte(result))
