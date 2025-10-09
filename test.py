import time

def medir_tempo(func, *args, **kwargs):
    inicio = time.perf_counter()
    func(*args, **kwargs)
    fim = time.perf_counter()
    return fim - inicio

# Exemplos de funções para comparar
def funcao1():
    return sum(range(1_000_000))

def funcao2():
    s = 0
    for i in range(1_000_000):
        s += i
    return s

# Medindo o tempo das duas funções
t1 = medir_tempo(funcao1)
t2 = medir_tempo(funcao2)

print(f"Tempo da função 1: {t1} segundos")
print(f"Tempo da função 2: {t2} segundos")  
