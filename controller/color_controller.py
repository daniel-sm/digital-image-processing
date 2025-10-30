from PySide6.QtWidgets import QMainWindow, QMessageBox, QSlider, QLabel
from PySide6.QtCore import Qt

from core.color_conversions import (
    rgb_to_gray_average, 
    rgb_to_gray,
    rgb_to_hsv,
    hsv_to_rgb,
    rgb_to_hsi,
    hsi_to_rgb,
)
from core.colored_operations import (
    adjust_hsi,
    adjust_hsv,
    adjust_rgb,
)
from core.image_handler import to_byte, to_double
from controller.image_controller import update_image

class ColorController:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window

    def convert_to_grayscale_simple_mean(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return
        # convertendo para o intervalo [0,1]
        img_double = to_double(self.main_window.original_image)
        # aplicando a conversao usando media simples
        gray_img = rgb_to_gray_average(img_double)
        # convertendo de volta para o intervale [0,255]
        img_byte = to_byte(gray_img)
        # atualiza a imagem no painel
        update_image(self.main_window, img_byte)

    def convert_to_grayscale_weighted_mean(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return
        # convertendo para o intervalo [0,1]
        img_double = to_double(self.main_window.original_image)
        # aplicando a conversao usando media simples
        gray_img = rgb_to_gray(img_double)
        # convertendo de volta para o intervale [0,255]
        img_byte = to_byte(gray_img)
        # atualiza a imagem no painel
        update_image(self.main_window, img_byte)

    def _setup_sliders(self, channels, apply_callback):
        panel = self.main_window.side_panel

        # limpa o painel antes de adicionar novos controles
        panel.clear_panel()
        
        for ch in channels:
            label = QLabel(f"{ch} Channel")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(1)
            slider.setMaximum(100)
            slider.setValue(50)
            slider.valueChanged.connect(lambda value, c=ch: apply_callback(c, value))
            
            # adiciona os widgets via add_widget para respeitar botão Close
            panel.add_widget(label)
            panel.add_widget(slider)

    def open_adjust_hsv_panel(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        self._setup_sliders(["Hue", "Saturation", "Value"], self._apply_hsv_adjust)

    def open_adjust_hsi_panel(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        self._setup_sliders(["Hue", "Saturation", "Intensity"], self._apply_hsi_adjust)

    def open_adjust_rgb_panel(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        self._setup_sliders(["Red", "Green", "Blue"], self._apply_rgb_adjust)

    def _apply_hsv_adjust(self, channel, value):
        if self.main_window.original_image is None:
            return
        hsv = rgb_to_hsv(to_double(self.main_window.original_image))
        h, s, v = 1.0, 1.0, 1.0
        scale = value / 50
        if channel == "Hue": h = scale
        elif channel == "Saturation": s = scale
        elif channel == "Value": v = scale
        result = adjust_hsv(hsv, h, s, v)
        rgb = to_byte(hsv_to_rgb(result))
        update_image(self.main_window, rgb)

    def _apply_hsi_adjust(self, channel, value):
        if self.main_window.original_image is None:
            return
        hsi = rgb_to_hsi(to_double(self.main_window.original_image))
        h, s, i = 1.0, 1.0, 1.0
        scale = value / 50
        if channel == "Hue": h = scale
        elif channel == "Saturation": s = scale
        elif channel == "Intensity": i = scale
        result = adjust_hsi(hsi, h, s, i)
        rgb = to_byte(hsi_to_rgb(result))
        update_image(self.main_window, rgb)

    def _apply_rgb_adjust(self, channel, value):
        if self.main_window.original_image is None:
            return
        img = to_double(self.main_window.original_image)
        r, g, b = 1.0, 1.0, 1.0
        scale = value / 50
        if channel == "Red": r = scale
        elif channel == "Green": g = scale
        elif channel == "Blue": b = scale
        result = to_byte(adjust_rgb(img, r, g, b))
        update_image(self.main_window, result)
