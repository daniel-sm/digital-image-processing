from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction


class ConvolutionMenu(QMenu):
    def __init__(self, parent, convolution_controller):
        super().__init__("Convolution", parent)

        generic = QAction("Generic Filter", self)
        generic.triggered.connect(convolution_controller.open_generic_filter_panel)
        self.addAction(generic)

        self.addSeparator()

        simple_mean = QAction("Simple Mean Filter", self)
        simple_mean.triggered.connect(convolution_controller.open_simple_mean_panel)
        self.addAction(simple_mean)

        weighted_mean = QAction("Weighted Mean Filter", self)
        weighted_mean.triggered.connect(convolution_controller.open_weighted_mean_panel)
        self.addAction(weighted_mean)

        median = QAction("Median Filter", self)
        median.triggered.connect(convolution_controller.open_median_panel)
        self.addAction(median)

        gaussian = QAction("Gaussian Filter", self)
        gaussian.triggered.connect(convolution_controller.open_gaussian_panel)
        self.addAction(gaussian)

        self.addSeparator()

        laplacian = QAction("Laplacian Filter", self)
        laplacian.triggered.connect(convolution_controller.open_laplacian_panel)
        self.addAction(laplacian)

        sobel_x = QAction("Sobel Filter - X", self)
        sobel_x.triggered.connect(convolution_controller.apply_sobel_x)
        self.addAction(sobel_x)

        sobel_y = QAction("Sobel Filter - Y", self)
        sobel_y.triggered.connect(convolution_controller.apply_sobel_y)
        self.addAction(sobel_y)

        magnitude = QAction("Magnitude - Gradient", self)
        magnitude.triggered.connect(convolution_controller.apply_magnitude_gradient)
        self.addAction(magnitude)
