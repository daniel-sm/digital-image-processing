from PySide6.QtWidgets import (
    QInputDialog,
    QMessageBox,
)

from core.steganography import write_steganography, read_steganography
from core.image_handler import to_byte
from controller.image_controller import update_image


class SteganographyController:
    def __init__(self, main_window):
        self.main_window = main_window

    def _check_image(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Aviso", "Nenhuma imagem aberta.")
            return False
        return True

    def write_message(self):
        if not self._check_image():
            return

        msg, ok = QInputDialog.getMultiLineText(
            self.main_window,
            "Escrever Mensagem",
            "Digite a mensagem a ser embutida na imagem:",
        )

        if not ok or not msg.strip():
            return

        img = to_byte(self.main_window.current_image)
        try:
            encoded = write_steganography(img, msg)
            update_image(self.main_window, encoded)
            QMessageBox.information(self.main_window, "Sucesso", "Mensagem gravada com sucesso!")
        except Exception as e:
            QMessageBox.critical(self.main_window, "Erro", f"Falha ao escrever mensagem:\n{e}")

    def read_message(self):
        if not self._check_image():
            return

        img = to_byte(self.main_window.current_image)
        try:
            msg = read_steganography(img)
            if not msg:
                QMessageBox.information(self.main_window, "Mensagem", "Nenhuma mensagem encontrada.")
            else:
                QMessageBox.information(self.main_window, "Mensagem Encontrada", msg)
        except Exception as e:
            QMessageBox.critical(self.main_window, "Erro", f"Falha ao ler mensagem:\n{e}")
