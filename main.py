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

    if(length > new.size):
        raise ValueError("Mensagem muito grande para a imagem!")

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
    s = np.round(dist * 255).astype(np.uint8)

    new = s[img]
    return new

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
    # criando nova imagem no mesmo formato
    new = np.empty_like(img)

    # obtendo o tamanho do kernel 
    kernel_length = kernel.shape[0]
    # baseado no kernel calcula tamanho do preenchimento
    pad_width = kernel_length // 2
    # realizando preenchimento da matriz
    padded = np.pad(img, pad_width, mode='edge')
    print('padded')
    print(padded)

    # percorrendo a imagem processando os valores da nova imagem
    for index, _ in np.ndenumerate(img):
        i, j = index
        matrix = padded[i : (i + kernel_length), j : (j + kernel_length)]
        new[index] = np.vdot(matrix, kernel)

    # retornando nova imagem processada
    return new

def main():
    img = cv.imread("paisagem.jpg", cv.IMREAD_GRAYSCALE)

    if (img is None):
        print("Could not read the image!")
        return 0

    # img = convert(img)

    msg = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

    new = write_steganography(img, msg)

    res = read_steganography(new)

    print(res == msg)

    cv.imshow("Image", img)
    cv.waitKey(0)
    cv.imshow("Image", new)
    cv.waitKey(0)

    return 0

if __name__ == "__main__":
    main()