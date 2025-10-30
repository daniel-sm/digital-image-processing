from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import os

from core.image_handler import open_image, save_image
from controller.image_controller import update_image

class FileController:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Open Image",
            os.getcwd(),
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            img_array = open_image(file_path)
            if img_array is None:
                QMessageBox.warning(self.main_window, "Erro", "Não foi possível carregar a imagem.")
                return

            self.main_window.original_image = img_array.copy()
            self.main_window.current_image = img_array

            # Usa update_image para exibir a imagem (inclui redimensionamento automático)
            update_image(self.main_window, img_array)

    def save_image(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Aviso", "Nenhuma imagem para salvar.")
            return
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Salvar Imagem Como",
            "",
            "Images (*.jpg *.jpeg *.png *.bmp);;All Files (*)",
            options=options
        )
        if not file_path:
            return

        try:
            img = self.main_window.current_image
            save_image(file_path, img)
            QMessageBox.information(self.main_window, "Sucesso", f"Imagem salva em:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self.main_window, "Erro ao salvar", f"Não foi possível salvar a imagem:\n{e}")

    def reset_image(self):
        if self.main_window.original_image is None:
            QMessageBox.information(self.main_window, "Aviso", "Nenhuma imagem carregada.")
            return

        self.main_window.current_image = self.main_window.original_image.copy()
        self.main_window.side_panel.clear_panel()
        update_image(self.main_window, self.main_window.current_image)

    def close_image(self):
        if self.main_window.current_image is None:
            QMessageBox.information(self.main_window, "Aviso", "Nenhuma imagem aberta.")
            return

        reply = QMessageBox.question(
            self.main_window,
            "Fechar imagem",
            "Deseja realmente fechar a imagem atual?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.main_window.original_image = None
            self.main_window.current_image = None
            self.main_window.image_panel.clear_image()

    def exit_application(self):
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.main_window.close()
