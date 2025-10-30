import numpy as np

from core.color_conversions import rgb_to_hsv, hsv_to_rgb

def fourier_transform(img: np.ndarray) -> np.ndarray:
    # obtendo as dimensoes da imagem
    img_height, img_width = img.shape

    # obtendo os vetores de coordenadas
    x = np.arange(img_height)
    y = np.arange(img_width)
    u = np.arange(img_height)
    v = np.arange(img_width)

    # criando as matrizes de exponenciais
    rows_exp = np.exp(-2j * np.pi * np.outer(u, x) / img_height)
    cols_exp = np.exp(-2j * np.pi * np.outer(v, y) / img_width)

    # calculando a transformada de fourier com produto matricial
    fourier = (rows_exp @ img) @ cols_exp.T

    # retornando a transformada de fourier
    return fourier

def inverse_fourier_transform(fourier: np.ndarray) -> np.ndarray:
    # obtendo as dimensoes da transformada
    f_height, f_width = fourier.shape

    # obtendo os vetores de coordenadas
    u = np.arange(f_height)
    v = np.arange(f_width)
    x = np.arange(f_height)
    y = np.arange(f_width)

    # criando as matrizes de exponenciais inversas
    inv_rows_exp = np.exp(2j * np.pi * np.outer(x, u) / f_height)
    inv_cols_exp = np.exp(2j * np.pi * np.outer(y, v) / f_width)

    # calculando a transformada inversa de fourier com produto matricial
    img = ((inv_rows_exp @ fourier) @ inv_cols_exp.T) / (f_height * f_width)

    # retornando a imagem reconstruida
    return np.real(img)

def shift_fourier(fourier: np.ndarray) -> np.ndarray:
    # obtendo as dimensoes da transformada
    img_height, img_width = fourier.shape

    # calculando as metades das dimensoes
    half_height, half_width = img_height // 2, img_width // 2

    # dividindo a transformada em quatro quadrantes
    quadrant1 = fourier[:half_height, :half_width]
    quadrant2 = fourier[:half_height, half_width:]
    quadrant3 = fourier[half_height:, :half_width]
    quadrant4 = fourier[half_height:, half_width:]

    # reorganizando os quadrantes para centralizar as baixas frequencias
    top = np.hstack((quadrant4, quadrant3))
    bottom = np.hstack((quadrant2, quadrant1))
    shifted = np.vstack((top, bottom))

    # retornando a transformada deslocada
    return shifted

def fast_fourier_transform(img: np.ndarray) -> np.ndarray:
    # aplicando a transformada rapida de fourier
    return np.fft.fft2(img)

def inverse_fast_fourier_transform(fourier: np.ndarray) -> np.ndarray:
    # aplicando a transformada inversa rapida de fourier
    return np.fft.ifft2(fourier)

def shift_fast_fourier(fourier: np.ndarray) -> np.ndarray:
    # aplicando o deslocamento da transformada rapida de fourier
    return np.fft.fftshift(fourier)

def colored_fourier(rgb: np.ndarray) -> np.ndarray:
    #convertendo para hsv
    hsv = rgb_to_hsv(rgb)

    # isolando os canais
    hue = hsv[..., 0]
    saturation = hsv[..., 1]
    value = hsv[..., 2]

    # aplicando a transformada de fourier no canal de intensidade
    fourier = fourier_transform(value)

    # reconstruindo a transformada colorida
    result = np.stack((hue, saturation, fourier), axis=-1)

    # retornando a transformada RGB
    return result

def colored_inverse_fourier(fourier: np.ndarray) -> np.ndarray:
    # isolando os canais
    H = np.real(fourier[..., 0])
    S = np.real(fourier[..., 1])
    # calculando a inversa
    V = inverse_fourier_transform(fourier[..., 2])
    # montando a iamgem reconstruida
    result = np.stack((H, S, V), axis=-1)
    # convertendo para rgb
    rgb = hsv_to_rgb(result)
    # retornando a imagem
    return rgb

def colored_fast_fourier(rgb: np.ndarray) -> np.ndarray:
    #convertendo para hsv
    hsv = rgb_to_hsv(rgb)

    # isolando os canais
    hue = hsv[..., 0]
    saturation = hsv[..., 1]
    value = hsv[..., 2]

    # aplicando a transformada de fourier no canal de intensidade
    fourier = fast_fourier_transform(value)

    # reconstruindo a transformada colorida
    result = np.stack((hue, saturation, fourier), axis=-1)

    # retornando a transformada RGB
    return result

def colored_inverse_fast_fourier(fourier: np.ndarray) -> np.ndarray:
    # isolando os canais
    H = np.real(fourier[..., 0])
    S = np.real(fourier[..., 1])
    # calculando a inversa
    V = np.real(inverse_fast_fourier_transform(fourier[..., 2]))
    # montando a iamgem reconstruida
    result = np.stack((H, S, V), axis=-1)
    # convertendo para rgb
    rgb = hsv_to_rgb(result)
    # retornando a imagem
    return rgb

def view_fourier_transform(fourier: np.ndarray) -> np.ndarray:
    shifted = shift_fourier(fourier[..., 2])
    # obtendo a magnitude da transformada
    magnitude = np.abs(shifted)
    # aplicando logaritmo para melhor visualizacao
    magnitude = (magnitude / np.max(magnitude)) * 1000
    # retornando a magnitude para visualizacao
    return magnitude
