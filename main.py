import cv2 as cv
import numpy as np

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

def main():
    img = cv.imread("paisagem.jpg", cv.IMREAD_GRAYSCALE)

    if (img is None):
        print("Could not read the image!")
        return 0

    return 0

main()