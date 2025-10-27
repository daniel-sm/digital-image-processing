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
