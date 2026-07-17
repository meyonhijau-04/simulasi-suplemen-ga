# ============================================================
# APP.PY — File utama Flask
# Jalankan dengan : python app.py
# Buka browser di : http://127.0.0.1:5000
# ============================================================

from flask import Flask, render_template, request, jsonify
from data.supplements import SUPPLEMENTS, RDA, NUTRISI_KEYS
from genetic_algorithm.ga import jalankan_ga
import plotly.graph_objects as go
import plotly.io as pio
import os

app = Flask(__name__)


# -------------------------------------------------------
# ROUTE: Halaman Utama
# -------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------------------------------
# ROUTE: Halaman Simulasi
# -------------------------------------------------------
@app.route("/simulation")
def simulation():
    return render_template("simulation.html",
                           suplemen=SUPPLEMENTS,
                           rda=RDA)


# -------------------------------------------------------
# ROUTE: Jalankan GA
# -------------------------------------------------------
@app.route("/run", methods=["POST"])
def run_ga():
    data = request.get_json()

    ukuran_populasi  = int(data.get("populationSize", 50))
    jumlah_generasi  = int(data.get("generations", 100))
    crossover_rate   = float(data.get("crossoverRate", 0.8))
    mutation_rate    = float(data.get("mutationRate", 0.05))
    max_budget       = int(data.get("maxBudget", 50000))
    metode_seleksi   = data.get("selectionMethod", "tournament")
    metode_crossover = data.get("crossoverMethod", "single")
    suplemen_data    = data.get("suplemen", SUPPLEMENTS)

    # Normalisasi suplemen dari frontend
    for s in suplemen_data:
        for k in NUTRISI_KEYS:
            if k not in s:
                s[k] = 0
        if "price" not in s:
            s["price"] = 0

    # Jalankan algoritma GA
    hasil = jalankan_ga(
        suplemen=suplemen_data,
        ukuran_populasi=ukuran_populasi,
        jumlah_generasi=jumlah_generasi,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        max_budget=max_budget,
        metode_seleksi=metode_seleksi,
        metode_crossover=metode_crossover,
    )

    # Buat grafik Plotly untuk web
    generasi = list(range(1, jumlah_generasi + 1))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=generasi,
        y=[v * 100 for v in hasil["riwayat_best"]],
        mode="lines",
        name="Fitness Terbaik",
        line=dict(color="#4f8ef7", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(79,142,247,0.06)"
    ))

    fig.add_trace(go.Scatter(
        x=generasi,
        y=[v * 100 for v in hasil["riwayat_avg"]],
        mode="lines",
        name="Fitness Rata-rata",
        line=dict(color="#34d399", width=1.5, dash="dash")
    ))

    fig.update_layout(
        title=dict(
            text="Evolusi Fitness per Generasi",
            font=dict(size=14, color="#f1f3f9"),
            x=0
        ),
        xaxis=dict(
            title="Generasi ke-",
            color="#8b92a9",
            gridcolor="#2e3348",
            zerolinecolor="#2e3348",
            range=[1, jumlah_generasi]
        ),
        yaxis=dict(
            title="Nilai Fitness (%)",
            color="#8b92a9",
            gridcolor="#2e3348",
            zerolinecolor="#2e3348",
            range=[0, 105]
        ),
        plot_bgcolor="#1e2130",
        paper_bgcolor="#1e2130",
        font=dict(
            family="Inter, sans-serif",
            size=12,
            color="#8b92a9"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(color="#f1f3f9")
        ),
        margin=dict(l=50, r=20, t=60, b=50),
    )

    grafik_json = fig.to_json()

    return jsonify({
        "hasil":  hasil,
        "grafik": grafik_json,
        "rda":    RDA,
    })


# -------------------------------------------------------
# ROUTE: Export Grafik PNG untuk Laporan
# -------------------------------------------------------
@app.route("/export-grafik", methods=["POST"])
def export_grafik():
    data         = request.get_json()
    riwayat_best = data.get("riwayat_best", [])
    riwayat_avg  = data.get("riwayat_avg", [])

    if not riwayat_best:
        return jsonify({
            "status": "error",
            "pesan":  "Tidak ada data grafik"
        }), 400

    generasi = list(range(1, len(riwayat_best) + 1))
    best_pct  = [v * 100 for v in riwayat_best]
    avg_pct   = [v * 100 for v in riwayat_avg]

    # Buat grafik PNG berkualitas tinggi untuk laporan
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=generasi,
        y=best_pct,
        mode="lines",
        name="Fitness Terbaik",
        line=dict(color="#6d28d9", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(109,40,217,0.08)"
    ))

    fig.add_trace(go.Scatter(
        x=generasi,
        y=avg_pct,
        mode="lines",
        name="Fitness Rata-rata",
        line=dict(color="#10b981", width=2, dash="dash")
    ))

    fig.update_layout(
        title=dict(
            text="Evolusi Fitness Genetic Algorithm<br>"
                 "<sub>Optimasi Kombinasi Suplemen Kesehatan Harian</sub>",
            font=dict(size=14),
            x=0
        ),
        xaxis=dict(
            title="Generasi ke-",
            gridcolor="#e5e7eb",
            range=[1, len(generasi)]
        ),
        yaxis=dict(
            title="Nilai Fitness (%)",
            gridcolor="#e5e7eb",
            range=[0, 105]
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="left",
            x=0
        ),
        margin=dict(l=60, r=40, t=80, b=60),
        width=900,
        height=500,
    )

    # Pastikan folder static/img/ ada
    img_folder = os.path.join(app.root_path, "static", "img")
    os.makedirs(img_folder, exist_ok=True)

    # Simpan PNG ke static/img/
    filepath = os.path.join(img_folder, "grafik_evolusi_fitness.png")
    pio.write_image(fig, filepath, format="png", scale=2)

    return jsonify({
        "status":   "success",
        "filepath": "static/img/grafik_evolusi_fitness.png",
        "pesan":    "Grafik berhasil disimpan"
    })


# -------------------------------------------------------
# ROUTE: Cara Pakai
# -------------------------------------------------------
@app.route("/how-to-use")
def how_to_use():
    return render_template("how_to_use.html")


# -------------------------------------------------------
# ROUTE: Tentang
# -------------------------------------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -------------------------------------------------------
# Jalankan server Flask
# -------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
