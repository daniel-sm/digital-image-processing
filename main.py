import numpy as np

from src.color.conversions import hsi_to_rgb, hsv_to_rgb, rgb_to_hsi, rgb_to_hsv
from src.image.handle import compare_images, convert, deconvert, open_image, save_image, show_image

def main():
    img = open_image("image.jpg")
    show_image("image", img)

    img = convert(img)

    print(img.shape, img.dtype, np.min(img), np.max(img))

    hsv = rgb_to_hsv(img)
    out = hsv_to_rgb(hsv)

    print(out.shape, out.dtype, np.min(out), np.max(out))

    show_image("output", deconvert(out))

    # save_image("output.jpg", out)

    return 0

if __name__ == "__main__":
    main()
