import streamlit as st
import pandas as pd
from pathlib import Path


# ==========================================
# PATH PROJECT
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = (
    BASE_DIR
    / "hasil_deteksi"
    / "data"
    / "hasil_deteksi.csv"
)

VISUAL_DIR = (
    BASE_DIR
    / "hasil_deteksi"
    / "visual"
)


# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Riwayat Hasil | AI-Fish",
    page_icon="🖼️",
    layout="wide"
)


# ==========================================
# LOAD CSS
# ==========================================

try:
    from components.ui import load_css
    load_css()
except Exception:
    pass


# ==========================================
# HEADER
# ==========================================

st.title("🖼️ Riwayat Hasil")

st.write(
    "Menampilkan hasil deteksi ikan yang telah "
    "diproses menggunakan YOLO11n."
)

st.markdown("---")


# ==========================================
# CEK FILE CSV
# ==========================================

if not CSV_PATH.exists():

    st.info(
        "📋 Belum ada riwayat deteksi."
    )

    st.write(
        "Silakan lakukan deteksi terlebih dahulu "
        "pada halaman **Deteksi Ikan**."
    )

    st.stop()


# ==========================================
# BACA CSV
# ==========================================

try:

    df = pd.read_csv(CSV_PATH)

except Exception as e:

    st.error(
        f"❌ Gagal membaca data: {e}"
    )

    st.stop()


# ==========================================
# CEK DATA
# ==========================================

if df.empty:

    st.info(
        "📋 Riwayat deteksi masih kosong."
    )

    st.stop()


# ==========================================
# FUNGSI HAPUS HASIL
# ==========================================

def delete_detection_file(filename):

    global df

    # --------------------------------------
    # Hapus data dari DataFrame
    # --------------------------------------

    df = df[
        df["File"] != filename
    ].copy()


    # --------------------------------------
    # Simpan kembali CSV
    # --------------------------------------

    df.to_csv(
        CSV_PATH,
        index=False
    )


    # --------------------------------------
    # Hapus gambar hasil deteksi
    # --------------------------------------

    visual_path = (
        VISUAL_DIR
        / f"hasil_{filename}"
    )

    if visual_path.exists():

        visual_path.unlink()


    return True


# ==========================================
# FILTER
# ==========================================

st.subheader("🔍 Filter Riwayat")

col1, col2 = st.columns(2)


# ==========================================
# FILTER KELAS
# ==========================================

with col1:

    classes = sorted(
        df["Kelas Ikan"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_class = st.selectbox(
        "Kelas Ikan",
        ["Semua Kelas"] + classes
    )


# ==========================================
# FILTER FILE
# ==========================================

with col2:

    files = sorted(
        df["File"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_file = st.selectbox(
        "Nama File",
        ["Semua File"] + files
    )


# ==========================================
# TERAPKAN FILTER
# ==========================================

filtered_df = df.copy()


if selected_class != "Semua Kelas":

    filtered_df = filtered_df[
        filtered_df["Kelas Ikan"]
        == selected_class
    ]


if selected_file != "Semua File":

    filtered_df = filtered_df[
        filtered_df["File"]
        == selected_file
    ]


# ==========================================
# RINGKASAN
# ==========================================

st.markdown("---")

st.subheader("📊 Ringkasan")

total_records = len(
    filtered_df
)

total_files = filtered_df[
    "File"
].nunique()


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Data",
        total_records
    )


with col2:

    st.metric(
        "Total File",
        total_files
    )


with col3:

    if not filtered_df.empty:

        avg_confidence = (
            filtered_df["Confidence"]
            .astype(str)
            .str.replace(
                "%",
                "",
                regex=False
            )
            .astype(float)
            .mean()
        )

        st.metric(
            "Rata-rata Confidence",
            f"{avg_confidence:.2f}%"
        )

    else:

        st.metric(
            "Rata-rata Confidence",
            "0%"
        )


# ==========================================
# TABEL RIWAYAT
# ==========================================

st.markdown("---")

st.subheader(
    "📋 Data Riwayat Deteksi"
)


if filtered_df.empty:

    st.info(
        "Tidak ada data yang sesuai dengan filter."
    )

else:

    display_df = filtered_df[
        [
            "Waktu",
            "File",
            "Kelas Ikan",
            "Confidence"
        ]
    ].copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# GALERI HASIL DETEKSI
# ==========================================

st.markdown("---")

st.subheader(
    "📸 Hasil Visual Deteksi"
)

st.write(
    "Gambar hasil bounding box yang telah "
    "disimpan oleh sistem."
)


# ==========================================
# CARI GAMBAR
# ==========================================

if selected_file != "Semua File":

    gallery_images = [
        VISUAL_DIR / f"hasil_{selected_file}"
    ]

else:

    gallery_images = []

    if VISUAL_DIR.exists():

        for image_path in VISUAL_DIR.iterdir():

            if image_path.suffix.lower() in [
                ".jpg",
                ".jpeg",
                ".png"
            ]:

                gallery_images.append(
                    image_path
                )


# ==========================================
# FILTER FILE YANG ADA
# ==========================================

gallery_images = [
    image
    for image in gallery_images
    if image.exists()
]


# ==========================================
# URUTKAN TERBARU
# ==========================================

gallery_images.sort(
    key=lambda x: x.stat().st_mtime,
    reverse=True
)


# ==========================================
# TAMPILKAN GALERI
# ==========================================

if gallery_images:

    gallery_cols = st.columns(3)


    for index, image_path in enumerate(
        gallery_images
    ):

        with gallery_cols[index % 3]:

            # ------------------------------
            # TAMPILKAN GAMBAR
            # ------------------------------

            st.image(
                str(image_path),
                caption=image_path.name,
                use_container_width=True
            )


            # ------------------------------
            # NAMA FILE ASLI
            # ------------------------------

            filename = image_path.name

            if filename.startswith("hasil_"):

                original_filename = (
                    filename[len("hasil_"):]
                )

            else:

                original_filename = filename


            st.caption(
                f"📄 {original_filename}"
            )


            # ------------------------------
            # TOMBOL HAPUS
            # ------------------------------

            delete_key = (
                f"delete_{original_filename}"
            )


            if st.button(
                "🗑️ Hapus Hasil",
                key=delete_key,
                use_container_width=True
            ):

                st.session_state[
                    "confirm_delete"
                ] = original_filename


# ==========================================
# KONFIRMASI HAPUS
# ==========================================

if (
    "confirm_delete"
    in st.session_state
):

    filename_to_delete = (
        st.session_state[
            "confirm_delete"
        ]
    )


    st.markdown("---")

    st.warning(
        f"⚠️ Anda akan menghapus seluruh "
        f"hasil deteksi untuk file: "
        f"**{filename_to_delete}**"
    )


    st.write(
        "Data riwayat dan gambar hasil deteksi "
        "untuk file tersebut akan dihapus."
    )


    confirm_col1, confirm_col2 = (
        st.columns(2)
    )


    # ======================================
    # BATAL
    # ======================================

    with confirm_col1:

        if st.button(
            "↩️ Batal",
            use_container_width=True
        ):

            del st.session_state[
                "confirm_delete"
            ]

            st.rerun()


    # ======================================
    # KONFIRMASI HAPUS
    # ======================================

    with confirm_col2:

        if st.button(
            "🗑️ Ya, Hapus Hasil",
            type="primary",
            use_container_width=True
        ):

            try:

                delete_detection_file(
                    filename_to_delete
                )


                # --------------------------
                # HAPUS SESSION
                # --------------------------

                del st.session_state[
                    "confirm_delete"
                ]


                # --------------------------
                # PESAN SUKSES
                # --------------------------

                st.success(
                    f"✅ Hasil deteksi "
                    f"**{filename_to_delete}** "
                    f"berhasil dihapus."
                )


                # --------------------------
                # REFRESH
                # --------------------------

                st.rerun()


            except Exception as e:

                st.error(
                    f"❌ Gagal menghapus hasil: "
                    f"{e}"
                )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "AI-Fish • YOLO11n Computer Vision"
)