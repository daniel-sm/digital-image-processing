from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

def update_image(main_window, img_array):
    if img_array is None:
        return

    # atualizando a imagem atual na janela
    main_window.current_image = img_array

    # obtendo dimensões da imagem
    height, width = img_array.shape[:2]

    # criando QImage conforme o tipo
    if len(img_array.shape) == 2:
        # imagem em escala de cinza
        q_image = QImage(
            img_array.data, width, height, width, QImage.Format_Grayscale8
        )
    elif len(img_array.shape) == 3 and img_array.shape[2] == 3:
        bytes_per_line = 3 * width
        q_image = QImage(
            img_array.data, width, height, bytes_per_line, QImage.Format_RGB888
        )
    else:
        raise ValueError("Formato de imagem não suportado.")

    pixmap = QPixmap.fromImage(q_image)

    # Agora: **ajuste inicial para caber no painel**, apenas se não houver zoom aplicado
    image_panel = main_window.image_panel

    # tamanho do widget de exibição
    panel_size = image_panel.viewport().size()  # área visível do scroll area
    if panel_size.width() > 0 and panel_size.height() > 0:
        # calcular fator de escala para caber
        factor_w = panel_size.width() / width
        factor_h = panel_size.height() / height
        scale_factor = min(factor_w, factor_h, 1.0)  # não ampliar acima do tamanho original
    else:
        scale_factor = 1.0

    # aplicar escala inicial
    pixmap = pixmap.scaled(
        width * scale_factor,
        height * scale_factor,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )

    # Atualiza o label
    image_panel.set_image_pixmap(pixmap)
