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

def steganography(img: np.ndarray, msg: str):
    new = img.copy()
    index = 0
    shift = 7
    msg_length = len(msg)
    # usando iterador para acessar indices
    it = np.nditer(img, flags=['multi_index'])
    for pixel in it:
        if (shift < 0):
            shift = 7
            index += 1
        if(index < msg_length):
            char = ord(msg[index])
            bit = (char >> shift) & 0b00000001
            pixel = (pixel & 0b11111110) | bit # definindo ultimo bit do pixel
            new[it.multi_index] = pixel # salvando pixel alterado na nova imagem
            shift -= 1
    return new

def main():
    img = cv.imread("paisagem.jpg", cv.IMREAD_GRAYSCALE)

    if (img is None):
        print("Could not read the image!")
        return 0

    new = steganography(img, "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")

    print(np.sum(img - new))

    return 0

main()