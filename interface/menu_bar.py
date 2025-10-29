from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction

from controller.file_controller import FileController
from controller.filter_controller import FilterController
from controller.histogram_controller import HistogramController
from controller.color_controller import ColorController

class MenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__(main_window)

        # guardando referencia para a janela principal e controladores
        self.main_window = main_window
        self.file_controller = FileController(main_window)
        self.filter_controller = FilterController(main_window)
        self.histogram_controller = HistogramController(main_window)
        self.color_controller = ColorController(main_window)

        # criando os menus
        self._create_menus()

    def _create_menus(self):
        # configurando menu FILE
        file_menu = self.addMenu("File")

        open_action = QAction("Open Image...", self)
        open_action.triggered.connect(self.file_controller.open_image)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        reset_action = QAction("Reset Image", self)
        reset_action.triggered.connect(self.file_controller.reset_image)
        file_menu.addAction(reset_action)

        close_action = QAction("Close Image", self)
        close_action.triggered.connect(self.file_controller.close_image)
        file_menu.addAction(close_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.file_controller.exit_application)
        file_menu.addAction(exit_action)

        # configurando menu EDIT
        edit_menu = self.addMenu("Edit")
        edit_menu.addAction(QAction("Undo", self))
        edit_menu.addAction(QAction("Redo", self))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Cut", self))
        edit_menu.addAction(QAction("Copy", self))
        edit_menu.addAction(QAction("Paste", self))

        # configurando menu FILTERS
        filters_menu = self.addMenu("Filters")

        negative_action = QAction("Negative", self)
        negative_action.triggered.connect(self.filter_controller.apply_negative)
        filters_menu.addAction(negative_action)

        sepia_action = QAction("Sepia", self)
        sepia_action.triggered.connect(self.filter_controller.apply_sepia)
        filters_menu.addAction(sepia_action)

        # configurando menu HISTOGRAM
        histogram_menu = self.addMenu("Histogram")

        show_hist_action = QAction("Show Histogram", self)
        show_hist_action.triggered.connect(self.histogram_controller.show_histogram)
        histogram_menu.addAction(show_hist_action)

        show_intensity_hist_action = QAction("Show Intensity Histogram", self)
        show_intensity_hist_action.triggered.connect(self.histogram_controller.show_intensity_histogram)
        histogram_menu.addAction(show_intensity_hist_action)

        histogram_menu.addSeparator()

        hist_eq_action = QAction("Histogram Equalization", self)
        hist_eq_action.triggered.connect(self.histogram_controller.apply_histogram_equalization)
        histogram_menu.addAction(hist_eq_action)

        # configurando menu COLORS
        color_menu = self.addMenu("Color")

        adjust_rgb_action = QAction("Adjust RGB", self)
        adjust_rgb_action.triggered.connect(self.color_controller.adjust_rgb)
        color_menu.addAction(adjust_rgb_action)

        adjust_hsv_action = QAction("Adjust HSV", self)
        adjust_hsv_action.triggered.connect(self.color_controller.adjust_hsv)
        color_menu.addAction(adjust_hsv_action)

        adjust_hsi_action = QAction("Adjust HSI", self)
        adjust_hsi_action.triggered.connect(self.color_controller.adjust_hsi)
        color_menu.addAction(adjust_hsi_action)

        color_menu.addSeparator()

        grayscale_submenu = QMenu("Convert to Grayscale", self)

        simple_mean_action = QAction("Simple Mean", self)
        simple_mean_action.triggered.connect(self.color_controller.convert_to_grayscale_simple_mean)
        grayscale_submenu.addAction(simple_mean_action)

        weighted_mean_action = QAction("Weighted Mean", self)
        weighted_mean_action.triggered.connect(self.color_controller.convert_to_grayscale_weighted_mean)
        grayscale_submenu.addAction(weighted_mean_action)

        color_menu.addMenu(grayscale_submenu)

        # configurando menu de ajuda
        help_menu = self.addMenu("Help")
        help_menu.addAction(QAction("Documentation", self))
        help_menu.addAction(QAction("About", self))
