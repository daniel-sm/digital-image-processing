import time

def medir_tempo(func, *args, **kwargs):
    inicio = time.perf_counter()
    func(*args, **kwargs)
    fim = time.perf_counter()
    return fim - inicio

def funcao1():
    return sum(range(1_000_000))

def funcao2():
    s = 0
    for i in range(1_000_000):
        s += i
    return s
