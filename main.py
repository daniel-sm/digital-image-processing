import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def convert(img: np.ndarray) -> np.ndarray:
    return img.astype(np.double) / 255

def deconvert(img: np.ndarray) -> np.ndarray:
    return (img * 255).astype(np.uint8)

def brightness(img: np.ndarray, k: np.double = 0.5) -> np.ndarray:
    return (img * k)

def negative(img: np.ndarray) -> np.ndarray:
    return (1 - img)

def threshold(img: np.ndarray, k: np.double = 0.5) -> np.ndarray:
    return (img > k).astype(np.double)

def constrast(img: np.ndarray) -> np.ndarray:
    minimum = np.min(img)
    new = img - minimum
    maximum = np.max(new)
    new = new / max
    return new

def log(img: np.ndarray, c: np.double = 1) -> np.ndarray:
    return c * np.log2(1 + img)

def gamma(img: np.ndarray, y: np.double, c: np.double = 1) -> np.ndarray:
    return c * np.pow(img, y) 

def intensity_level_slicing(
        img: np.ndarray, 
        a: float = 0, 
        b: float = 1, 
        highlight: bool = True, 
        binary: bool = False
    ) -> np.ndarray:
    condition = (img >= a) & (img <= b) # destacando valores no intervalo

    yes = 1.0 if highlight else 0.0 # decidindo se vai escurecer ou clarear no intervalo
    no = 1.0 - yes # obtendo o inverso da cor no intervalo
    no = no if binary else img # decidindo se vai manter as outras cores

    new = np.where(condition, yes, no) # construindo a imagem de saida

    return new # retornando nova imagem

def bit_slice(img: np.ndarray, k: np.uint8) -> np.ndarray:
    return img & (2 ** (k - 1))

def write_steganography(img: np.ndarray, msg: str) -> np.ndarray:
    msg += '\0'

    bits = np.fromiter(
        (int(bit) for char in msg for bit in format(ord(char), '08b')),
        dtype=np.uint8
        )
    length = bits.size

    new = img.flatten()

    new[:length] = (new[:length] & 0b1111_1110) | bits

    return new.reshape(img.shape)

def read_steganography(img: np.ndarray) -> str:
    bits = (img.flatten() & 1)
    multiple_of_8 = (bits.size // 8) * 8 
    bits = bits[:multiple_of_8]

    chars = np.packbits(bits)

    msg = "".join(map(chr, chars))
    msg = msg[ : msg.find('\0')]

    return msg

def histogram(img: np.ndarray) -> np.ndarray:
    hist = np.bincount(img.ravel(), minlength=256)
    # hist = np.zeros(shape=256, dtype=int)
    # for pixel in np.nditer(img):
    #     hist[pixel] += 1
    return hist

def plot_histgram(hist: np.array) -> None:
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

def piecewise_linear(
        img: np.ndarray, 
        p1: list[float], 
        p2: list[float]
    )  -> np.ndarray:
    # obtendo as coordenadas dos pontos
    x1, y1 = p1
    x2, y2 = p2

    #  coeficientes angulares das funcoes
    m1 = y1 / x1
    m2 = (y2 - y1) / (x2 - x1)
    m3 = (1 - y2) / (1 - x2)

    # coeficientes lineares das funcoes
    b2 = y1 - (m2 * x1)
    b3 = y2 - (m3 * x2)

    # criando nova imagem vazia com mesmo formato
    new = np.empty_like(img)

    # criando mascaras booleanas
    mask1 = img <= x1
    mask2 = (img > x1) & (img <= x2)
    mask3 = img > x2

    # aplicando as tres funcoes por mascaras
    new[mask1] = img[mask1] * m1
    new[mask2] = (img[mask2] * m2) + b2
    new[mask3] = (img[mask3] * m3) + b3

    # retornando imagem final
    return new

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
    kernel = np.ones((size, size)) / (size * size)
    return convolution(img, kernel)

def weighted_mean_filter(img: np.ndarray, size: int) -> np.ndarray:
    center = size // 2
    kernel = np.ones((size, size))
    kernel[center, center] = (size * size) - 1
    kernel /= 2 * (size * size) - 2
    return convolution(img, kernel)

def main():
    img = cv.imread("paisagem.jpg", cv.IMREAD_GRAYSCALE)

    if (img is None):
        print("Could not read the image!")
        return 0

    img = convert(img)
    new = weighted_mean_filter(img, 81)

    cv.imshow("Image", img)
    cv.waitKey(0)
    cv.imshow("Image", new)
    cv.waitKey(0)

    return 0

if __name__ == "__main__":
    main()