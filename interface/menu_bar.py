from PySide6.QtWidgets import QMenuBar

from controller.convolution_controller import ConvolutionController
from controller.file_controller import FileController
from controller.filter_controller import FilterController
from controller.histogram_controller import HistogramController
from controller.color_controller import ColorController
from controller.geometric_controller import GeometricController

from interface.file_menu import FileMenu
from interface.edit_menu import EditMenu
from interface.filter_menu import FilterMenu
from interface.histogram_menu import HistogramMenu
from interface.color_menu import ColorMenu
from interface.geometric_menu import GeometricMenu
from interface.help_menu import HelpMenu
from interface.convolution_menu import ConvolutionMenu


class MenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.main_window = main_window

        # controladores
        self.file_controller = FileController(main_window)
        self.filter_controller = FilterController(main_window)
        self.histogram_controller = HistogramController(main_window)
        self.color_controller = ColorController(main_window)
        self.geometric_controller = GeometricController(main_window)
        self.convolution_controller = ConvolutionController(main_window)

        # adiciona menus
        self.addMenu(FileMenu(self, self.file_controller))
        self.addMenu(EditMenu(self))
        self.addMenu(FilterMenu(self, self.filter_controller))
        self.addMenu(ConvolutionMenu(self, self.convolution_controller))
        self.addMenu(HistogramMenu(self, self.histogram_controller))
        self.addMenu(ColorMenu(self, self.color_controller))
        self.addMenu(GeometricMenu(self, self.geometric_controller))
        self.addMenu(HelpMenu(self))
