import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def convert(img: np.ndarray) -> np.ndarray:
    return img.astype(np.double) / 255

def deconvert(img: np.ndarray) -> np.ndarray:
    return (img * 255).astype(np.uint8)

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

def intensity_level_slicing(
        img: np.ndarray, 
        a: float = 0, 
        b: float = 1, 
        highlight: bool = True, 
        binary: bool = False
    ) -> np.ndarray:
    condition = (img >= a) & (img <= b) # destacando valores no intervalo

    yes = 1.0 if highlight else 0.0 # decidindo se vai escurecer ou clarear no intervalo
    no = 1.0 - yes # obtendo o inverso da cor no intervalo
    no = no if binary else img # decidindo se vai manter as outras cores

    new = np.where(condition, yes, no) # construindo a imagem de saida

    return new # retornando nova imagem

def bit_slice(img: np.ndarray, k: np.uint8) -> np.ndarray:
    return img & (2 ** (k - 1))

def write_steganography(img: np.ndarray, msg: str) -> np.ndarray:
    msg += '\0'

    bits = np.fromiter(
        (int(bit) for char in msg for bit in format(ord(char), '08b')),
        dtype=np.uint8
        )
    length = bits.size

    new = img.flatten()

    new[:length] = (new[:length] & 0b1111_1110) | bits

    return new.reshape(img.shape)

def read_steganography(img: np.ndarray) -> str:
    bits = (img.flatten() & 1)
    multiple_of_8 = (bits.size // 8) * 8 
    bits = bits[:multiple_of_8]

    chars = np.packbits(bits)

    msg = "".join(map(chr, chars))
    msg = msg[ : msg.find('\0')]

    return msg

def histogram(img: np.ndarray) -> np.ndarray:
    hist = np.bincount(img.ravel(), minlength=256)
    # hist = np.zeros(shape=256, dtype=int)
    # for pixel in np.nditer(img):
    #     hist[pixel] += 1
    return hist

def plot_histogram(hist: np.array) -> None:
    fig, ax = plt.subplots()
    ax.plot(hist)
    # ax.set_xlim(0, 255)
    # ax.set_ylim(0)
    # ax.set_xticks(np.arange(0, 256, 10), minor=True)
    plt.show()

def histogram_equalization(img: np.ndarray) -> np.ndarray:
    hist = histogram(img)

    prob = hist / img.size
    dist = np.cumsum(prob)
    result = np.round(dist * 255).astype(np.uint8)

    return result[img]

def piecewise_linear(
        img: np.ndarray, 
        p1: list[float], 
        p2: list[float]
    )  -> np.ndarray:
    # obtendo as coordenadas dos pontos
    x1, y1 = p1
    x2, y2 = p2

    #  coeficientes angulares das funcoes
    m1 = y1 / x1
    m2 = (y2 - y1) / (x2 - x1)
    m3 = (1 - y2) / (1 - x2)

    # coeficientes lineares das funcoes
    b2 = y1 - (m2 * x1)
    b3 = y2 - (m3 * x2)

    # criando nova imagem vazia com mesmo formato
    new = np.empty_like(img)

    # criando mascaras booleanas
    mask1 = img <= x1
    mask2 = (img > x1) & (img <= x2)
    mask3 = img > x2

    # aplicando as tres funcoes por mascaras
    new[mask1] = img[mask1] * m1
    new[mask2] = (img[mask2] * m2) + b2
    new[mask3] = (img[mask3] * m3) + b3

    # retornando imagem final
    return new

def convolution(img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # obtendo as dimensoes da imagem
    img_height, img_width = img.shape
    
    # obtendo as dimensoes do kernel
    kernel_height, kernel_width = kernel.shape

    # baseado no kernel realiza o preenchimento
    pad = (kernel_height // 2), (kernel_width // 2)
    padded = np.pad(img, pad, mode='edge')
    
    # criando nova imagem com mesmo formato
    new = np.zeros_like(img)

    # processando os valores da nova imagem
    for i in range(kernel_height):
        for j in range(kernel_width):
            new += kernel[i, j] * padded[i : (i + img_height), j : (j + img_width)]

    # retornando nova imagem processada
    return new

def mean_filter(img: np.ndarray, size: int) -> np.ndarray:
    # criando o kernel de media de acordo com o tamanho especificado
    kernel = np.ones((size, size)) / (size * size)
    # aplicando a convolucao
    return convolution(img, kernel)

def weighted_mean_filter(img: np.ndarray, size: int) -> np.ndarray:
    center = size // 2
    kernel = np.ones((size, size))
    kernel[center, center] = (size * size) - 1
    kernel /= 2 * (size * size) - 2
    return convolution(img, kernel)

def laplacian_filter(img: np.ndarray, diagonal: bool = False, negate: bool = False) -> np.ndarray:
    # constroi matriz com apenas valores 1
    kernel = np.ones((3, 3))
    # definindo o centro do kernel
    kernel[1, 1] = -8 if diagonal else -4
    # excluindo os valores diagonais se especificado
    if not diagonal:
        kernel[0, 0] = kernel[0, 2] = kernel[2, 0] = kernel[2, 2] = 0
    # invertendo os valores do kernel se especificado
    if negate:
        kernel = np.negative(kernel)
    # aplicando a convolucao
    return convolution(img, kernel)

def gaussian_kernel(size: int, sigma: float) -> np.ndarray:
    # obtendo a metade do tamanho do kernel
    half = size // 2
    # criando um vetor de coordenadas [-half, ..., 0, ..., half]
    a = np.arange(-half, half + 1)
    # criando uma grade de coordenadas [[-half, ..., half], [-half, ..., half]]
    x, y = np.meshgrid(a, a)
    # aplicando a formula gaussiana
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    # normalizando o kernel
    kernel /= np.sum(kernel)
    # retornando o kernel
    return kernel

def gaussian_filter(img: np.ndarray, size: int = 3, sigma: float = 1.0) -> np.ndarray:
    # criando o kernel gaussiano
    kernel = gaussian_kernel(size, sigma)
    # aplicando a convolucao
    return convolution(img, kernel)

def median_filter(img: np.ndarray, size: int = 3) -> np.ndarray:
    # obtendo as dimensoes da imagem
    img_height, img_width = img.shape

    # realizando preenchimento baseado no tamanho das janelas
    pad = (size // 2)
    padded = np.pad(img, pad, mode='edge')
    
    # criando array para armazenar as janelas deslocadas
    windows_shape = (size * size, img_height, img_width)
    windows = np.empty(windows_shape, dtype=img.dtype)

    # processando as janelas deslocadas
    for i in range(size):
        for j in range(size):
            window = padded[i : (i + img_height), j : (j + img_width)]
            windows[(i * size) + j] = window

    # calculando a mediana das janelas
    new = np.median(windows, axis=0).astype(img.dtype)

    # retornando nova imagem processada
    return new

def sharpening_with_laplacian(img: np.ndarray, c: float = -1, diagonal: bool = False, negate: bool = False) -> np.ndarray:
    # gerando o laplaciano da imagem
    laplacian = laplacian_filter(img, diagonal, negate)
    # somando o laplaciano a imagem original
    new = img + (c * laplacian)
    # retornando a imagem final
    return new

def high_boost_filter(img: np.ndarray, k: float = 1) -> np.ndarray:
    # obtendo a imagem desfocada
    blurred = gaussian_filter(img, size=7, sigma=1.0)
    # gerando a mascara de realce
    mask = img - blurred
    # aplicando a mascara na imagem original
    new = img + (k * mask)
    # retornando a imagem final
    return new

def sobel_x_filter(img: np.ndarray):
    # definindo o kernel sobel na direcao x
    kernel = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ])
    # aplicando a convolucao
    return convolution(img, kernel)

def sobel_y_filter(img: np.ndarray):
    # definindo o kernel sobel na direcao y
    kernel = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1],
    ])
    # aplicando a convolucao
    return convolution(img, kernel)

def sobel_magnitude_filter(img: np.ndarray):
    # obtendo os gradientes nas direcoes x e y
    gx = sobel_x_filter(img)
    gy = sobel_y_filter(img)
    # calculando a magnitude do gradiente
    new = np.sqrt(gx**2 + gy**2)
    # retornando a imagem final
    return new

def scale(img: np.ndarray, sx: float, sy: float) -> np.ndarray:
    # obtendo as dimensoes da imagem
    img_height, img_width = img.shape

    # calculando os valores de mapeamento
    x_space = np.linspace(0, img_width - 1, sx * img_width)
    y_space = np.linspace(0, img_height - 1, sy * img_height)
    dx, dy = np.meshgrid(x_space, y_space)

    # coordenadas correspondentes na imagem original
    x0 = np.floor(dx).astype(int)
    y0 = np.floor(dy).astype(int)
    x1 = np.clip(x0 + 1, 0, img_width - 1)
    y1 = np.clip(y0 + 1, 0, img_height - 1)

    # partes fracionarias
    xf = dx - x0
    yf = dy - y0

    # obtendo os valores dos pixels vizinhos da imagem original
    p1 = img[y0, x0]
    p2 = img[y0, x1]
    p3 = img[y1, x0]
    p4 = img[y1, x1]

    # interpolacao bilinear dos valores
    i1 = p1 * (1 - xf) + p2 * xf
    i2 = p3 * (1 - xf) + p4 * xf
    result = i1 * (1 - yf) + i2 * yf

    # retornando a imagem redimensionada
    return result

def rotate(img: np.ndarray, angle: float) -> np.ndarray:
    # obtendo as dimensoes da imagem
    img_height, img_width = img.shape

    # converte angulo para radianos
    rad_angle = np.deg2rad(angle)

    # calcula seno e cosseno do angulo de rotacao
    sen = np.sin(-rad_angle)
    cos = np.cos(-rad_angle)
    positive_sen = np.sin(rad_angle)
    positive_cos = np.cos(rad_angle)

    # calculando coordenadas dos cantos apos rotacao
    # canto superior direito
    top_right_x = img_width * positive_cos
    top_right_y = img_width * positive_sen
    # canto inferior direito
    bottom_right_x = (img_width * positive_cos) - (img_height * positive_sen)
    bottom_right_y = (img_width * positive_sen) + (img_height * positive_cos)
    # canto inferior esquerdo
    bottom_left_x = -img_height * positive_sen
    bottom_left_y = img_height * positive_cos
    
    # listas de coordenadas x e y dos cantos
    x_coords = [0, top_right_x, bottom_right_x, bottom_left_x]
    y_coords = [0, top_right_y, bottom_right_y, bottom_left_y]
    
    # calculando os limites da nova imagem
    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)

    # calculando as dimensoes da imagem rotacionada
    new_height = round(y_max - y_min)
    new_width = round(x_max - x_min)

    # criando grade de coordenadas da imagem rotacionada
    new_y_coords, new_x_coords = np.indices((new_height, new_width))

    # aplicando a transformacao inversa para obter coordenadas na imagem original
    original_x = ((new_x_coords + x_min) * cos - (new_y_coords + y_min) * sen)
    original_y = ((new_x_coords + x_min) * sen + (new_y_coords + y_min) * cos)
    # arrendondando com interpolacao do vizinho mais proximo
    original_x = np.round(original_x).astype(int)
    original_y = np.round(original_y).astype(int)

    # criando mascara para pixels dentro dos limites
    inside_bounds = (
        (original_x >= 0) & (original_x < img_width) & 
        (original_y >= 0) & (original_y < img_height)
    )
    # criando imagem de saida
    new = np.zeros((new_height, new_width), dtype=img.dtype)
    
    # preenchendo os pixels dentro dos limites
    new[inside_bounds] = img[
        original_y[inside_bounds], 
        original_x[inside_bounds]
    ]
    # retornando a imagem rotacionada
    return new

def show_image(title: str, img: np.ndarray) -> None:
    cv.imshow(title, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def compare_images(img1: np.ndarray, img2: np.ndarray) -> None:
    plt.subplot(1, 2, 1)
    plt.title("Image 1")
    plt.imshow(img1, cmap='gray')

    plt.subplot(1, 2, 2)
    plt.title("Image 2")
    plt.imshow(img2, cmap='gray')
    plt.show()

def save_image(path: str, img: np.ndarray) -> None:
    if img.dtype == np.double:
        img = deconvert(img)
    cv.imwrite(path, img)

def open_image(path: str) -> np.ndarray:
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read the image at path: {path}")
    return img

def main():
    img = open_image("image.jpg")

    # img = convert(img)

    out = rotate(img, 10)

    # compare_images(img, out)

    show_image("image", img)
    show_image("output", out)

    # save_image("output.jpg", out)

    return 0

if __name__ == "__main__":
    main()
