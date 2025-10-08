import cv2 as cv

img = cv.imread("sonic.jpg")

if img is None:
    print("Could not read the image.")

cv.imshow("Image", img)
cv.waitKey(0)