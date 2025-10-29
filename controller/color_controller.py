from PySide6.QtWidgets import QMainWindow, QMessageBox
from core.color_conversions import rgb_to_gray_average, rgb_to_gray
from core.image_handler import to_byte, to_double
from controller.image_controller import update_image

from core.image_handler import to_byte, to_double
from controller.image_controller import update_image

class ColorController:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window

    def adjust_rgb(self):
        pass

    def adjust_hsv(self):
        pass

    def adjust_hsi(self):
        pass

    def convert_to_grayscale_simple_mean(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        # convertendo para o intervalo [0,1]
        img_double = to_double(self.main_window.current_image)

        # aplicando a conversao usando media simples
        gray_img = rgb_to_gray_average(img_double)

        # convertendo de volta para o intervale [0,255]
        img_byte = to_byte(gray_img)

        # atualiza a imagem no painel
        update_image(self.main_window, img_byte)
 
    def convert_to_grayscale_weighted_mean(self):
        if self.main_window.current_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        # convertendo para o intervalo [0,1]
        img_double = to_double(self.main_window.current_image)

        # aplicando a conversao usando media simples
        gray_img = rgb_to_gray(img_double)

        # convertendo de volta para o intervale [0,255]
        img_byte = to_byte(gray_img)

        # atualiza a imagem no painel
        update_image(self.main_window, img_byte)

    # def show_histogram(self):
    #     if self.main_window.current_image is None:
    #         QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
    #         return
    #     # mostrando histograma colorido
    #     plot_colored_histogram(colored_histogram(self.main_window.current_image))

    # def show_intensity_histogram(self):
    #     if self.main_window.current_image is None:
    #         QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
    #         return
    #     # mostrando histograma de intensidade
    #     plot_intensity_histogram(intensity_histogram(to_double(self.main_window.current_image)))

    # def apply_histogram_equalization(self):
    #     if self.main_window.current_image is None:
    #         QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
    #         return
    #     # aplicando equalização de histograma
    #     img_array = to_byte(colored_histogram_equalization(to_double(self.main_window.current_image)))
    #     update_image(self.main_window, img_array)
