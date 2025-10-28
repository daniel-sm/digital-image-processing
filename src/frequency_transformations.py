import numpy as np

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
