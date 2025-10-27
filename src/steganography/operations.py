import numpy as np

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
