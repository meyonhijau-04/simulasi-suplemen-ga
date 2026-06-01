// ============================================================
// MAIN.JS
// Logika JavaScript untuk halaman simulasi GA Suplemen
// ============================================================

// Nilai RDA harian standar WHO
const rdaVal = {
    vitC: 75, vitD: 600, zinc: 8,
    omega3: 1000, calcium: 1000, iron: 18
};

const nutrisiLabel = {
    vitC: "Vitamin C", vitD: "Vitamin D",
    zinc: "Zinc", omega3: "Omega-3",
    calcium: "Calcium", iron: "Iron"
};

const nutrisiUnit = {
    vitC: "mg", vitD: "IU", zinc: "mg",
    omega3: "mg", calcium: "mg", iron: "mg"
};

// Simpan riwayat untuk export grafik
window.riwayatBest = [];
window.riwayatAvg  = [];

// ============================================================
// UPDATE PREVIEW TOMBOL JALANKAN
// ============================================================
function updatePreview() {
    const budget = parseInt(
        document.getElementById("maxBudget").value
    ) || 0;
    const jml = dataSuplemenList.length;
    const pop = parseInt(
        document.getElementById("populationSize").value
    ) || 50;
    const gen = parseInt(
        document.getElementById("generations").value
    ) || 100;

    const el1 = document.getElementById("preview-budget");
    const el2 = document.getElementById("total-suplemen-btn");
    const el3 = document.getElementById("total-kombinasi");

    if (el1) el1.innerText = budget.toLocaleString("id-ID");
    if (el2) el2.innerText = jml;
    if (el3) el3.innerText = (pop * gen).toLocaleString("id-ID");
}

// ============================================================
// RENDER TABEL SUPLEMEN
// ============================================================
function renderTabel() {
    const tbody = document.getElementById("bodySuplemen");
    if (!tbody) return;
    tbody.innerHTML = "";

    dataSuplemenList.forEach((s, i) => {
        tbody.innerHTML += `
            <tr>
                <td>${i + 1}</td>
                <td>${s.name}</td>
                <td>${s.vitC    > 0 ? s.vitC    : "—"}</td>
                <td>${s.vitD    > 0 ? s.vitD    : "—"}</td>
                <td>${s.zinc    > 0 ? s.zinc    : "—"}</td>
                <td>${s.omega3  > 0 ? s.omega3  : "—"}</td>
                <td>${s.calcium > 0 ? s.calcium : "—"}</td>
                <td>${s.iron    > 0 ? s.iron    : "—"}</td>
                <td>Rp ${s.price.toLocaleString("id-ID")}</td>
                <td>
                    <button class="btn btn-danger"
                        onclick="hapusSuplemen(${i})">
                        Hapus
                    </button>
                </td>
            </tr>
        `;
    });

    const el = document.getElementById("jml-suplemen");
    if (el) el.innerText = dataSuplemenList.length;
    updatePreview();
}

// ============================================================
// TOGGLE FORM TAMBAH
// ============================================================
function toggleFormTambah() {
    const form = document.getElementById("formTambah");
    form.style.display =
        form.style.display === "none" ? "block" : "none";
    document.getElementById("errorTambah").style.display = "none";
}

// ============================================================
// TAMBAH SUPLEMEN
// ============================================================
function tambahSuplemen() {
    const nama  = document.getElementById("inp-name").value.trim();
    const harga = parseFloat(
        document.getElementById("inp-price").value
    );
    const err = document.getElementById("errorTambah");

    if (!nama) {
        err.style.display = "block";
        err.innerText     = "Nama suplemen wajib diisi.";
        return;
    }
    if (!harga || harga <= 0) {
        err.style.display = "block";
        err.innerText     = "Harga harus lebih dari 0.";
        return;
    }

    dataSuplemenList.push({
        id:      Date.now(),
        name:    nama,
        vitC:    parseFloat(
            document.getElementById("inp-vitC").value)    || 0,
        vitD:    parseFloat(
            document.getElementById("inp-vitD").value)    || 0,
        zinc:    parseFloat(
            document.getElementById("inp-zinc").value)    || 0,
        omega3:  parseFloat(
            document.getElementById("inp-omega3").value)  || 0,
        calcium: parseFloat(
            document.getElementById("inp-calcium").value) || 0,
        iron:    parseFloat(
            document.getElementById("inp-iron").value)    || 0,
        price:   harga,
    });

    err.style.display = "none";
    document.getElementById("inp-name").value  = "";
    document.getElementById("inp-price").value = "0";
    toggleFormTambah();
    renderTabel();
}

// ============================================================
// HAPUS SUPLEMEN
// ============================================================
function hapusSuplemen(index) {
    if (confirm("Hapus suplemen ini dari daftar?")) {
        dataSuplemenList.splice(index, 1);
        renderTabel();
    }
}

// ============================================================
// JALANKAN SIMULASI GA
// ============================================================
async function jalankanSimulasi() {

    if (dataSuplemenList.length < 2) {
        document.getElementById("hasilArea").style.display  = "none";
        document.getElementById("loading").style.display    = "none";

        // Tampilkan pesan error di halaman bukan alert popup
        const box = document.getElementById("jalankan-error");
        if (box) {
            box.style.display = "block";
            box.innerText =
                "Daftar suplemen kosong atau kurang dari 2. " +
                "Pastikan data suplemen sudah tersedia di tabel " +
                "sebelum menjalankan simulasi.";
        }
        return;
    }

    // Sembunyikan error jika ada
    const errBox = document.getElementById("jalankan-error");
    if (errBox) errBox.style.display = "none";

    // Tampilkan loading
    document.getElementById("loading").style.display    = "block";
    document.getElementById("hasilArea").style.display  = "none";
    document.getElementById("btnJalankan").disabled     = true;
    document.getElementById("btnJalankan").innerText    =
        "Sedang memproses...";

    // Kumpulkan semua parameter
    const params = {
        populationSize:  parseInt(
            document.getElementById("populationSize").value) || 50,
        generations:     parseInt(
            document.getElementById("generations").value)    || 100,
        crossoverRate:   parseFloat(
            document.getElementById("crossoverRate").value)  || 0.8,
        mutationRate:    parseFloat(
            document.getElementById("mutationRate").value)   || 0.05,
        maxBudget:       parseInt(
            document.getElementById("maxBudget").value)      || 50000,
        selectionMethod:
            document.getElementById("selectionMethod").value,
        crossoverMethod:
            document.getElementById("crossoverMethod").value,
        suplemen: dataSuplemenList,
    };

    // Kirim ke Flask
    const response = await fetch("/run", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(params),
    });

    const data  = await response.json();
    const hasil = data.hasil;

    // Simpan riwayat untuk export
    window.riwayatBest = hasil.riwayat_best;
    window.riwayatAvg  = hasil.riwayat_avg;

    // Sembunyikan loading, tampilkan hasil
    document.getElementById("loading").style.display    = "none";
    document.getElementById("btnJalankan").disabled     = false;
    document.getElementById("btnJalankan").innerText    =
        "Jalankan Simulasi Genetic Algorithm";
    document.getElementById("hasilArea").style.display  = "block";

    // ---- GRAFIK PLOTLY ----
    const grafikData = JSON.parse(data.grafik);
    Plotly.newPlot(
        "grafik",
        grafikData.data,
        grafikData.layout,
        { responsive: true }
    );

    // ---- SKOR FITNESS ----
    document.getElementById("fitness-angka").innerText =
        hasil.fitness_terbaik + "%";

    // ---- SUBJUDUL ----
    document.getElementById("subjudul-hasil").innerText =
        hasil.suplemen_terpilih.length +
        " suplemen dipilih  ·  Total Rp " +
        hasil.total_harga.toLocaleString("id-ID");

    // Tampilkan metrik GA
document.getElementById("metrik-ga").innerHTML = `
    <div class="metrik-item">
        <span class="metrik-label">Waktu eksekusi</span>
        <span class="metrik-val">${hasil.waktu_eksekusi} detik</span>
    </div>
    <div class="metrik-item">
        <span class="metrik-label">Konvergen pada generasi</span>
        <span class="metrik-val">${hasil.generasi_konvergen}</span>
    </div>
    <div class="metrik-item">
        <span class="metrik-label">Total iterasi</span>
        <span class="metrik-val">${hasil.riwayat_best.length} generasi</span>
    </div>
    <div class="metrik-item">
        <span class="metrik-label">Skor fitness terbaik</span>
        <span class="metrik-val">${hasil.fitness_terbaik}%</span>
    </div>
`;


    // ---- SUPLEMEN TERPILIH ----
    let htmlSuplemen = "";
    if (hasil.suplemen_terpilih.length === 0) {
        htmlSuplemen = `
            <div class="alert alert-warning">
                Tidak ada kombinasi yang memenuhi budget ini.
                Coba naikkan budget atau tambah suplemen
                yang lebih terjangkau.
            </div>
        `;
    } else {
        hasil.suplemen_terpilih.forEach(s => {
            htmlSuplemen += `
                <div class="suplemen-item">
                    <span class="suplemen-nama">${s.name}</span>
                    <span class="suplemen-harga">
                        Rp ${s.price.toLocaleString("id-ID")}
                    </span>
                </div>
            `;
        });
    }
    document.getElementById("suplemen-terpilih").innerHTML =
        htmlSuplemen;

    // ---- NUTRISI PROGRESS BAR ----
    let htmlNutrisi      = "";
    let jmlTerpenuhi     = 0;
    let daftarKurang     = [];

    Object.keys(rdaVal).forEach(k => {
        const jumlah = hasil.total_nutrisi[k] || 0;
        const pct    = Math.min(
            (jumlah / rdaVal[k]) * 100, 100
        );
        const pctStr = pct.toFixed(1);

        let warna, status, statusClass;
        if (pct >= 100) {
            warna       = "#34d399";
            status      = "Terpenuhi sepenuhnya";
            statusClass = "status-green";
            jmlTerpenuhi++;
        } else if (pct >= 50) {
            warna       = "#4f8ef7";
            status      = "Sebagian terpenuhi (" + pctStr + "%)";
            statusClass = "status-blue";
        } else if (pct > 0) {
            warna       = "#fb923c";
            status      = "Masih kurang (" + pctStr + "%)";
            statusClass = "status-orange";
            daftarKurang.push(nutrisiLabel[k]);
        } else {
            warna       = "#555d78";
            status      = "Tidak terpenuhi";
            statusClass = "status-gray";
            daftarKurang.push(nutrisiLabel[k]);
        }

        htmlNutrisi += `
            <div class="nutrisi-item">
                <div class="nutrisi-header">
                    <span class="nutrisi-nama">
                        ${nutrisiLabel[k]}
                    </span>
                    <span class="nutrisi-angka"
                        style="color: ${warna};">
                        ${jumlah}${nutrisiUnit[k]}
                        dari ${rdaVal[k]}${nutrisiUnit[k]}
                    </span>
                </div>
                <div class="progress-bar-wrap">
                    <div class="progress-bar-fill"
                        style="width:${pctStr}%;
                               background:${warna};">
                    </div>
                </div>
                <div class="nutrisi-status ${statusClass}">
                    ${status}
                </div>
            </div>
        `;
    });
    document.getElementById("nutrisi-bars").innerHTML =
        htmlNutrisi;

    // ---- KESIMPULAN ----
    let kesimpulan = "";
    if (hasil.fitness_terbaik >= 90) {
        kesimpulan = `
            <div class="alert alert-success">
                Hasil sangat baik. ${jmlTerpenuhi} dari 6 nutrisi
                harian sudah terpenuhi sepenuhnya dengan budget
                yang kamu miliki. Kombinasi ini sangat direkomendasikan.
            </div>
        `;
    } else if (hasil.fitness_terbaik >= 60) {
        const kurang = daftarKurang.length > 0
            ? " Nutrisi yang belum optimal: " +
              daftarKurang.join(", ") + "."
            : "";
        kesimpulan = `
            <div class="alert alert-info">
                Hasil cukup baik. ${jmlTerpenuhi} dari 6 nutrisi
                terpenuhi sepenuhnya.${kurang}
                Pertimbangkan menaikkan budget untuk hasil lebih
                optimal.
            </div>
        `;
    } else {
        const kurang = daftarKurang.length > 0
            ? " Nutrisi yang perlu ditambah: " +
              daftarKurang.join(", ") + "."
            : "";
        kesimpulan = `
            <div class="alert alert-warning">
                Budget saat ini belum cukup untuk memenuhi semua
                kebutuhan nutrisi harian.${kurang}
                Disarankan menaikkan budget atau menambahkan
                suplemen multivitamin lengkap ke dalam daftar.
            </div>
        `;
    }
    document.getElementById("kesimpulan-box").innerHTML =
        kesimpulan;

    // ---- KROMOSOM ----
    let htmlKromosom = "";
    hasil.kromosom_terbaik.forEach((gen, i) => {
        const nama = dataSuplemenList[i]
            ? dataSuplemenList[i].name : "";
        htmlKromosom += `
            <div class="gen-box gen-${gen}"
                title="${nama}">${gen}</div>
        `;
    });
    document.getElementById("kromosom-display").innerHTML =
        htmlKromosom;

    // Scroll ke hasil
    document.getElementById("hasilArea").scrollIntoView({
        behavior: "smooth", block: "start"
    });
}

// ============================================================
// DOWNLOAD GRAFIK PNG
// ============================================================
async function downloadGrafik() {
    const btn     = document.getElementById("btnDownload");
    btn.disabled  = true;
    btn.innerText = "Menyiapkan...";

    const response = await fetch("/export-grafik", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            riwayat_best: window.riwayatBest,
            riwayat_avg:  window.riwayatAvg,
        }),
    });

    const data = await response.json();

    if (data.status === "success") {
        const notif         = document.getElementById(
            "notif-download"
        );
        notif.style.display = "block";
        notif.innerText     =
            "Grafik berhasil disimpan di: " + data.filepath;
    }

    btn.disabled  = false;
    btn.innerText = "Simpan PNG";
}

// ============================================================
// INISIALISASI
// ============================================================
document.addEventListener("DOMContentLoaded", function () {

    // Pasang event listener untuk update preview
    const inputBudget = document.getElementById("maxBudget");
    const inputPop    = document.getElementById("populationSize");
    const inputGen    = document.getElementById("generations");

    if (inputBudget) {
        inputBudget.addEventListener("input", updatePreview);
    }
    if (inputPop) {
        inputPop.addEventListener("input", updatePreview);
    }
    if (inputGen) {
        inputGen.addEventListener("input", updatePreview);
    }

    // Render tabel dan preview awal
    renderTabel();
    updatePreview();
});