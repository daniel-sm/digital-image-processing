from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

def update_image(main_window, img_array):
    if img_array is None:
        return

    # Atualiza o estado da janela
    main_window.current_image = img_array

    # Converte a imagem NumPy em QPixmap
    height, width = img_array.shape[:2]

    # verificando as dimensoes da imagem
    if len(img_array.shape) == 2:
        # imagem em escala de cinza
        q_image = QImage(
            img_array.data, width, height, width, QImage.Format_Grayscale8
        )
    elif len(img_array.shape) == 3 and img_array.shape[2] == 3:
        # imagem colorida
        bytes_per_line = 3 * width
        q_image = QImage(
            img_array.data, width, height, bytes_per_line, QImage.Format_RGB888
        )
    else:
        # caso inesperado
        raise ValueError("Formato de imagem não suportado.")

    # redimensionando a imagem para caber no painel
    pixmap = QPixmap.fromImage(q_image).scaled(
        1024, 576, Qt.KeepAspectRatio, Qt.SmoothTransformation
    )

    # Atualiza o label
    main_window.image_panel.set_image_pixmap(pixmap)
