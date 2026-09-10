import csv
from pathlib import Path


# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = (
    BASE_DIR
    / "hasil_deteksi"
    / "data"
    / "hasil_deteksi.csv"
)

BACKUP_PATH = (
    BASE_DIR
    / "hasil_deteksi"
    / "data"
    / "hasil_deteksi_backup.csv"
)


# =========================================================
# CEK FILE
# =========================================================

if not CSV_PATH.exists():

    print("❌ File CSV tidak ditemukan.")

    raise SystemExit


# =========================================================
# BACKUP
# =========================================================

BACKUP_PATH.write_bytes(
    CSV_PATH.read_bytes()
)

print(
    f"✅ Backup dibuat:\n"
    f"{BACKUP_PATH}"
)


# =========================================================
# BACA CSV LAMA
# =========================================================

rows = []

with open(
    CSV_PATH,
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.reader(file)

    for row in reader:

        # Lewati baris kosong
        if not row:
            continue

        # Lewati header lama
        if row[0] == "Waktu":
            continue

        # -------------------------------------------------
        # FORMAT LAMA
        # -------------------------------------------------

        if len(row) == 4:

            rows.append([
                row[0],     # Waktu
                row[1],     # File
                row[2],     # Kelas Ikan
                row[3],     # Confidence
                "-",        # X1
                "-",        # Y1
                "-",        # X2
                "-"         # Y2
            ])

        # -------------------------------------------------
        # FORMAT BARU
        # -------------------------------------------------

        elif len(row) == 8:

            rows.append(row)

        # -------------------------------------------------
        # FORMAT TIDAK DIKENAL
        # -------------------------------------------------

        else:

            print(
                "⚠️ Baris dilewati karena format tidak dikenal:"
            )

            print(row)


# =========================================================
# HAPUS DUPLIKAT IDENTIK
# =========================================================

unique_rows = []

seen = set()

for row in rows:

    row_tuple = tuple(row)

    if row_tuple not in seen:

        seen.add(row_tuple)

        unique_rows.append(row)


# =========================================================
# TULIS CSV BARU
# =========================================================

with open(
    CSV_PATH,
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Waktu",
        "File",
        "Kelas Ikan",
        "Confidence",
        "X1",
        "Y1",
        "X2",
        "Y2"
    ])

    writer.writerows(
        unique_rows
    )


# =========================================================
# HASIL
# =========================================================

print()
print("======================================")
print("✅ CSV BERHASIL DIPERBAIKI")
print("======================================")

print(
    f"Data sebelum : {len(rows)}"
)

print(
    f"Data sesudah : {len(unique_rows)}"
)

print(
    f"Backup       : {BACKUP_PATH.name}"
)

print()
print(
    "Sekarang semua data menggunakan "
    "format 8 kolom."
)