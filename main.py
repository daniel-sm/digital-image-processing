import numpy as np

from core.colored_operations import sepia
from core.image_handler import compare_images, to_double, to_byte, open_image, save_image, show_image

def main():
    img = open_image("image.jpg")
    show_image("image", img)

    img = to_double(img)
    print("IMG", img.shape, img.dtype, np.min(img), np.max(img))

    out = sepia(img)
    print("OUT", out.shape, out.dtype, np.min(out), np.max(out))

    show_image("OUT", to_byte(out))

    compare_images(img, out)

    return 0

if __name__ == "__main__":
    main()
