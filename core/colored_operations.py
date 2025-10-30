import numpy as np
import matplotlib.pyplot as plt

from core.color_conversions import hsi_to_rgb, rgb_to_hsi
from core.histogram import histogram, histogram_equalization
from core.image_handler import to_byte, to_double
from core.convolution_operations import (
    convolution,
    mean_filter,
    sobel_x_filter,
    sobel_y_filter, 
    weighted_mean_filter, 
    median_filter,
    gaussian_filter,
    laplacian_filter,
    sobel_magnitude_filter,
    high_boost_filter,
)

def colored_histogram(rgb: np.ndarray) -> np.ndarray:
    # convertendo a imagem para double
    rgb = to_byte(rgb)

    # calculando o histograma para cada canal
    r_hist = histogram(rgb[..., 0])
    g_hist = histogram(rgb[..., 1])
    b_hist = histogram(rgb[..., 2])

    # retornando o histograma colorido
    return np.array([r_hist, g_hist, b_hist])

def plot_colored_histogram(hist: np.ndarray) -> None:
    # definindo as cores
    colors = ['r', 'g', 'b']
    # plotando o histograma colorido
    for i in range(3):
        # plotando o histograma de cada canal
        plt.plot(hist[i], color=colors[i])
    # configurando o grafico
    plt.title("Colored Histogram")
    plt.xlim(0, 255)
    plt.ylim(0)
    plt.xticks(np.arange(0, 256, 10), minor=True)
    # mostrando o grafico
    plt.show()

def colored_histogram_equalization(rgb: np.ndarray) -> np.ndarray:
    # convertendo imagem para hsi
    hsi = rgb_to_hsi(rgb)

    # isolando o canal de intensidade
    intensity = to_byte(hsi[..., 2])
    # equalizando o canal de intensidade
    equalized = histogram_equalization(intensity)
    # atualizando o canal de intensidade 
    hsi[:, :, 2] = to_double(equalized)

    # convertendo de volta para rgb
    new = hsi_to_rgb(hsi)

    # retornando a imagem equalizada
    return new

def intensity_histogram(rgb: np.ndarray) -> np.ndarray:
    # convertendo para hsi
    hsi = rgb_to_hsi(rgb)

    # isolando o canal de intensidade
    intensity = to_byte(hsi[..., 2])

    # calculando o histograma de intensidade
    hist = histogram(intensity)

    # retornando o histograma de intensidade
    return hist

def plot_intensity_histogram(hist: np.ndarray) -> None:
    # plotando o histograma de intensidade
    plt.plot(hist, color='k')
    # configurando o grafico
    plt.title("Intensity Histogram")
    plt.xlim(0, 255)
    plt.ylim(0)
    plt.xticks(np.arange(0, 256, 10), minor=True)
    # mostrando o grafico
    plt.show()

def adjust_hsi(hsi: np.ndarray, h: float, s: float, i: float) -> np.ndarray:
    # ajustando o matiz
    hsi[..., 0] = (hsi[..., 0] * h) % 1.0

    # ajustando a saturacao
    hsi[..., 1] = np.clip(hsi[..., 1] * s, 0, 1)

    # ajustando a intensidade
    hsi[..., 2] = np.clip(hsi[..., 2] * i, 0, 1)

    # retornando a imagem ajustada
    return hsi

def adjust_hsv(hsv: np.ndarray, h: float, s: float, v: float) -> np.ndarray:
    # ajustando o matiz
    hsv[..., 0] = (hsv[..., 0] * h) % 1.0

    # ajustando a saturacao
    hsv[..., 1] = np.clip(hsv[..., 1] * s, 0, 1)

    # ajustando o valor
    hsv[..., 2] = np.clip(hsv[..., 2] * v, 0, 1)

    # retornando a imagem ajustada
    return hsv

def adjust_rgb(rgb: np.ndarray, r: float, g: float, b: float) -> np.ndarray:
    # ajustando o canal vermelho
    rgb[..., 0] = np.clip(rgb[..., 0] * r, 0, 1)

    # ajustando o canal verde
    rgb[..., 1] = np.clip(rgb[..., 1] * g, 0, 1)

    # ajustando o canal azul
    rgb[..., 2] = np.clip(rgb[..., 2] * b, 0, 1)

    # retornando a imagem ajustada
    return rgb

def sepia(rgb: np.ndarray) -> np.ndarray:
    # definindo a matriz de filtro sepia
    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
    
    # aplicando o filtro sepia
    sepia = rgb @ sepia_matrix.T
    
    # cortando os valores para o intervalo [0, 1]
    sepia = np.clip(sepia, 0, 1)
    
    return sepia

def rgb_mean_filter(img: np.ndarray, size: int) -> np.ndarray:
    # aplicando o filtro de media em cada canal
    img[..., 0] = mean_filter(img[..., 0], size)
    img[..., 1] = mean_filter(img[..., 1], size)
    img[..., 2] = mean_filter(img[..., 2], size)
    # retornando a imagem filtrada
    return img

def rgb_weighted_mean_filter(img: np.ndarray, size: int) -> np.ndarray:
    # aplicando o filtro de media ponderada em cada canal
    img[..., 0] = weighted_mean_filter(img[..., 0], size)
    img[..., 1] = weighted_mean_filter(img[..., 1], size)
    img[..., 2] = weighted_mean_filter(img[..., 2], size)
    # retornando a imagem filtrada
    return img

def rgb_median_filter(img: np.ndarray, size: int) -> np.ndarray:
    # aplicando o filtro de mediana em cada canal
    img[..., 0] = median_filter(img[..., 0], size)
    img[..., 1] = median_filter(img[..., 1], size)
    img[..., 2] = median_filter(img[..., 2], size)
    # retornando a imagem filtrada
    return img

def rgb_gaussian_filter(img: np.ndarray, size: int = 3, sigma: float = 1.0) -> np.ndarray:
    # aplicando o filtro gaussiano em cada canal
    img[..., 0] = gaussian_filter(img[..., 0], size, sigma)
    img[..., 1] = gaussian_filter(img[..., 1], size, sigma)
    img[..., 2] = gaussian_filter(img[..., 2], size, sigma)
    # retornando a imagem filtrada
    return img

def rgb_laplacian_filter(img: np.ndarray, diagonal: bool = False, negate: bool = False) -> np.ndarray:
    # convertendo para hsi
    hsi = rgb_to_hsi(img)

    # aplicando o filtro laplaciano no canal de intensidade
    laplacian = laplacian_filter(hsi[..., 2], diagonal, negate)

    # retornando a imagem filtrada
    return laplacian

def generic_filter(img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    print(kernel)
    # aplicando o filtro generico em cada canal
    img[..., 0] = convolution(img[..., 0], kernel)
    img[..., 1] = convolution(img[..., 1], kernel)
    img[..., 2] = convolution(img[..., 2], kernel)
    # retornando a imagem filtrada
    return img

def rgb_sobel_x(img: np.ndarray) -> np.ndarray:
    # convertendo para hsi
    hsi = rgb_to_hsi(img)

    # aplicando o filtro sobel na direcao x no canal de intensidade
    sobel_x = sobel_x_filter(hsi[..., 2])

    # retornando a imagem filtrada
    return sobel_x

def rgb_sobel_y(img: np.ndarray) -> np.ndarray:
    # convertendo para hsi
    hsi = rgb_to_hsi(img)

    # aplicando o filtro sobel na direcao y no canal de intensidade
    sobel_y = sobel_y_filter(hsi[..., 2])

    # retornando a imagem filtrada
    return sobel_y

def rgb_magnitude_gradient(img: np.ndarray) -> np.ndarray:
    # convertendo para hsi
    hsi = rgb_to_hsi(img)

    # calculando a magnitude do gradiente no canal de intensidade
    magnitude = sobel_magnitude_filter(hsi[..., 2])

    # retornando a imagem filtrada
    return magnitude

def rgb_high_boost_filter(img: np.ndarray, c: float) -> np.ndarray:
    # convertendo para hsi
    hsi = rgb_to_hsi(img)

    # aplicando o filtro de alta frequencia no canal de intensidade
    hsi[..., 2] = high_boost_filter(hsi[..., 2], c)

    # convertendo de volta para rgb
    rgb = hsi_to_rgb(hsi)

    # retornando a imagem filtrada
    return rgb
