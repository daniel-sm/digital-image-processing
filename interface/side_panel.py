from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider
from PySide6.QtCore import Qt

class SidePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # layout vertical
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # título do painel
        title = QLabel("Ferramentas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(title)

        # exemplo de botao
        btn_apply_filter = QPushButton("Aplicar Filtro")
        layout.addWidget(btn_apply_filter)

        # exemplo de slider
        label_slider = QLabel("Intensidade:")
        layout.addWidget(label_slider)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        layout.addWidget(slider)

        # adicionando um espaço flexível no final
        layout.addStretch()

        self.setLayout(layout)
        self.setFixedWidth(200)  # largura fixa do painel lateral
