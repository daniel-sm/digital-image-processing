from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from interface.side_panel import SidePanel
from interface.image_panel import ImagePanel
from interface.menu_bar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # imagem atualmente carregada
        self.original_image = None
        self.current_image = None

        # definindo título da janela e tamanho fixo
        self.setWindowTitle("Digital Image Processing")
        self.setFixedSize(1280, 720)

        # criando barra de menus
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # layout central
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)

        # adicionando painel lateral e painel de imagem
        self.side_panel = SidePanel(self)
        self.image_panel = ImagePanel(self)

        layout.addWidget(self.side_panel)
        layout.addWidget(self.image_panel)

        # definindo o layout central
        self.setCentralWidget(central_widget)
