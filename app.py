import streamlit as st
from components.ui import load_css


# ==========================================
# KONFIGURASI APLIKASI
# ==========================================

st.set_page_config(
    page_title="AI-Fish",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# LOAD CSS
# ==========================================

load_css()


# ==========================================
# HALAMAN
# ==========================================

dashboard = st.Page(
    "pages/1_Dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True
)

detection = st.Page(
    "pages/2_Deteksi_Ikan.py",
    title="Deteksi Ikan",
    icon="🔍"
)

model_ai = st.Page(
    "pages/3_Model_AI.py",
    title="Model AI",
    icon="🤖"
)

history = st.Page(
    "pages/4_Riwayat_Hasil.py",
    title="Riwayat Hasil",
    icon="🖼️"
)


# ==========================================
# NAVIGATION
# ==========================================

pg = st.navigation(
    [
        dashboard,
        detection,
        history,
        model_ai
    ],
    position="hidden"
)


# ==========================================
# SIDEBAR CUSTOM
# ==========================================

with st.sidebar:

    st.markdown(
        "## 🐟 AI-FISH"
    )

    st.caption(
        "COMPUTER VISION SYSTEM"
    )

    st.divider()

    st.markdown(
        "**MENU**"
    )

    st.page_link(
        dashboard,
        label="Dashboard",
        icon="🏠"
    )

    st.page_link(
        detection,
        label="Deteksi Ikan",
        icon="🔍"
    )

    st.page_link(
        history,
        label="Riwayat Hasil",
        icon="🖼️"
    )

    st.page_link(
        model_ai,
        label="Model AI",
        icon="🤖"
    )

    st.divider()

    st.markdown(
        "**MODEL STATUS**"
    )

    st.success(
        "● YOLO11n Ready"
    )

    st.caption(
        "Object Detection"
    )

    st.divider()

    st.caption(
        "AI-Fish Dashboard"
    )

    st.caption(
        "YOLO11n • 9 Classes"
    )


# ==========================================
# JALANKAN HALAMAN
# ==========================================

pg.run()