import time

def medir_tempo(func, *args, **kwargs):
    inicio = time.perf_counter()
    func(*args, **kwargs)
    fim = time.perf_counter()
    return fim - inicio

def funcao1(a):
    return a ** 2

def funcao2(a):
    return a * a
