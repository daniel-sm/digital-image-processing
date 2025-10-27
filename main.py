import numpy as np

from src.color.conversions import rgb_to_gray, rgb_to_gray_average
from src.image.handle import compare_images, convert, deconvert, open_image, save_image, show_image

def main():
    img = open_image("image.jpg")
    show_image("image", img)

    img = convert(img)

    print(img.shape, img.dtype, np.min(img), np.max(img))

    out = rgb_to_gray(img)
    out1 = rgb_to_gray_average(img)

    print(out.shape, out.dtype, np.min(out), np.max(out))

    compare_images(out, out1)

    # save_image("output.jpg", out)

    return 0

if __name__ == "__main__":
    main()
