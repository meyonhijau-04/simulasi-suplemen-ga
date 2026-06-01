# ============================================================
# FUNGSI CROSSOVER
# Menukar gen antara dua parent untuk menghasilkan offspring baru
# Ada 2 metode: Single-point dan Multi-point
# ============================================================

import random


def single_point_crossover(parent1, parent2, crossover_rate):
    """
    Single-point Crossover:
    Potong di satu titik acak, tukar bagian setelah titik tersebut.

    Contoh:
    Parent1: [1,0,1,1,0]
    Parent2: [0,1,0,0,1]
    Titik  : 2
    Child1 : [1,0,0,0,1]
    Child2 : [0,1,1,1,0]
    """
    # Jika angka acak lebih besar dari crossover_rate, tidak jadi crossover
    if random.random() > crossover_rate:
        return list(parent1), list(parent2)

    # Tentukan titik potong secara acak
    titik = random.randint(1, len(parent1) - 1)

    child1 = parent1[:titik] + parent2[titik:]
    child2 = parent2[:titik] + parent1[titik:]

    return child1, child2


def multi_point_crossover(parent1, parent2, crossover_rate):
    """
    Multi-point Crossover:
    Potong di dua titik acak, tukar bagian di antara dua titik tersebut.

    Contoh:
    Parent1: [1,0,1,1,0,1]
    Parent2: [0,1,0,0,1,0]
    Titik  : 2 dan 4
    Child1 : [1,0,0,0,0,1]
    Child2 : [0,1,1,1,1,0]
    """
    if random.random() > crossover_rate:
        return list(parent1), list(parent2)

    # Tentukan dua titik potong
    titik1 = random.randint(1, len(parent1) - 2)
    titik2 = random.randint(titik1 + 1, len(parent1) - 1)

    child1 = parent1[:titik1] + parent2[titik1:titik2] + parent1[titik2:]
    child2 = parent2[:titik1] + parent1[titik1:titik2] + parent2[titik2:]

    return child1, child2