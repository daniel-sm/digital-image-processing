import numpy as np

def rgb_to_gray(rgb: np.ndarray) -> np.ndarray:
    # coeficientes de luminancia
    r_coeficcient, g_coeficcient, b_coeficcient = 0.299, 0.587, 0.114

    # calculando escala de cinza
    gray = (r_coeficcient * rgb[..., 0]) + (g_coeficcient * rgb[..., 1]) + (b_coeficcient * rgb[..., 2])

    # retornando imagem em escala de cinza
    return gray

def rgb_to_gray_average(rgb: np.ndarray) -> np.ndarray:
    # calculando escala de cinza pela media dos canais
    gray = np.mean(rgb, axis=-1)

    # retornando imagem em escala de cinza
    return gray

def rgb_to_hsi(rgb: np.ndarray) -> np.ndarray:
    # isolando canais rgb
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    # calculando intensidade
    I = (R + G + B) / 3

    # calculando saturacao
    min_rgb = np.min(rgb, axis=-1)
    S = np.zeros_like(I)
    non_black = I > 0
    S[non_black] = 1 - (min_rgb[non_black] / I[non_black])

    # calculando matiz
    num = (R - G) + (R - B)
    den = np.sqrt((R - G)**2 + (R - B)*(G - B))
    den += 1e-10 # evitar divisao por zero
    theta = np.degrees(np.arccos(num / (2 * den)))
    H = np.where(B <= G, theta, 360 - theta)

    return np.stack((H, S, I), axis=-1)

def hsi_to_rgb(hsi: np.ndarray) -> np.ndarray:
    # isolando canais hsi
    H, S, I = hsi[..., 0], hsi[..., 1], hsi[..., 2]

    # inicializando canais rgb
    R = np.zeros_like(H)
    G = np.zeros_like(H)
    B = np.zeros_like(H)

    # convertendo graus para radianos
    H_radians = np.radians(H)

    # caso seja vermelho dominante (0°–120°)
    red = (H < 120)
    B[red] = I[red] * (1 - S[red])
    R[red] = I[red] * (1 + (S[red] * np.cos(H_radians[red]) / np.cos(np.radians(60) - H_radians[red])))
    G[red] = 3 * I[red] - (R[red] + B[red])

    # caso seja verde dominante (120°–240°)
    green = (H >= 120) & (H < 240)
    H2 = np.radians(H[green] - 120)
    R[green] = I[green] * (1 - S[green])
    G[green] = I[green] * (1 + (S[green] * np.cos(H2) / np.cos(np.radians(60) - H2)))
    B[green] = 3 * I[green] - (R[green] + G[green])

    # caso seja azul dominante (240°–360°)
    blue = (H >= 240)
    H3 = np.radians(H[blue] - 240)
    G[blue] = I[blue] * (1 - S[blue])
    B[blue] = I[blue] * (1 + (S[blue] * np.cos(H3) / np.cos(np.radians(60) - H3)))
    R[blue] = 3 * I[blue] - (G[blue] + B[blue])

    # montando imagem
    rgb = np.stack((R, G, B), axis=-1)

    # retornando imagem
    return np.clip(rgb, 0, 1)

def rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    # isolando canais rgb
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    
    # calculando maximo, minimo e delta
    c_max = np.max(rgb, axis=-1)
    c_min = np.min(rgb, axis=-1)
    delta = c_max - c_min

    # inicializando matiz com zeros
    H = np.zeros_like(c_max)

    # mascara de pixels nao cinza
    mask = delta != 0

    # calculando matiz de pixels com vermelho dominante
    red_index = (c_max == R) & mask
    H[red_index] = (60 * ((G[red_index] - B[red_index]) / delta[red_index]) + 360) % 360

    # calculando matiz de pixels com verde dominante
    green_index = (c_max == G) & mask
    H[green_index] = (60 * ((B[green_index] - R[green_index]) / delta[green_index]) + 120) % 360

    # calculando matiz de pixels com azul dominante
    blue_index = (c_max == B) & mask
    H[blue_index] = (60 * ((R[blue_index] - G[blue_index]) / delta[blue_index]) + 240) % 360

    # inicializando saturacao com zeros
    S = np.zeros_like(c_max)

    # mascara de pixels nao pretos
    mask_nonblack = c_max != 0

    # calculando saturacao de pixels nao pretos
    S[mask_nonblack] = delta[mask_nonblack] / c_max[mask_nonblack]

    # calculando valor
    V = c_max

    # montando imagem hsv
    hsv = np.stack((H, S, V), axis=-1)

    # retornando imagem
    return hsv

def hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    # isolando canais hsv
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    # calculando componentes intermediarias
    C = V * S
    X = C * (1 - np.abs((H / 60) % 2 - 1))
    m = V - C

    # criando matriz de zeros
    zeros = np.zeros_like(H)

    # criando as condicoes para cada faixa de matiz
    conditions = [
        (H < 60),
        (H >= 60) & (H < 120),
        (H >= 120) & (H < 180),
        (H >= 180) & (H < 240),
        (H >= 240) & (H < 300),
        (H >= 300),
    ]

    # definindo valores rgb para cada condicao
    rgb_values = np.array([
        (C, X, zeros),
        (X, C, zeros),
        (zeros, C, X),
        (zeros, X, C),
        (X, zeros, C),
        (C, zeros, X),
    ])

    # atribuindo valores rgb conforme as condicoes
    r = np.select(conditions, rgb_values[:, 0])
    g = np.select(conditions, rgb_values[:, 1])
    b = np.select(conditions, rgb_values[:, 2])

    # inicializando rgb com zeros
    rgb = np.stack((r, g, b), axis=-1)

    # ajustando rgb com o valor m 
    rgb += m[..., np.newaxis]

    # retornando a imagem rgb
    return rgb
