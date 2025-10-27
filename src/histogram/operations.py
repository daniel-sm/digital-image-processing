import numpy as np
import matplotlib.pyplot as plt

def histogram(img: np.ndarray) -> np.ndarray:
    hist = np.bincount(img.ravel(), minlength=256)
    # hist = np.zeros(shape=256, dtype=int)
    # for pixel in np.nditer(img):
    #     hist[pixel] += 1
    return hist

def plot_histogram(hist: np.array) -> None:
    fig, ax = plt.subplots()
    ax.plot(hist)
    # ax.set_xlim(0, 255)
    # ax.set_ylim(0)
    # ax.set_xticks(np.arange(0, 256, 10), minor=True)
    plt.show()

def histogram_equalization(img: np.ndarray) -> np.ndarray:
    hist = histogram(img)

    prob = hist / img.size
    dist = np.cumsum(prob)
    result = np.round(dist * 255).astype(np.uint8)

    return result[img]
