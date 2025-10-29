from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import os

from core.image_handler import open_image

class FileController:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window

    def open_image(self):
        # abrindo dialogo para selecionar imagem
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Open Image",
            os.getcwd(),
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            # usa a função open_image para obter matriz numpy
            img_array = open_image(file_path)
            if img_array is None:
                QMessageBox.warning(self.main_window, "Erro", "Não foi possível carregar a imagem.")
                return

            # armazena no estado da janela principal
            self.main_window.current_image = img_array

            # convertendo a imagem para QPixmap e exibindo
            height, width = img_array.shape[:2]
            bytes_per_line = 3 * width
            q_image = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image).scaled(
                self.main_window.image_label.width(), 
                self.main_window.image_label.height(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )

            self.main_window.image_label.setPixmap(pixmap)
            self.main_window.image_label.setMinimumSize(pixmap.size())

    def exit_application(self):
        # confirmando se o usuario quer sair
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # fechando a aplicacao
            self.main_window.close()
