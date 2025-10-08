import cv2 as cv
import numpy as np

def convert(img: np.ndarray) -> np.ndarray:
    return img.astype(np.double) / 255

def brightness(img: np.ndarray, k: np.double = 0.5) -> np.ndarray:
    return (img * k)

def negative(img: np.ndarray):
    return 1 - img

def threshold(img: np.ndarray, k: np.double = 0.5) -> np.ndarray:
    return (img > k) * 1.0 # transform boolean into double

def constrast(img: np.ndarray):
    min = np.min(img)
    tmp = img - min
    max = np.max(tmp)
    tmp = tmp / max
    return tmp

img = cv.imread("low2.jpg", cv.IMREAD_GRAYSCALE)

if img is None:
    print("Could not read the image!")

img = convert(img)

print(np.min(img))
print(np.max(img))
print(np.min(constrast(img)))
print(np.max(constrast(img)))

cv.imshow("Image", img)
cv.waitKey(0)
cv.imshow("Image", constrast(img))
cv.waitKey(0)