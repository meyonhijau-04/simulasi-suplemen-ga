# ============================================================
# DATA SUPLEMEN DAN KEBUTUHAN NUTRISI HARIAN (RDA)
# Sumber: WHO Vitamin and Mineral Requirements (2004)
# ============================================================

# Daftar suplemen yang tersedia
# Setiap suplemen memiliki:
# - name  : nama suplemen
# - vitC  : kandungan Vitamin C (mg)
# - vitD  : kandungan Vitamin D (IU)
# - zinc  : kandungan Zinc (mg)
# - omega3: kandungan Omega-3 (mg)
# - calcium: kandungan Calcium (mg)
# - iron  : kandungan Iron (mg)
# - price : harga per tablet/kapsul (Rupiah)

SUPPLEMENTS = [
    {"id": 1,  "name": "Vitamin C 500mg",      "vitC": 500,  "vitD": 0,    "zinc": 0,   "omega3": 0,    "calcium": 0,   "iron": 0,   "price": 5000},
    {"id": 2,  "name": "Vitamin D3 400IU",      "vitC": 0,    "vitD": 400,  "zinc": 0,   "omega3": 0,    "calcium": 0,   "iron": 0,   "price": 8000},
    {"id": 3,  "name": "Zinc Tablet 10mg",       "vitC": 0,    "vitD": 0,    "zinc": 10,  "omega3": 0,    "calcium": 0,   "iron": 0,   "price": 6000},
    {"id": 4,  "name": "Fish Oil 1000mg",        "vitC": 0,    "vitD": 0,    "zinc": 0,   "omega3": 1000, "calcium": 0,   "iron": 0,   "price": 12000},
    {"id": 5,  "name": "Multivitamin A",         "vitC": 250,  "vitD": 200,  "zinc": 5,   "omega3": 0,    "calcium": 100, "iron": 8,   "price": 15000},
    {"id": 6,  "name": "Calcium 500mg",          "vitC": 0,    "vitD": 0,    "zinc": 0,   "omega3": 0,    "calcium": 500, "iron": 0,   "price": 7000},
    {"id": 7,  "name": "Iron 14mg",              "vitC": 0,    "vitD": 0,    "zinc": 0,   "omega3": 0,    "calcium": 0,   "iron": 14,  "price": 9000},
    {"id": 8,  "name": "Vitamin C 1000mg",       "vitC": 1000, "vitD": 0,    "zinc": 0,   "omega3": 0,    "calcium": 0,   "iron": 0,   "price": 9000},
    {"id": 9,  "name": "Omega-3 500mg",          "vitC": 0,    "vitD": 0,    "zinc": 0,   "omega3": 500,  "calcium": 0,   "iron": 0,   "price": 10000},
    {"id": 10, "name": "Multivitamin B",         "vitC": 300,  "vitD": 300,  "zinc": 8,   "omega3": 0,    "calcium": 150, "iron": 10,  "price": 18000},
    {"id": 11, "name": "Vitamin D3 1000IU",      "vitC": 0,    "vitD": 1000, "zinc": 0,   "omega3": 0,    "calcium": 0,   "iron": 0,   "price": 11000},
    {"id": 12, "name": "Zinc 25mg",              "vitC": 0,    "vitD": 0,    "zinc": 25,  "omega3": 0,    "calcium": 0,   "iron": 0,   "price": 8500},
    {"id": 13, "name": "Calcium + Vit D",        "vitC": 0,    "vitD": 200,  "zinc": 0,   "omega3": 0,    "calcium": 600, "iron": 0,   "price": 13000},
    {"id": 14, "name": "Iron + Vit C",           "vitC": 100,  "vitD": 0,    "zinc": 0,   "omega3": 0,    "calcium": 0,   "iron": 18,  "price": 11000},
    {"id": 15, "name": "Complete Multivitamin",  "vitC": 500,  "vitD": 400,  "zinc": 10,  "omega3": 0,    "calcium": 200, "iron": 14,  "price": 25000},
]

# Kebutuhan nutrisi harian berdasarkan standar WHO (RDA)
RDA = {
    "vitC":    {"label": "Vitamin C",  "unit": "mg",  "value": 75},
    "vitD":    {"label": "Vitamin D",  "unit": "IU",  "value": 600},
    "zinc":    {"label": "Zinc",       "unit": "mg",  "value": 8},
    "omega3":  {"label": "Omega-3",    "unit": "mg",  "value": 1000},
    "calcium": {"label": "Calcium",    "unit": "mg",  "value": 1000},
    "iron":    {"label": "Iron",       "unit": "mg",  "value": 18},
}

# Daftar kunci nutrisi (dipakai di banyak tempat)
NUTRISI_KEYS = list(RDA.keys())