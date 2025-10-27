import numpy as np

def bit_slice(img: np.ndarray, k: np.uint8) -> np.ndarray:
    return img & (2 ** (k - 1))

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
