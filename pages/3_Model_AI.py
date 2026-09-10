import streamlit as st
from components.ui import load_css


st.set_page_config(
    page_title="Model AI | AI-Fish",
    page_icon="🤖",
    layout="wide"
)

load_css()


# =========================================================
# HEADER
# =========================================================

st.title("🤖 Model AI")

st.subheader("YOLO11n Object Detection")

st.write(
    "Informasi model Artificial Intelligence "
    "yang digunakan pada sistem AI-Fish."
)

st.info("Model: YOLO11n")


# =========================================================
# MODEL OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-kicker">MODEL OVERVIEW</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Model",
        value="YOLO11n"
    )

with col2:
    st.metric(
        label="Jumlah Kelas",
        value="9"
    )

with col3:
    st.metric(
        label="Image Size",
        value="512 × 512"
    )


# =========================================================
# MODEL DESCRIPTION
# =========================================================

st.markdown(
    '<div class="section-space"></div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.3, 1])


with left:

    st.markdown(
        '<div class="section-kicker">TENTANG MODEL</div>',
        unsafe_allow_html=True
    )

    st.subheader("YOLO11n")

    st.write(
        """
        YOLO11n merupakan model object detection yang digunakan
        untuk mendeteksi dan mengklasifikasikan ikan berdasarkan
        gambar yang diberikan kepada sistem.

        Model menerima gambar sebagai input kemudian menghasilkan
        bounding box, nama kelas ikan, dan nilai confidence.
        """
    )

    st.info(
        "Model digunakan untuk melakukan object detection "
        "terhadap 9 kelas ikan."
    )


with right:

    st.markdown(
        '<div class="section-kicker">KONFIGURASI TRAINING</div>',
        unsafe_allow_html=True
    )

    st.write("**Epoch:** 50")
    st.write("**Image Size:** 512 × 512")
    st.write("**Batch Size:** 16")
    st.write("**Model:** YOLO11n")
    st.write("**Pretrained:** Ya")
    st.write("**Task:** Object Detection")


# =========================================================
# DETECTION CLASSES
# =========================================================

st.markdown(
    '<div class="section-space"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-kicker">DETECTION CLASSES</div>',
    unsafe_allow_html=True
)

classes = [
    "Black Sea Sprat",
    "Gilt-Head Bream",
    "Hourse Mackerel",
    "Red Mullet",
    "Red Sea Bream",
    "Sea Bass",
    "Shrimp",
    "Striped Red Mullet",
    "Trout"
]

cols = st.columns(3)

for index, class_name in enumerate(classes):

    with cols[index % 3]:

        st.info(
            f"**{index + 1}.** {class_name}"
        )


# =========================================================
# PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-space"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-kicker">MODEL PERFORMANCE</div>',
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.metric(
        "Precision",
        "99.73%"
    )

with p2:
    st.metric(
        "Recall",
        "99.74%"
    )

with p3:
    st.metric(
        "mAP50",
        "99.50%"
    )

with p4:
    st.metric(
        "mAP50-95",
        "97.98%"
    )


# =========================================================
# NOTE
# =========================================================

st.markdown(
    '<div class="section-space"></div>',
    unsafe_allow_html=True
)

st.warning(
    "Nilai performa di atas merupakan hasil evaluasi pada "
    "test set internal. Performa pada gambar dari luar dataset "
    "dapat berbeda."
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">AI-Fish • YOLO11n Computer Vision</div>',
    unsafe_allow_html=True
)