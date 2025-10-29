from PySide6.QtWidgets import QMainWindow, QMenuBar, QLabel, QScrollArea
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from controller.file_controller import FileController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # definindo dimensoes da janela
        self.window_width = 1280
        self.window_height = 720

        # imagem atualmente carregada
        self.current_image = None

        # definindo título da janela e tamanho fixo
        self.setWindowTitle("Digital Image Processing")
        self.setFixedSize(self.window_width, self.window_height)

        # criando o controlador do menu de arquivos
        self.file_controller = FileController(self)

        # criando elementos da janela principal
        self._create_menu_bar()
        self._create_image_viewer()

    def _create_menu_bar(self):
        # criando o menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # configurando menu de arquivos
        file_menu = menu_bar.addMenu("File")
        
        open_image_action = QAction("Open Image...", self)
        open_image_action.triggered.connect(self.file_controller.open_image)
        file_menu.addAction(open_image_action)

        file_menu.addAction(QAction("Save As...", self))
        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.file_controller.exit_application)
        file_menu.addAction(exit_action)

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

        # inserindo mensagem inicial
        self.image_label.setText("Nenhuma imagem carregada.")
        self.image_label.setMinimumSize(
            self.window_width * 0.8, 
            self.window_height * 0.8
        )

        # adicionando o label a um scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.image_label)
        scroll_area.setAlignment(Qt.AlignCenter)

        # definindo o scroll area como widget central
        self.setCentralWidget(scroll_area)
