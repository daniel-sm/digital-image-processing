from PySide6.QtWidgets import QLabel, QScrollArea
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

class ImagePanel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.setText("Nenhuma imagem carregada.")
        self.setWidget(self.image_label)
        self.setAlignment(Qt.AlignCenter)
        self.setWidgetResizable(True)

        # controle de zoom
        self._scale_factor = 1.0
        self._pixmap_original = None

    def set_image_pixmap(self, pixmap: QPixmap):
        if pixmap is None:
            self.clear_image()
            return

        self._pixmap_original = pixmap
        self._scale_factor = 1.0
        self._update_displayed_pixmap()

    def clear_image(self):
        self._pixmap_original = None
        self.image_label.clear()
        self.image_label.setText("Nenhuma imagem carregada.")

    def _update_displayed_pixmap(self):
        if self._pixmap_original is None:
            return

        # redimensiona suavemente a imagem
        scaled_pixmap = self._pixmap_original.scaled(
            self._pixmap_original.size() * self._scale_factor,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.adjustSize()

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier and self._pixmap_original:
            angle = event.angleDelta().y()
            zoom_factor = 1.25 if angle > 0 else 0.8
            self._scale_factor *= zoom_factor
            self._scale_factor = max(0.1, min(self._scale_factor, 10))  # limites
            self._update_displayed_pixmap()
            event.accept()
        else:
            super().wheelEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._pixmap_original and self._scale_factor == 1.0:
            self._update_displayed_pixmap()
