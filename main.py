import numpy as np

from src.frequency.fourier import fourier_transform, inverse_fourier_transform, shift_fourier
from src.image.handle import compare_images, convert, open_image, save_image, show_image

def main():
    img = open_image("image.jpg")
    show_image("image", img)

    img = convert(img)

    out = shift_fourier(fourier_transform(img))
    show_image("output", 1000 * np.real(out)/np.max(np.real(out)))

    inv = inverse_fourier_transform(shift_fourier(out))
    show_image("inverse", inv)

    compare_images(img, inv)

    # save_image("output.jpg", out)

    return 0

if __name__ == "__main__":
    main()
