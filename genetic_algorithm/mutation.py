# ============================================================
# FUNGSI MUTASI
# Mengubah gen secara acak untuk menjaga keberagaman populasi
# dan mencegah konvergensi terlalu cepat (premature convergence)
# ============================================================

import random


def mutasi(kromosom, mutation_rate):
    """
    Flip Bit Mutation:
    Setiap gen berpeluang berubah (0 jadi 1 atau 1 jadi 0)
    sesuai probabilitas mutasi.

    Parameter:
    - kromosom     : list biner [1,0,1,0,...]
    - mutation_rate: probabilitas mutasi per gen (0.0 - 1.0)

    Return:
    - kromosom baru setelah mutasi
    """
    hasil = []
    for gen in kromosom:
        if random.random() < mutation_rate:
            # Flip: 0 jadi 1, atau 1 jadi 0
            hasil.append(1 if gen == 0 else 0)
        else:
            hasil.append(gen)
    return hasil