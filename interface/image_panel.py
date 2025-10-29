from PySide6.QtWidgets import QLabel, QScrollArea
from PySide6.QtCore import Qt

class ImagePanel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        # configurando o label para exibir a imagem
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Nenhuma imagem carregada.")
        self.image_label.setFixedSize(1024, 576)

        # configurando o painel de rolagem
        self.setWidget(self.image_label)
        self.setAlignment(Qt.AlignCenter)

    def set_image_pixmap(self, pixmap):
        # atualizando o label com a nova imagem
        self.image_label.setPixmap(pixmap)

    def clear_image(self):
        # resetando o painel para o estado inicial
        self.image_label.clear()
        self.image_label.setText("Nenhuma imagem carregada.")
