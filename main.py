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
    return 1 - img

def threshold(img: np.ndarray, k: np.double = 0.5) -> np.ndarray:
    return (img > k) * 1.0 # transform boolean into double

def constrast(img: np.ndarray) -> np.ndarray:
    min = np.min(img)
    tmp = img - min
    max = np.max(tmp)
    tmp = tmp / max
    return tmp

def log(img: np.ndarray, c: np.double = 1) -> np.ndarray:
    return c * np.log2(1 + img)

def gamma(img: np.ndarray, y: np.double, c: np.double = 1) -> np.ndarray:
    return c * np.pow(img, y) 

def bit_slice(img: np.ndarray, k: np.uint8):
    return img & (2**(k-1))

def write_steganography(img: np.ndarray, msg: str) -> np.ndarray:
    new = img.copy()
    msg_index = 0
    shift = 7
    msg_length = len(msg)
    for index, pixel in np.ndenumerate(img):
        if (shift < 0):
            shift = 7
            msg_index += 1
        if (msg_index < msg_length):
            char = ord(msg[msg_index])
            bit = (char >> shift) & 0b00000001
            new[index] = (pixel & 0b11111110) | bit # definindo ultimo bit do pixel
            shift -= 1
        else:
            new[index] = pixel & 0b11111110 # restante dos pixels vai zerar o ultimo bit
    return new

def read_steganography(img: np.ndarray) -> str:
    msg = []
    char = 0
    bits = 0
    for pixel in np.nditer(img):
        bit = pixel & 0b00000001
        char = (char << 1) | bit
        bits += 1
        if (bits == 8):
            if (char != 0):
                msg.append(chr(char))
            bits = 0
            char = 0
    return "".join(msg) # transformando lista de caracteres em uma string

def histogram(img: np.ndarray) -> np.ndarray:
    hist = np.zeros(shape=256, dtype=int)
    for pixel in np.nditer(img):
        hist[pixel] += 1
    return hist

def plot_histgram(hist: np.array) -> None:
    _, ax = plt.subplots()
    ax.plot(hist)
    ax.set_xlim(0, 255)
    ax.set_ylim(0)
    ax.set_xticks(np.arange(0, 256, 10), minor=True)
    plt.show()

def histogram_equalization(img: np.ndarray) -> np.ndarray:
    hist = histogram(img)
    prob = hist / img.size

    acc = 0
    for i, p in np.ndenumerate(prob):
        acc += p
        prob[i] = acc

    s = np.round(prob * 255)
    s = s.astype(np.uint8)

    new = img.copy()
    for index, pixel in np.ndenumerate(new):
        new[index] = s[pixel]

    return new

def main():
    img = cv.imread("paisagem.jpg", cv.IMREAD_GRAYSCALE)

    if (img is None):
        print("Could not read the image!")
        return 0

    hist = histogram(img)
    h = histogram(histogram_equalization(img))

    print(hist)
    print(h)

    plot_histgram(hist)
    plot_histgram(h)

    return 0

main()