import numpy as np
import matplotlib.pyplot as plt

from core.color_conversions import hsi_to_rgb, rgb_to_hsi
from core.histogram import histogram, histogram_equalization
from core.image_handler import to_byte, to_double

def colored_histogram(rgb: np.ndarray) -> np.ndarray:
    # convertendo a imagem para double
    rgb = to_byte(rgb)

    # calculando o histograma para cada canal
    r_hist = histogram(rgb[..., 0])
    g_hist = histogram(rgb[..., 1])
    b_hist = histogram(rgb[..., 2])

    # retornando o histograma colorido
    return np.array([r_hist, g_hist, b_hist])

def plot_colored_histogram(histogram: np.ndarray) -> None:
    # definindo as cores
    colors = ['r', 'g', 'b']
    # plotando o histograma colorido
    for i in range(3):
        # plotando o histograma de cada canal
        plt.plot(histogram[i], color=colors[i])
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
