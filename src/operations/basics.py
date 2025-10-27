import numpy as np

def brightness(img: np.ndarray, k: np.double = 0.5) -> np.ndarray:
    return (img * k)

def negative(img: np.ndarray) -> np.ndarray:
    return (1 - img)

def threshold(img: np.ndarray, k: np.double = 0.5) -> np.ndarray:
    return (img > k).astype(np.double)

def contrast(img: np.ndarray) -> np.ndarray:
    minimum = np.min(img)
    new = img - minimum
    maximum = np.max(new)
    new = new / maximum
    return new

def log(img: np.ndarray, c: np.double = 1) -> np.ndarray:
    return c * np.log2(1 + img)

def gamma(img: np.ndarray, y: np.double, c: np.double = 1) -> np.ndarray:
    return c * np.pow(img, y) 
