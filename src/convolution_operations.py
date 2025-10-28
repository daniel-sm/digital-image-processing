import numpy as np

def convolution(img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # obtendo as dimensoes da imagem
    img_height, img_width = img.shape
    
    # obtendo as dimensoes do kernel
    kernel_height, kernel_width = kernel.shape

    # baseado no kernel realiza o preenchimento
    pad = (kernel_height // 2), (kernel_width // 2)
    padded = np.pad(img, pad, mode='edge')
    
    # criando nova imagem com mesmo formato
    new = np.zeros_like(img)

    # processando os valores da nova imagem
    for i in range(kernel_height):
        for j in range(kernel_width):
            new += kernel[i, j] * padded[i : (i + img_height), j : (j + img_width)]

    # retornando nova imagem processada
    return new

def mean_filter(img: np.ndarray, size: int) -> np.ndarray:
    # criando o kernel de media de acordo com o tamanho especificado
    kernel = np.ones((size, size)) / (size * size)
    # aplicando a convolucao
    return convolution(img, kernel)

def weighted_mean_filter(img: np.ndarray, size: int) -> np.ndarray:
    center = size // 2
    kernel = np.ones((size, size))
    kernel[center, center] = (size * size) - 1
    kernel /= 2 * (size * size) - 2
    return convolution(img, kernel)

def laplacian_filter(img: np.ndarray, diagonal: bool = False, negate: bool = False) -> np.ndarray:
    # constroi matriz com apenas valores 1
    kernel = np.ones((3, 3))
    # definindo o centro do kernel
    kernel[1, 1] = -8 if diagonal else -4
    # excluindo os valores diagonais se especificado
    if not diagonal:
        kernel[0, 0] = kernel[0, 2] = kernel[2, 0] = kernel[2, 2] = 0
    # invertendo os valores do kernel se especificado
    if negate:
        kernel = np.negative(kernel)
    # aplicando a convolucao
    return convolution(img, kernel)

def gaussian_kernel(size: int, sigma: float) -> np.ndarray:
    # obtendo a metade do tamanho do kernel
    half = size // 2
    # criando um vetor de coordenadas [-half, ..., 0, ..., half]
    a = np.arange(-half, half + 1)
    # criando uma grade de coordenadas [[-half, ..., half], [-half, ..., half]]
    x, y = np.meshgrid(a, a)
    # aplicando a formula gaussiana
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    # normalizando o kernel
    kernel /= np.sum(kernel)
    # retornando o kernel
    return kernel

def gaussian_filter(img: np.ndarray, size: int = 3, sigma: float = 1.0) -> np.ndarray:
    # criando o kernel gaussiano
    kernel = gaussian_kernel(size, sigma)
    # aplicando a convolucao
    return convolution(img, kernel)

def sobel_x_filter(img: np.ndarray):
    # definindo o kernel sobel na direcao x
    kernel = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ])
    # aplicando a convolucao
    return convolution(img, kernel)

def sobel_y_filter(img: np.ndarray):
    # definindo o kernel sobel na direcao y
    kernel = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1],
    ])
    # aplicando a convolucao
    return convolution(img, kernel)

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
