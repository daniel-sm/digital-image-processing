from PySide6.QtWidgets import QMainWindow
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
        
        # criando painel de imagem
        self.image_panel = ImagePanel(self)
        self.setCentralWidget(self.image_panel)
