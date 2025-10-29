import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def to_double(img: np.ndarray) -> np.ndarray:
    if img.dtype == np.uint8:
        return img.astype(np.double) / 255.0
    return img

def to_byte(img: np.ndarray) -> np.ndarray:
    if img.dtype != np.uint8:
        return (img * 255).astype(np.uint8)
    return img

def open_image(path: str) -> np.ndarray:
    img = cv.imread(path, cv.IMREAD_COLOR_RGB)
    if img is None:
        raise FileNotFoundError(f"Could not read the image at path: {path}")
    return img

def show_image(title: str, img: np.ndarray) -> None:
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    cv.imshow(title, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def compare_images(img1: np.ndarray, img2: np.ndarray) -> None:
    plt.subplot(1, 2, 1)
    plt.title("Image 1")
    plt.imshow(img1)

    plt.subplot(1, 2, 2)
    plt.title("Image 2")
    plt.imshow(img2)
    plt.show()

def save_image(path: str, img: np.ndarray) -> None:
    if (img.dtype == np.double):
        img = to_byte(img)
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    cv.imwrite(path, img)
