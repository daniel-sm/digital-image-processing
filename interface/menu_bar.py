from PySide6.QtWidgets import QMenuBar

from controller.file_controller import FileController
from controller.image_menu_controller import ImageMenuController
from controller.histogram_controller import HistogramController
from controller.convolution_controller import ConvolutionController
from controller.fourier_controller import FourierController
from controller.geometric_controller import GeometricController
from controller.color_controller import ColorController
from controller.steganography_controller import SteganographyController

from interface.file_menu import FileMenu
from interface.image_menu import ImageMenu
from interface.histogram_menu import HistogramMenu
from interface.convolution_menu import ConvolutionMenu
from interface.fourier_menu import FourierMenu
from interface.geometric_menu import GeometricMenu
from interface.color_menu import ColorMenu
from interface.steganography_menu import SteganographyMenu


class MenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__(main_window)

        # referencia para a janela principal
        self.main_window = main_window

        # controladores
        self.file_controller = FileController(main_window)
        self.image_controller = ImageMenuController(main_window)
        self.histogram_controller = HistogramController(main_window)
        self.convolution_controller = ConvolutionController(main_window)
        self.fourier_controller = FourierController(main_window)
        self.geometric_controller = GeometricController(main_window)
        self.color_controller = ColorController(main_window)
        self.steganography_controller = SteganographyController(main_window)

        # adiciona menus
        self.addMenu(FileMenu(self, self.file_controller))
        self.addMenu(ImageMenu(self, self.image_controller))
        self.addMenu(HistogramMenu(self, self.histogram_controller))
        self.addMenu(ConvolutionMenu(self, self.convolution_controller))
        self.addMenu(FourierMenu(self, self.fourier_controller))
        self.addMenu(GeometricMenu(self, self.geometric_controller))
        self.addMenu(ColorMenu(self, self.color_controller))
        self.addMenu(SteganographyMenu(self, self.steganography_controller))
