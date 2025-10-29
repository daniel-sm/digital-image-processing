from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class HistogramMenu(QMenu):
    def __init__(self, parent, histogram_controller):
        super().__init__("Histogram", parent)

        show_hist = QAction("Show Histogram", self)
        show_hist.triggered.connect(histogram_controller.show_histogram)
        self.addAction(show_hist)

        show_intensity = QAction("Show Intensity Histogram", self)
        show_intensity.triggered.connect(histogram_controller.show_intensity_histogram)
        self.addAction(show_intensity)

        self.addSeparator()

        hist_eq = QAction("Histogram Equalization", self)
        hist_eq.triggered.connect(histogram_controller.apply_histogram_equalization)
        self.addAction(hist_eq)
