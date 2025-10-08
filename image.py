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

def main():
    img = cv.imread("paisagem.jpg", cv.IMREAD_GRAYSCALE)

    if img is None:
        print("Could not read the image!")
        return 0

    img = convert(img)

    return 0

main()