from PySide6.QtWidgets import QMainWindow, QMenuBar, QLabel, QScrollArea
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # definindo título da janela
        self.setWindowTitle("Digital Image Processing")
        # definindo tamanho fixo da janela
        self.setFixedSize(1280, 720)

        # criando o menu bar
        self._create_menu_bar()

        # criando a area de visualização da imagem
        self._create_image_viewer()

    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # configurando menu des arquivos
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("Open Image", self))
        file_menu.addAction(QAction("Save As...", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Exit", self))

        # configurando menu de edicao
        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction(QAction("Undo", self))
        edit_menu.addAction(QAction("Redo", self))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Cut", self))
        edit_menu.addAction(QAction("Copy", self))
        edit_menu.addAction(QAction("Paste", self))

        # configurando menu de visualizacao
        view_menu = menu_bar.addMenu("View")
        view_menu.addAction(QAction("Zoom In", self))
        view_menu.addAction(QAction("Zoom Out", self))
        view_menu.addAction(QAction("Reset Zoom", self))
        view_menu.addSeparator()
        view_menu.addAction(QAction("Fullscreen", self))

        # configurando menu de ajuda
        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(QAction("Documentation", self))
        help_menu.addAction(QAction("About", self))

    def _create_image_viewer(self):
        # criando o label que vai exibir a imagem
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        # carregando uma imagem de exemplo
        pixmap = QPixmap("image.jpg")

        # ajustando o pixmap ao label
        self.image_label.setPixmap(pixmap)
        self.image_label.setPixmap(pixmap.scaled(
            self.width(), 
            self.height(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        ))

        # adicionando o label a um scroll area
        # scroll_area = QScrollArea()
        # scroll_area.setWidget(self.image_label)
        # scroll_area.setAlignment(Qt.AlignCenter)
        # self.setCentralWidget(scroll_area)

        self.setCentralWidget(self.image_label)
