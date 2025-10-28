import numpy as np
import matplotlib.pyplot as plt

def histogram(img: np.ndarray) -> np.ndarray:
    # calculando o histograma da imagem
    hist = np.bincount(img.ravel(), minlength=256)
    # retornando o histograma
    return hist

def plot_histogram(hist: np.array) -> None:
    # plotando o histograma
    plt.plot(hist)
    # configurando o grafico
    plt.title("Histogram")
    plt.xlim(0, 255)
    plt.ylim(0)
    plt.xticks(np.arange(0, 256, 10), minor=True)
    # mostrando o grafico
    plt.show()

def histogram_equalization(img: np.ndarray) -> np.ndarray:
    # calculando o histograma
    hist = histogram(img)
    # calculando a porbabilidade
    prob = hist / img.size
    # calculando a distribuicao acumulada
    dist = np.cumsum(prob)
    # mapeando os valores de 0 a 255
    result = np.round(dist * 255).astype(np.uint8)

    # ajustando os pixels da imagem de acordo com o mapeamento
    new = result[img]

    # retornando a imagem equalizada
    return new
