import numpy as np
import matplotlib.pyplot as plt

from src.color_conversions import hsi_to_rgb, rgb_to_hsi
from src.histogram import histogram, histogram_equalization
from src.image_handler import to_byte, to_double

def colored_histogram(img: np.ndarray) -> np.ndarray:
    # convertendo a imagem para double
    img = to_byte(img)

    # calculando o histograma para cada canal
    r_hist = histogram(img[..., 0])
    g_hist = histogram(img[..., 1])
    b_hist = histogram(img[..., 2])

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

def colored_histogram_equalization(img: np.ndarray) -> np.ndarray:
    # convertendo imagem para hsi
    hsi = rgb_to_hsi(img)

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
