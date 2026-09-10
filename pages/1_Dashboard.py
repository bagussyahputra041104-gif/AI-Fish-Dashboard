import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt


# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = (
    BASE_DIR
    / "hasil_deteksi"
    / "data"
    / "hasil_deteksi.csv"
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Dashboard | AI-Fish",
    page_icon="🐟",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

try:

    from components.ui import load_css

    load_css()

except Exception:

    pass


# =========================================================
# HEADER
# =========================================================

st.title("🐟 AI-Fish Dashboard")

st.subheader(
    "Computer Vision Monitoring System"
)

st.write(
    "Monitoring hasil deteksi ikan "
    "menggunakan model YOLO11n."
)


# =========================================================
# CEK CSV
# =========================================================

if not CSV_PATH.exists():

    st.markdown("---")

    st.info(
        "📋 Belum ada data deteksi."
    )

    st.write(
        "Silakan masuk ke halaman "
        "**Deteksi Ikan**, upload gambar "
        "atau gunakan kamera, lalu lakukan "
        "proses deteksi."
    )

    st.stop()


# =========================================================
# BACA CSV
# =========================================================

try:

    df = pd.read_csv(
        CSV_PATH
    )

except Exception as e:

    st.error(
        f"❌ Gagal membaca data CSV: {e}"
    )

    st.stop()


# =========================================================
# CEK DATA
# =========================================================

if df.empty:

    st.markdown("---")

    st.info(
        "📋 Belum terdapat data hasil deteksi."
    )

    st.stop()


# =========================================================
# KONVERSI CONFIDENCE
# =========================================================

df["Confidence_Numeric"] = (

    df["Confidence"]
    .astype(str)
    .str.replace(
        "%",
        "",
        regex=False
    )
    .astype(float)

)


# =========================================================
# DATA STATISTIK
# =========================================================

total_images = (
    df["File"]
    .nunique()
)

total_fish = (
    len(df)
)

average_confidence = (
    df["Confidence_Numeric"]
    .mean()
)

highest_confidence = (
    df["Confidence_Numeric"]
    .max()
)

lowest_confidence = (
    df["Confidence_Numeric"]
    .min()
)

most_common_class = (
    df["Kelas Ikan"]
    .value_counts()
    .idxmax()
)

most_common_count = (
    df["Kelas Ikan"]
    .value_counts()
    .max()
)


# =========================================================
# RINGKASAN UTAMA
# =========================================================

st.markdown("---")

st.subheader(
    "📊 Ringkasan Sistem"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📸 Total Gambar",
        total_images
    )


with col2:

    st.metric(
        "🐟 Total Ikan",
        total_fish
    )


with col3:

    st.metric(
        "🏆 Kelas Terbanyak",
        most_common_class,
        delta=f"{most_common_count} deteksi"
    )


with col4:

    st.metric(
        "🎯 Confidence Tertinggi",
        f"{highest_confidence:.2f}%"
    )


# =========================================================
# STATISTIK CONFIDENCE
# =========================================================

st.markdown("---")

st.subheader(
    "🎯 Statistik Confidence"
)


conf_col1, conf_col2, conf_col3 = (
    st.columns(3)
)


with conf_col1:

    st.metric(
        "Confidence Rata-rata",
        f"{average_confidence:.2f}%"
    )


with conf_col2:

    st.metric(
        "Confidence Tertinggi",
        f"{highest_confidence:.2f}%"
    )


with conf_col3:

    st.metric(
        "Confidence Terendah",
        f"{lowest_confidence:.2f}%"
    )


# =========================================================
# DISTRIBUSI KELAS
# =========================================================

st.markdown("---")

st.subheader(
    "📈 Distribusi Kelas Ikan"
)

st.caption(
    "Jumlah objek ikan yang terdeteksi "
    "pada setiap kelas."
)


class_counts = (

    df["Kelas Ikan"]
    .value_counts()
    .reset_index()

)

class_counts.columns = [
    "Kelas Ikan",
    "Jumlah"
]

class_chart = (

    alt.Chart(
        class_counts
    )

    .mark_bar(
        cornerRadiusEnd=6,
        height=24
    )

    .encode(

        y=alt.Y(
            "Kelas Ikan:N",
            sort="-x",
            title=None,
            axis=alt.Axis(
                labelFontSize=12,
                labelColor="#A9BFD1"
            )
        ),

        x=alt.X(
            "Jumlah:Q",
            title=None,
            axis=alt.Axis(
                labelFontSize=11,
                labelColor="#718DA5",
                gridColor="#1B3042"
            )
        ),

        tooltip=[

            alt.Tooltip(
                "Kelas Ikan:N",
                title="Kelas"
            ),

            alt.Tooltip(
                "Jumlah:Q",
                title="Jumlah"
            )

        ]

    )

    .properties(
        height=330
    )

)


class_labels = (

    alt.Chart(
        class_counts
    )

    .mark_text(

        align="left",
        baseline="middle",
        dx=7,
        color="#EAF4FF",
        fontSize=12,
        fontWeight="bold"

    )

    .encode(

        y=alt.Y(
            "Kelas Ikan:N",
            sort="-x"
        ),

        x=alt.X(
            "Jumlah:Q"
        ),

        text=alt.Text(
            "Jumlah:Q"
        )

    )

)


st.altair_chart(
    class_chart + class_labels,
    use_container_width=True
)


# =========================================================
# CONFIDENCE PER KELAS
# =========================================================

st.markdown("---")

st.subheader(
    "🎯 Rata-rata Confidence per Kelas"
)

st.caption(
    "Rata-rata tingkat keyakinan model "
    "YOLO11n untuk setiap kelas ikan."
)


confidence_analysis = (

    df.groupby(
        "Kelas Ikan"
    )["Confidence_Numeric"]
    .mean()
    .reset_index()

)

confidence_analysis.columns = [
    "Kelas Ikan",
    "Confidence"
]

confidence_analysis = (
    confidence_analysis
    .sort_values(
        "Confidence",
        ascending=False
    )
)


confidence_chart = (

    alt.Chart(
        confidence_analysis
    )

    .mark_bar(
        cornerRadiusEnd=6,
        height=24
    )

    .encode(

        y=alt.Y(
            "Kelas Ikan:N",
            sort="-x",
            title=None,
            axis=alt.Axis(
                labelFontSize=12,
                labelColor="#A9BFD1"
            )
        ),

        x=alt.X(
            "Confidence:Q",
            title=None,
            scale=alt.Scale(
                domain=[0, 100]
            ),
            axis=alt.Axis(
                labelFontSize=11,
                labelColor="#718DA5",
                gridColor="#1B3042",
                format=".0f"
            )
        ),

        tooltip=[

            alt.Tooltip(
                "Kelas Ikan:N",
                title="Kelas"
            ),

            alt.Tooltip(
                "Confidence:Q",
                title="Confidence",
                format=".2f"
            )

        ]

    )

    .properties(
        height=330
    )

)


confidence_labels = (

    alt.Chart(
        confidence_analysis
    )

    .mark_text(

        align="left",
        baseline="middle",
        dx=7,
        color="#EAF4FF",
        fontSize=12,
        fontWeight="bold"

    )

    .encode(

        y=alt.Y(
            "Kelas Ikan:N",
            sort="-x"
        ),

        x=alt.X(
            "Confidence:Q"
        ),

        text=alt.Text(
            "Confidence:Q",
            format=".1f"
        )

    )

)


st.altair_chart(
    confidence_chart + confidence_labels,
    use_container_width=True
)


# =========================================================
# AKTIVITAS TERBARU
# =========================================================

st.markdown("---")

st.subheader(
    "🕐 Aktivitas Deteksi Terbaru"
)


recent_df = (

    df[
        [
            "Waktu",
            "File",
            "Kelas Ikan",
            "Confidence"
        ]
    ]

    .tail(8)
    .copy()

)


recent_df = (
    recent_df
    .iloc[::-1]
)


st.dataframe(
    recent_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# STATUS SISTEM
# =========================================================

st.markdown("---")

st.subheader(
    "⚙️ Status Sistem"
)


status1, status2, status3 = (
    st.columns(3)
)


with status1:

    st.success(
        "🟢 YOLO11n Ready"
    )


with status2:

    st.success(
        "🟢 Detection Active"
    )


with status3:

    st.success(
        "🟢 CSV Storage Active"
    )


# =========================================================
# INFORMASI MODEL
# =========================================================

st.markdown("---")

st.subheader(
    "🤖 Model AI"
)


model_col1, model_col2, model_col3 = (
    st.columns(3)
)


with model_col1:

    st.metric(
        "Model",
        "YOLO11n"
    )


with model_col2:

    st.metric(
        "Task",
        "Object Detection"
    )


with model_col3:

    st.metric(
        "Classes",
        "9"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "AI-Fish • YOLO11n Computer Vision Dashboard"
)