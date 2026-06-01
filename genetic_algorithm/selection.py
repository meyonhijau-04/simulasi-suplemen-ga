# ============================================================
# FUNGSI SELEKSI
# Memilih individu terbaik dari populasi untuk bereproduksi
# Ada 2 metode: Tournament dan Roulette Wheel
# ============================================================

import random


def tournament_selection(populasi, fitness_scores, tournament_size=3):
    """
    Tournament Selection:
    Pilih beberapa kandidat secara acak,
    lalu yang fitness-nya tertinggi yang menang.

    Parameter:
    - populasi       : list kromosom
    - fitness_scores : list nilai fitness tiap kromosom
    - tournament_size: jumlah kandidat per turnamen

    Return:
    - list kromosom terpilih (ukuran sama dengan populasi)
    """
    terpilih = []

    for _ in range(len(populasi)):
        # Pilih kandidat secara acak
        kandidat_idx = random.sample(range(len(populasi)), tournament_size)

        # Pilih yang fitness-nya tertinggi
        pemenang = max(kandidat_idx, key=lambda i: fitness_scores[i])
        terpilih.append(list(populasi[pemenang]))

    return terpilih


def roulette_selection(populasi, fitness_scores):
    total_fitness = sum(fitness_scores)

    if total_fitness == 0:
        return [list(random.choice(populasi)) for _ in populasi]

    terpilih = []
    for _ in range(len(populasi)):
        nilai_acak = random.uniform(0, total_fitness)
        kumulatif  = 0
        dipilih    = populasi[-1]  # fallback ke yang terakhir
        for i, score in enumerate(fitness_scores):
            kumulatif += score
            if nilai_acak <= kumulatif:
                dipilih = populasi[i]
                break
        terpilih.append(list(dipilih))

    return terpilih