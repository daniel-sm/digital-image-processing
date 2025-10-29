import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel, 
    QPushButton, 
    QComboBox, 
    QDoubleSpinBox, 
    QCheckBox, 
    QMessageBox, 
    QDialog, 
    QGridLayout, 
    QLineEdit,
    QVBoxLayout
)

from core.colored_operations import (
    rgb_mean_filter,
    rgb_weighted_mean_filter,
    rgb_median_filter,
    rgb_gaussian_filter,
    rgb_laplacian_filter,
    generic_filter,
    rgb_sobel_x,
    rgb_sobel_y,
    rgb_magnitude_gradient,
)
from controller.image_controller import update_image
from core.image_handler import to_byte, to_double


class ConvolutionController:
    def __init__(self, main_window):
        self.main_window = main_window

    def _check_image(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Aviso", "Nenhuma imagem aberta.")
            return False
        return True

    def _create_kernel_selector(self, panel):
        panel.add_widget(QLabel("Selecione o tamanho do kernel:"))
        combo = QComboBox()
        for i in range(3, 26, 2):  # apenas tamanhos ímpares
            combo.addItem(str(i))
        panel.add_widget(combo)
        return combo

    def open_generic_filter_panel(self):
        if not self._check_image():
            return
        panel = self.main_window.side_panel
        panel.clear_panel()

        label = QLabel("Selecione o tamanho do kernel:")
        panel.add_widget(label)

        kernel_size = QComboBox()
        for i in range(3, 26, 2):
            kernel_size.addItem(str(i))
        panel.add_widget(kernel_size)

        open_btn = QPushButton("Editar Kernel")
        open_btn.clicked.connect(lambda: self._open_kernel_input_dialog(int(kernel_size.currentText())))
        panel.add_widget(open_btn)

    def _open_kernel_input_dialog(self, size: int):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle(f"Editar Kernel {size}x{size}")
        layout = QVBoxLayout(dialog)

        grid = QGridLayout()
        inputs = []

        for i in range(size):
            row_inputs = []
            for j in range(size):
                field = QLineEdit("0")
                field.setFixedWidth(50)
                field.setAlignment(Qt.AlignCenter)
                grid.addWidget(field, i, j)
                row_inputs.append(field)
            inputs.append(row_inputs)

        layout.addLayout(grid)

        apply_btn = QPushButton("Aplicar Filtro")
        layout.addWidget(apply_btn)
        apply_btn.clicked.connect(lambda: self._apply_generic_filter(size, inputs, dialog))

        dialog.setLayout(layout)
        dialog.exec()

    def _apply_generic_filter(self, size: int, inputs, dialog):
        if not self._check_image():
            return

        kernel = np.zeros((size, size), dtype=np.double)
        for i in range(size):
            for j in range(size):
                try:
                    kernel[i, j] = float(inputs[i][j].text())
                except ValueError:
                    kernel[i, j] = 0.0

        img = to_double(self.main_window.original_image)
        filtered = generic_filter(img, kernel)
        update_image(self.main_window, to_byte(filtered))
        dialog.accept()

    def open_simple_mean_panel(self):
        panel = self.main_window.side_panel
        panel.clear_panel()

        kernel_size = self._create_kernel_selector(panel)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self.apply_simple_mean_filter(int(kernel_size.currentText())))
        panel.add_widget(apply_btn)

    def apply_simple_mean_filter(self, size: int):
        if not self._check_image():
            return
        img = to_double(self.main_window.original_image)
        filtered = rgb_mean_filter(img, size)
        update_image(self.main_window, to_byte(filtered))

    def open_weighted_mean_panel(self):
        panel = self.main_window.side_panel
        panel.clear_panel()

        kernel_size = self._create_kernel_selector(panel)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self.apply_weighted_mean_filter(int(kernel_size.currentText())))
        panel.add_widget(apply_btn)

    def apply_weighted_mean_filter(self, size: int):
        if not self._check_image():
            return
        img = to_double(self.main_window.original_image)
        filtered = rgb_weighted_mean_filter(img, size)
        update_image(self.main_window, to_byte(filtered))

    def open_median_panel(self):
        panel = self.main_window.side_panel
        panel.clear_panel()

        kernel_size = self._create_kernel_selector(panel)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self.apply_median_filter(int(kernel_size.currentText())))
        panel.add_widget(apply_btn)

    def apply_median_filter(self, size: int):
        if not self._check_image():
            return
        img = to_double(self.main_window.original_image)
        filtered = rgb_median_filter(img, size)
        update_image(self.main_window, to_byte(filtered))

    def open_gaussian_panel(self):
        panel = self.main_window.side_panel
        panel.clear_panel()

        kernel_size = self._create_kernel_selector(panel)
        panel.add_widget(QLabel("Valor de Sigma (desvio padrão):"))

        sigma_input = QDoubleSpinBox()
        sigma_input.setRange(0.1, 20.0)
        sigma_input.setSingleStep(0.1)
        sigma_input.setValue(1.0)
        panel.add_widget(sigma_input)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self.apply_gaussian_filter(
            int(kernel_size.currentText()), float(sigma_input.value())
        ))
        panel.add_widget(apply_btn)

    def apply_gaussian_filter(self, size: int, sigma: float):
        if not self._check_image():
            return
        img = to_double(self.main_window.original_image)
        filtered = rgb_gaussian_filter(img, size, sigma)
        update_image(self.main_window, to_byte(filtered))

    def open_laplacian_panel(self):
        panel = self.main_window.side_panel
        panel.clear_panel()

        panel.add_widget(QLabel("Opções do Filtro Laplaciano:"))

        diagonal_check = QCheckBox("Incluir diagonais")
        negate_check = QCheckBox("Centro positivo")

        panel.add_widget(diagonal_check)
        panel.add_widget(negate_check)

        apply_btn = QPushButton("Aplicar")
        apply_btn.clicked.connect(lambda: self.apply_laplacian_filter(
            diagonal_check.isChecked(), negate_check.isChecked()
        ))
        panel.add_widget(apply_btn)

    def apply_laplacian_filter(self, diagonal: bool, negate: bool):
        if not self._check_image():
            return
        img = to_double(self.main_window.original_image)
        filtered = rgb_laplacian_filter(img, diagonal, negate)
        update_image(self.main_window, to_byte(filtered))

    def apply_sobel_x(self):
        if not self._check_image():
            return
        img = to_double(self.main_window.original_image)
        filtered = rgb_sobel_x(img)
        update_image(self.main_window, to_byte(filtered))

    def apply_sobel_y(self):
        if not self._check_image():
            return
        img = to_double(self.main_window.original_image)
        filtered = rgb_sobel_y(img)
        update_image(self.main_window, to_byte(filtered))

    def apply_magnitude_gradient(self):
        if not self._check_image():
            return
        img = to_double(self.main_window.original_image)
        magnitude = rgb_magnitude_gradient(img)
        update_image(self.main_window, to_byte(magnitude))
