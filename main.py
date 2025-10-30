from PySide6.QtWidgets import QApplication

from core.image_handler import open_image, save_image
from core.steganography import write_steganography, read_steganography
from interface.main_window import MainWindow

def main():
    # img = open_image("stegano_image.bmp")
    # msg = read_steganography(img)
    # print(msg)
    # stg = write_steganography(img, "Hello, World!")
    # save_image("stegano_image.bmp", stg)
    # return
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
