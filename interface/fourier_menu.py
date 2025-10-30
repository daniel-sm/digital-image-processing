from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class FourierMenu(QMenu):
    def __init__(self, parent, fourier_controller):
        super().__init__("Fourier", parent)

        fourier_transform = QAction("Fourier Transform", self)
        fourier_transform.triggered.connect(fourier_controller.apply_fourier_transform)
        self.addAction(fourier_transform)

        inverse_fourier = QAction("Inverse Fourier Transform", self)
        inverse_fourier.triggered.connect(fourier_controller.apply_inverse_fourier_transform)
        self.addAction(inverse_fourier)

        self.addSeparator()

        fast_fourier = QAction("Fast Fourier Transform", self)
        fast_fourier.triggered.connect(fourier_controller.apply_fast_fourier_transform)
        self.addAction(fast_fourier)

        inverse_fft = QAction("Inverse FFT", self)
        inverse_fft.triggered.connect(fourier_controller.apply_inverse_fast_fourier)
        self.addAction(inverse_fft)
