from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

def update_image(main_window, img_array):
    if img_array is None:
        return

    # Atualiza o estado da janela
    main_window.current_image = img_array

    # Converte a imagem NumPy em QPixmap
    height, width = img_array.shape[:2]
    bytes_per_line = 3 * width
    q_image = QImage(
        img_array.data, width, height, bytes_per_line, QImage.Format_RGB888
    )
    pixmap = QPixmap.fromImage(q_image).scaled(
        1200, 680, Qt.KeepAspectRatio, Qt.SmoothTransformation
    )

    # Atualiza o label
    main_window.image_label.setPixmap(pixmap)
    main_window.image_label.setMinimumSize(pixmap.size())
