# ============================================================
# FUNGSI FITNESS
# Menilai seberapa baik suatu kombinasi suplemen
# memenuhi kebutuhan nutrisi harian dengan budget tertentu
# ============================================================

from data.supplements import RDA, NUTRISI_KEYS


def hitung_fitness(kromosom, suplemen, max_budget):
    """
    Menghitung nilai fitness dari satu kromosom.

    Parameter:
    - kromosom   : list biner [0,1,1,0,...] — 1 berarti suplemen dipilih
    - suplemen   : list data suplemen
    - max_budget : batas maksimal harga total (Rupiah)

    Return:
    - score      : nilai fitness antara 0.0 sampai 1.0
    - total_nutrisi : dict jumlah nutrisi yang terpenuhi
    - total_harga   : total harga suplemen yang dipilih
    """

    # Hitung total nutrisi dan harga dari suplemen yang dipilih
    total_nutrisi = {k: 0 for k in NUTRISI_KEYS}
    total_harga = 0

    for i, gen in enumerate(kromosom):
        if gen == 1:  # gen bernilai 1 berarti suplemen ini dipilih
            s = suplemen[i]
            total_harga += s["price"]
            for k in NUTRISI_KEYS:
                total_nutrisi[k] += s[k]

    # Jika total harga melebihi budget, fitness langsung 0
    if total_harga > max_budget:
        return 0.0, total_nutrisi, total_harga

    # Hitung rata-rata pemenuhan nutrisi (maksimal 100% per nutrisi)
    skor_total = 0
    for k in NUTRISI_KEYS:
        pemenuhan = min(total_nutrisi[k] / RDA[k]["value"], 1.0)
        skor_total += pemenuhan

    # Fitness = rata-rata pemenuhan semua nutrisi (0.0 - 1.0)
    score = skor_total / len(NUTRISI_KEYS)

    return score, total_nutrisi, total_harga