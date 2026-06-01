import random
import time
from genetic_algorithm.fitness import hitung_fitness
from genetic_algorithm.selection import tournament_selection, roulette_selection
from genetic_algorithm.crossover import single_point_crossover, multi_point_crossover
from genetic_algorithm.mutation import mutasi
from data.supplements import NUTRISI_KEYS


def jalankan_ga(suplemen, ukuran_populasi, jumlah_generasi,
                crossover_rate, mutation_rate, max_budget,
                metode_seleksi, metode_crossover):

    jumlah_suplemen = len(suplemen)

    # Normalisasi suplemen — pastikan semua key nutrisi ada
    for s in suplemen:
        for k in NUTRISI_KEYS:
            if k not in s:
                s[k] = 0

    # Validasi awal — jika semua suplemen di atas budget, return early
    ada_yang_terjangkau = any(s["price"] <= max_budget for s in suplemen)
    if not ada_yang_terjangkau:
        return {
            "kromosom_terbaik": [0] * jumlah_suplemen,
            "fitness_terbaik": 0,
            "total_harga": 0,
            "total_nutrisi": {k: 0 for k in NUTRISI_KEYS},
            "suplemen_terpilih": [],
            "riwayat_best": [0] * jumlah_generasi,
            "riwayat_avg": [0] * jumlah_generasi,
            "waktu_eksekusi": 0,
            "generasi_konvergen": 0,
        }

    # Inisialisasi populasi awal
    populasi = []
    for _ in range(ukuran_populasi):
        kromosom = [random.randint(0, 1) for _ in range(jumlah_suplemen)]
        populasi.append(kromosom)

    kromosom_terbaik = None
    fitness_terbaik = -1
    detail_terbaik = None
    generasi_konvergen = 1

    riwayat_best = []
    riwayat_avg = []

    waktu_mulai = time.time()

    for gen in range(jumlah_generasi):

        fitness_scores = []
        semua_detail = []
        for kromosom in populasi:
            score, nutrisi, harga = hitung_fitness(kromosom, suplemen, max_budget)
            fitness_scores.append(score)
            semua_detail.append({"score": score, "nutrisi": nutrisi, "harga": harga})

        max_fitness = max(fitness_scores)
        avg_fitness = sum(fitness_scores) / len(fitness_scores)
        riwayat_best.append(round(max_fitness, 4))
        riwayat_avg.append(round(avg_fitness, 4))

        idx_terbaik = fitness_scores.index(max_fitness)
        if max_fitness > fitness_terbaik:
            fitness_terbaik = max_fitness
            kromosom_terbaik = list(populasi[idx_terbaik])
            detail_terbaik = semua_detail[idx_terbaik]
            generasi_konvergen = gen + 1

        # Seleksi
        if metode_seleksi == "tournament":
            terpilih = tournament_selection(populasi, fitness_scores)
        else:
            terpilih = roulette_selection(populasi, fitness_scores)

        # Guard: pastikan minimal 2 individu untuk crossover
        if len(terpilih) < 2:
            terpilih = terpilih * 2

        # Crossover dan mutasi
        populasi_baru = [list(kromosom_terbaik)]  # Elitisme

        i = 0
        while len(populasi_baru) < ukuran_populasi:
            parent1 = terpilih[i % len(terpilih)]
            parent2 = terpilih[(i + 1) % len(terpilih)]

            if metode_crossover == "single":
                child1, child2 = single_point_crossover(parent1, parent2, crossover_rate)
            else:
                child1, child2 = multi_point_crossover(parent1, parent2, crossover_rate)

            child1 = mutasi(child1, mutation_rate)
            child2 = mutasi(child2, mutation_rate)

            populasi_baru.append(child1)
            if len(populasi_baru) < ukuran_populasi:
                populasi_baru.append(child2)

            i += 2

        populasi = populasi_baru

    waktu_selesai = time.time()
    waktu_eksekusi = round(waktu_selesai - waktu_mulai, 2)

    # Guard: jika semua generasi fitness 0
    if detail_terbaik is None:
        return {
            "kromosom_terbaik": [0] * jumlah_suplemen,
            "fitness_terbaik": 0,
            "total_harga": 0,
            "total_nutrisi": {k: 0 for k in NUTRISI_KEYS},
            "suplemen_terpilih": [],
            "riwayat_best": riwayat_best,
            "riwayat_avg": riwayat_avg,
            "waktu_eksekusi": waktu_eksekusi,
            "generasi_konvergen": 0,
        }

    suplemen_terpilih = []
    for i, gen in enumerate(kromosom_terbaik):
        if gen == 1:
            suplemen_terpilih.append(suplemen[i])

    return {
        "kromosom_terbaik": kromosom_terbaik,
        "fitness_terbaik": round(fitness_terbaik * 100, 2),
        "total_harga": detail_terbaik["harga"],
        "total_nutrisi": detail_terbaik["nutrisi"],
        "suplemen_terpilih": suplemen_terpilih,
        "riwayat_best": riwayat_best,
        "riwayat_avg": riwayat_avg,
        "waktu_eksekusi": waktu_eksekusi,
        "generasi_konvergen": generasi_konvergen,
    }