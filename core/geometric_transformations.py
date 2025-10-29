import numpy as np

def scale(img: np.ndarray, sx: float, sy: float) -> np.ndarray:
    # obtendo as dimensoes da imagem
    img_height, img_width = img.shape

    # calculando os valores de mapeamento
    x_space = np.linspace(0, img_width - 1, int(sx * img_width))
    y_space = np.linspace(0, img_height - 1, int(sy * img_height))
    x, y = np.meshgrid(x_space, y_space)

    # coordenadas correspondentes na imagem original
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    x1 = np.clip(x0 + 1, 0, img_width - 1)
    y1 = np.clip(y0 + 1, 0, img_height - 1)

    # partes fracionarias
    dx = x - x0
    dy = y - y0

    # obtendo os valores dos pixels vizinhos da imagem original
    p1 = img[y0, x0]
    p2 = img[y0, x1]
    p3 = img[y1, x0]
    p4 = img[y1, x1]

    # interpolacao bilinear dos valores
    i1 = (p1 * (1 - dx)) + (p2 * dx)
    i2 = (p3 * (1 - dx)) + (p4 * dx)
    result = (i1 * (1 - dy)) + (i2 * dy)

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
    
    # calculando os pixels vizinhos para interpolacao
    x0 = np.floor(original_x).astype(int)
    y0 = np.floor(original_y).astype(int)
    x1 = x0 + 1
    y1 = y0 + 1

    # limitando os indices aos limites da imagem original
    x0 = np.clip(x0, 0, img_width - 1)
    y0 = np.clip(y0, 0, img_height - 1)
    x1 = np.clip(x1, 0, img_width - 1)
    y1 = np.clip(y1, 0, img_height - 1)

    # partes fracionarias
    dx = original_x - x0
    dy = original_y - y0

    # obtendo os valores dos pixels vizinhos da imagem original
    p1 = img[y0, x0].astype(np.double)
    p2 = img[y0, x1].astype(np.double)
    p3 = img[y1, x0].astype(np.double)
    p4 = img[y1, x1].astype(np.double)

    # interpolacao bilinear dos valores
    i1 = (p1 * (1 - dx)) + (p2 * dx)
    i2 = (p3 * (1 - dx)) + (p4 * dx)
    result = (i1 * (1 - dy)) + (i2 * dy)

    # obtendo os pixels fora dos limites da imagem original
    outside_bounds = (
        (original_x < 0) | (original_x >= img_width - 1) |
        (original_y < 0) | (original_y >= img_height - 1)
    )
    # preenchendo com 0 os pixels fora dos limites da imagem original
    result[outside_bounds] = 0

    # retornando a imagem interpolada
    return result.astype(img.dtype)

def scale_rgb(img: np.ndarray, sx: float, sy: float) -> np.ndarray:
    # separando os canais de cor
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    # aplicando escala em cada canal
    r_scaled = scale(R, sx, sy)
    g_scaled = scale(G, sx, sy)
    b_scaled = scale(B, sx, sy)

    # recombinando os canais em uma imagem RGB
    result = np.stack((r_scaled, g_scaled, b_scaled), axis=-1)

    return result

def rotate_rgb(img: np.ndarray, angle: float) -> np.ndarray:
    # separando os canais de cor
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    # aplicando rotacao em cada canal
    r_rotated = rotate(R, angle)
    g_rotated = rotate(G, angle)
    b_rotated = rotate(B, angle)

    # recombinando os canais em uma imagem RGB
    result = np.stack((r_rotated, g_rotated, b_rotated), axis=-1)

    return result
