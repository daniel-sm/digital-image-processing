from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class SidePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # layout vertical
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.setFixedWidth(200)  # largura fixa do painel lateral

        # título do painel
        self.title = QLabel("Ferramentas")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")

        # botão "Close"
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.clear_panel)
        self.close_btn.hide()  # esconde inicialmente

        # inicia vazio (sem outros elementos)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.close_btn)
        self.layout.addStretch()

    def add_widget(self, widget):
        # adiciona widget antes do botão Close
        index = self.layout.indexOf(self.close_btn)
        self.layout.insertWidget(index, widget)
        self.close_btn.show()  # mostra o botão Close sempre que adicionar algo

    def clear_panel(self):
        # remove todos os widgets, exceto título e botão Close
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            w = item.widget()
            if w is not None and w not in (self.title, self.close_btn):
                w.setParent(None)
        self.close_btn.hide()  # esconde o botão Close quando o painel fica vazio
