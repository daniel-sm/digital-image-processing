from PySide6.QtWidgets import QApplication

from core.image_handler import open_image, save_image
from core.steganography import write_steganography, read_steganography
from interface.main_window import MainWindow

def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
