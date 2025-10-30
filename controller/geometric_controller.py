from PySide6.QtWidgets import QSlider, QLabel, QMessageBox
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

from controller.image_controller import update_image
from core.image_handler import to_double, to_byte
from core.geometric_transformations import scale_rgb, rotate_rgb

class GeometricController:
    def __init__(self, main_window):
        self.main_window = main_window

    def open_scale_panel(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        panel = self.main_window.side_panel
        panel.clear_panel()

        label_x = QLabel("Scale X (%)")
        slider_x = QSlider(Qt.Horizontal)
        slider_x.setMinimum(1)
        slider_x.setMaximum(100)
        slider_x.setValue(50)
        panel.add_widget(label_x)
        panel.add_widget(slider_x)

        label_y = QLabel("Scale Y (%)")
        slider_y = QSlider(Qt.Horizontal)
        slider_y.setMinimum(1)
        slider_y.setMaximum(100)
        slider_y.setValue(50)
        panel.add_widget(label_y)
        panel.add_widget(slider_y)

        # cada vez que se muda um slider, aplica escala
        slider_x.valueChanged.connect(lambda v: self._apply_scale(slider_x.value()/50.0, slider_y.value()/50.0))
        slider_y.valueChanged.connect(lambda v: self._apply_scale(slider_x.value()/50.0, slider_y.value()/50.0))

    def _apply_scale(self, sx, sy):
        if self.main_window.original_image is None:
            return

        img = to_double(self.main_window.original_image)
        result = to_byte(scale_rgb(img, sx, sy))
        self.main_window.current_image = result
        # diretamente definir pixmap para ver a escala real
        height, width = result.shape[:2]
        if len(result.shape) == 2:
            q_image = QImage(result.data, width, height, width, QImage.Format_Grayscale8)
        else:
            bytes_per_line = 3 * width
            q_image = QImage(result.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        # nao redimensiona para caber, mostra no tamanho real
        self.main_window.image_panel.set_image_pixmap(pixmap)

    def open_rotate_panel(self):
        if self.main_window.original_image is None:
            QMessageBox.warning(self.main_window, "Erro", "Nenhuma imagem aberta.")
            return

        panel = self.main_window.side_panel
        panel.clear_panel()

        label_angle = QLabel("Angle (degrees)")
        slider_angle = QSlider(Qt.Horizontal)
        slider_angle.setMinimum(-180)
        slider_angle.setMaximum(180)
        slider_angle.setValue(0)
        slider_angle.valueChanged.connect(lambda v: self._apply_rotate(v))

        panel.add_widget(label_angle)
        panel.add_widget(slider_angle)

    def _apply_rotate(self, angle):
        if self.main_window.original_image is None:
            return
        img = to_double(self.main_window.original_image)
        result = to_byte(rotate_rgb(img, angle))
        update_image(self.main_window, result)
