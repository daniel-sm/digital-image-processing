import numpy as np

from src.convolution.basics import gaussian_filter, laplacian_filter, sobel_x_filter, sobel_y_filter

def median_filter(img: np.ndarray, size: int = 3) -> np.ndarray:
    # obtendo as dimensoes da imagem
    img_height, img_width = img.shape

    # realizando preenchimento baseado no tamanho das janelas
    pad = (size // 2)
    padded = np.pad(img, pad, mode='edge')
    
    # criando array para armazenar as janelas deslocadas
    windows_shape = (size * size, img_height, img_width)
    windows = np.empty(windows_shape, dtype=img.dtype)

    # processando as janelas deslocadas
    for i in range(size):
        for j in range(size):
            window = padded[i : (i + img_height), j : (j + img_width)]
            windows[(i * size) + j] = window

    # calculando a mediana das janelas
    new = np.median(windows, axis=0).astype(img.dtype)

    # retornando nova imagem processada
    return new

def sharpening_with_laplacian(img: np.ndarray, c: float = -1, diagonal: bool = False, negate: bool = False) -> np.ndarray:
    # gerando o laplaciano da imagem
    laplacian = laplacian_filter(img, diagonal, negate)
    # somando o laplaciano a imagem original
    new = img + (c * laplacian)
    # retornando a imagem final
    return new

def high_boost_filter(img: np.ndarray, k: float = 1) -> np.ndarray:
    # obtendo a imagem desfocada
    blurred = gaussian_filter(img, size=7, sigma=1.0)
    # gerando a mascara de realce
    mask = img - blurred
    # aplicando a mascara na imagem original
    new = img + (k * mask)
    # retornando a imagem final
    return new

def sobel_magnitude_filter(img: np.ndarray):
    # obtendo os gradientes nas direcoes x e y
    gx = sobel_x_filter(img)
    gy = sobel_y_filter(img)
    # calculando a magnitude do gradiente
    new = np.sqrt(gx**2 + gy**2)
    # retornando a imagem final
    return new
