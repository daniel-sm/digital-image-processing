from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, 
    QLabel, 
    QSlider, 
    QDoubleSpinBox, 
    QPushButton, 
    QCheckBox,
)

from core.basic_operations import (
    brightness,
    gamma,
    negative,
    threshold,
    log
)
from core.colored_operations import (
    rgb_contrast, 
    rgb_intensity_slicing, 
    sepia, 
    rgb_piecewise_linear,
)
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

    def apply_contrast(self):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(rgb_contrast(img))
        update_image(self.main_window, result)

    def open_threshold_panel(self):
        if self._check_image() is False:
            return
        
        panel = self.main_window.side_panel
        panel.clear_panel()

        label_threshold = QLabel("Threshold:")
        slider_threshold = QSlider(Qt.Horizontal)
        slider_threshold.setMinimum(0)
        slider_threshold.setMaximum(255)
        slider_threshold.setValue(128)
        slider_threshold.valueChanged.connect(lambda v: self._apply_threshold(v/255.0))

        panel.add_widget(label_threshold)
        panel.add_widget(slider_threshold)

    def _apply_threshold(self, value):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(threshold(img, value))
        update_image(self.main_window, result)  

    def open_log_panel(self):
        if self._check_image() is False:
            return
        panel = self.main_window.side_panel
        panel.clear_panel()

        panel.add_widget(QLabel("Multiplier:"))

        k_input = QDoubleSpinBox()
        k_input.setRange(0.1, 2.0)
        k_input.setSingleStep(0.01)
        k_input.setValue(1.0)
        panel.add_widget(k_input)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self._apply_log(float(k_input.value())))
        panel.add_widget(apply_btn)

    def _apply_log(self, value):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(log(img, value))
        update_image(self.main_window, result)

    def open_gamma_panel(self):
        if self._check_image() is False:
            return
        panel = self.main_window.side_panel
        panel.clear_panel()

        panel.add_widget(QLabel("Lambda:"))
        y_input = QDoubleSpinBox()
        y_input.setRange(0.1, 5.0)
        y_input.setSingleStep(0.05)
        y_input.setValue(1.0)
        panel.add_widget(y_input)

        panel.add_widget(QLabel("Multiplier:"))
        k_input = QDoubleSpinBox()
        k_input.setRange(0.1, 2.0)
        k_input.setSingleStep(0.01)
        k_input.setValue(1.0)
        panel.add_widget(k_input)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self._apply_gamma(
            float(y_input.value()), float(k_input.value())))
        panel.add_widget(apply_btn)

    def _apply_gamma(self, y, c):
        if self._check_image() is False:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(gamma(img, y, c))
        update_image(self.main_window, result)

    def open_intensity_level_panel(self):
        if self._check_image() is False:
            return

        panel = self.main_window.side_panel
        panel.clear_panel()

        # Intervalo A
        panel.add_widget(QLabel("Interval start:"))
        a_input = QDoubleSpinBox()
        a_input.setRange(0.0, 1.0)
        a_input.setSingleStep(0.05)
        a_input.setValue(0.2)
        panel.add_widget(a_input)

        # Intervalo B
        panel.add_widget(QLabel("Interval end:"))
        b_input = QDoubleSpinBox()
        b_input.setRange(0.0, 1.0)
        b_input.setSingleStep(0.05)
        b_input.setValue(0.8)
        panel.add_widget(b_input)

        # Opções de comportamento
        highlight_check = QCheckBox("Highlight in Interval")
        highlight_check.setChecked(True)
        binary_check = QCheckBox("Binary Mode")
        panel.add_widget(highlight_check)
        panel.add_widget(binary_check)

        # Botão aplicar
        apply_btn = QPushButton("Apply")
        panel.add_widget(apply_btn)

        apply_btn.clicked.connect(
            lambda: self.apply_intensity_level(
                float(a_input.value()),
                float(b_input.value()),
                highlight_check.isChecked(),
                binary_check.isChecked(),
            )
        )

    def apply_intensity_level(self, a, b, highlight, binary):
        if self.main_window.original_image is None:
            return

        img = to_double(self.main_window.original_image)
        filtered = rgb_intensity_slicing(img, a, b, highlight, binary)
        update_image(self.main_window, to_byte(filtered))

    def open_piecewise_linear_panel(self):
        if self._check_image() is False:
            return

        panel = self.main_window.side_panel
        panel.clear_panel()

        # Ponto 1 (p1)
        panel.add_widget(QLabel("Ponto P1 (x1, y1):"))

        x1_input = QDoubleSpinBox()
        x1_input.setRange(0.0, 1.0)
        x1_input.setSingleStep(0.05)
        x1_input.setValue(0.2)

        y1_input = QDoubleSpinBox()
        y1_input.setRange(0.0, 1.0)
        y1_input.setSingleStep(0.05)
        y1_input.setValue(0.2)

        panel.add_widget(QLabel("x1:"))
        panel.add_widget(x1_input)
        panel.add_widget(QLabel("y1:"))
        panel.add_widget(y1_input)

        # Ponto 2 (p2)
        panel.add_widget(QLabel("Ponto P2 (x2, y2):"))

        x2_input = QDoubleSpinBox()
        x2_input.setRange(0.0, 1.0)
        x2_input.setSingleStep(0.05)
        x2_input.setValue(0.8)

        y2_input = QDoubleSpinBox()
        y2_input.setRange(0.0, 1.0)
        y2_input.setSingleStep(0.05)
        y2_input.setValue(0.8)

        panel.add_widget(QLabel("x2:"))
        panel.add_widget(x2_input)
        panel.add_widget(QLabel("y2:"))
        panel.add_widget(y2_input)

        # Botão aplicar
        apply_btn = QPushButton("Apply")
        panel.add_widget(apply_btn)

        apply_btn.clicked.connect(
            lambda: self.apply_piecewise_linear(
                [float(x1_input.value()), float(y1_input.value())],
                [float(x2_input.value()), float(y2_input.value())],
            )
        )

    def apply_piecewise_linear(self, p1, p2):
        if self.main_window.original_image is None:
            return

        img = to_double(self.main_window.original_image)
        filtered = rgb_piecewise_linear(img, p1, p2)
        update_image(self.main_window, to_byte(filtered))

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

