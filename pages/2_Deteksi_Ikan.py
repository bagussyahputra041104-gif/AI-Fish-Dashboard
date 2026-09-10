import streamlit as st
from components.ui import load_css
from components.detector import (
    detect,
    extract_detections,
    save_result,
    save_detection_data
)
from PIL import Image


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Deteksi Ikan | AI-Fish",
    page_icon="🔎",
    layout="wide"
)

load_css()


# =========================================================
# HEADER
# =========================================================

st.title("🔎 Deteksi Ikan")

st.write(
    "Masukkan gambar melalui upload atau kamera "
    "untuk melakukan deteksi ikan menggunakan YOLO11n."
)

st.markdown("---")


# =========================================================
# MODE DETEKSI
# =========================================================

st.subheader("🎯 Mode Deteksi")

detection_mode = st.radio(
    "Pilih mode deteksi",
    [
        "⚡ Cepat",
        "⚖️ Seimbang",
        "🎯 Ketat",
        "⚙️ Custom"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


# =========================================================
# CONFIDENCE BERDASARKAN MODE
# =========================================================

if detection_mode == "⚡ Cepat":

    confidence_percent = 25

    st.info(
        "⚡ Mode Cepat — model lebih sensitif "
        "terhadap kemungkinan objek ikan."
    )


elif detection_mode == "⚖️ Seimbang":

    confidence_percent = 50

    st.info(
        "⚖️ Mode Seimbang — keseimbangan antara "
        "sensitivitas dan keyakinan model."
    )


elif detection_mode == "🎯 Ketat":

    confidence_percent = 70

    st.info(
        "🎯 Mode Ketat — hanya prediksi dengan "
        "confidence tinggi yang ditampilkan."
    )


else:

    confidence_percent = st.slider(
        "Confidence Minimum",
        min_value=25,
        max_value=95,
        value=50,
        step=5,
        help=(
            "Tentukan sendiri confidence minimum "
            "yang digunakan YOLO11n."
        )
    )

    st.info(
        f"⚙️ Mode Custom — confidence minimum "
        f"{confidence_percent}%."
    )


confidence = confidence_percent / 100

st.caption(
    f"🎯 Confidence Minimum Aktif: "
    f"**{confidence_percent}%**"
)


# =========================================================
# PILIH METODE INPUT
# =========================================================

st.markdown("---")

st.subheader("📥 Pilih Metode Input")

input_method = st.radio(
    "Metode input",
    [
        "📁 Upload Gambar",
        "📷 Kamera"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


# =========================================================
# UPLOAD GAMBAR
# =========================================================

if input_method == "📁 Upload Gambar":

    st.markdown("---")

    st.subheader("📁 Upload Gambar")

    uploaded_files = st.file_uploader(
        "Pilih satu atau beberapa gambar ikan",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        accept_multiple_files=True
    )

    # -----------------------------------------------------
    # PREVIEW
    # -----------------------------------------------------

    if uploaded_files:

        st.markdown("---")

        st.subheader(
            f"🖼️ File Dipilih ({len(uploaded_files)})"
        )

        preview_cols = st.columns(
            min(len(uploaded_files), 4)
        )

        for index, uploaded_file in enumerate(
            uploaded_files
        ):

            image = Image.open(
                uploaded_file
            ).convert("RGB")

            with preview_cols[index % 4]:

                st.image(
                    image,
                    caption=uploaded_file.name,
                    use_container_width=True
                )

        # -------------------------------------------------
        # PROCESS BUTTON
        # -------------------------------------------------

        st.markdown("---")

        process_upload = st.button(
            "🔍 Proses Gambar Upload",
            type="primary",
            use_container_width=True
        )

        # -------------------------------------------------
        # PROCESS UPLOAD
        # -------------------------------------------------

        if process_upload:

            st.subheader("🎯 Hasil Deteksi")

            total_images = len(
                uploaded_files
            )

            total_objects = 0

            all_detections = []

            progress = st.progress(0)

            status_text = st.empty()

            for index, uploaded_file in enumerate(
                uploaded_files
            ):

                try:

                    status_text.write(
                        f"🔄 Memproses "
                        f"{uploaded_file.name}..."
                    )

                    image = Image.open(
                        uploaded_file
                    ).convert("RGB")

                    result = detect(
                        image,
                        confidence=confidence
                    )

                    detections = extract_detections(
                        result
                    )

                    st.markdown("---")

                    st.markdown(
                        f"### 📷 {uploaded_file.name}"
                    )

                    # -------------------------------------
                    # ADA DETEKSI
                    # -------------------------------------

                    if detections:

                        result_image = (
                            result.plot()
                        )

                        output_filename = (
                            f"hasil_{uploaded_file.name}"
                        )

                        saved_image = save_result(
                            result,
                            output_filename
                        )

                        saved_csv = (
                            save_detection_data(
                                uploaded_file.name,
                                detections
                            )
                        )

                        result_col1, result_col2 = (
                            st.columns([1.5, 1])
                        )

                        # ---------------------------------
                        # HASIL GAMBAR
                        # ---------------------------------

                        with result_col1:

                            st.image(
                                result_image,
                                caption=(
                                    "Hasil Deteksi YOLO11n"
                                ),
                                use_container_width=True
                            )

                        # ---------------------------------
                        # DETAIL
                        # ---------------------------------

                        with result_col2:

                            st.markdown(
                                "#### 🎯 Detail Deteksi"
                            )

                            st.metric(
                                "Jumlah Objek",
                                len(detections)
                            )

                            st.caption(
                                f"Mode: "
                                f"{detection_mode}"
                            )

                            st.caption(
                                f"Threshold: "
                                f"{confidence_percent}%"
                            )

                            for detection in detections:

                                st.info(
                                    f"🐟 "
                                    f"**{detection['Kelas Ikan']}**\n\n"
                                    f"Confidence: "
                                    f"**{detection['Confidence']}**"
                                )

                        # ---------------------------------
                        # BOUNDING BOX
                        # ---------------------------------

                        st.markdown("---")

                        st.markdown(
                            "#### 📐 Detail Bounding Box"
                        )

                        bbox_data = []

                        for detection in detections:

                            bbox_data.append({

                                "Kelas Ikan":
                                    detection[
                                        "Kelas Ikan"
                                    ],

                                "Confidence":
                                    detection[
                                        "Confidence"
                                    ],

                                "X1":
                                    detection["X1"],

                                "Y1":
                                    detection["Y1"],

                                "X2":
                                    detection["X2"],

                                "Y2":
                                    detection["Y2"]

                            })

                        st.dataframe(
                            bbox_data,
                            use_container_width=True,
                            hide_index=True
                        )

                        # ---------------------------------
                        # STATUS PENYIMPANAN
                        # ---------------------------------

                        st.success(
                            f"💾 Gambar tersimpan: "
                            f"{saved_image.name}"
                        )

                        st.success(
                            f"📊 Data tersimpan: "
                            f"{saved_csv.name}"
                        )

                        # ---------------------------------
                        # REKAP
                        # ---------------------------------

                        total_objects += len(
                            detections
                        )

                        for detection in detections:

                            all_detections.append({

                                "File":
                                    uploaded_file.name,

                                "Kelas Ikan":
                                    detection[
                                        "Kelas Ikan"
                                    ],

                                "Confidence":
                                    detection[
                                        "Confidence"
                                    ],

                                "X1":
                                    detection["X1"],

                                "Y1":
                                    detection["Y1"],

                                "X2":
                                    detection["X2"],

                                "Y2":
                                    detection["Y2"]

                            })

                    # -------------------------------------
                    # TIDAK ADA DETEKSI
                    # -------------------------------------

                    else:

                        st.warning(
                            "⚠️ Tidak ada ikan yang "
                            "terdeteksi pada gambar "
                            f"dengan threshold "
                            f"{confidence_percent}%."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Gagal memproses "
                        f"{uploaded_file.name}: {e}"
                    )

                progress.progress(
                    (index + 1) / total_images
                )

            status_text.success(
                "✅ Semua gambar upload selesai diproses."
            )

            # -------------------------------------------------
            # SUMMARY
            # -------------------------------------------------

            st.markdown("---")

            st.subheader(
                "📊 Ringkasan Proses"
            )

            summary1, summary2, summary3 = (
                st.columns(3)
            )

            with summary1:

                st.metric(
                    "Total Gambar",
                    total_images
                )

            with summary2:

                st.metric(
                    "Total Ikan",
                    total_objects
                )

            with summary3:

                if all_detections:

                    avg_confidence = sum(
                        float(
                            detection[
                                "Confidence"
                            ].replace(
                                "%",
                                ""
                            )
                        )
                        for detection in
                        all_detections
                    ) / len(
                        all_detections
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

            # -------------------------------------------------
            # REKAPITULASI
            # -------------------------------------------------

            if all_detections:

                st.markdown("---")

                st.subheader(
                    "📋 Rekapitulasi Deteksi"
                )

                st.dataframe(
                    all_detections,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.warning(
                    "Tidak ada objek ikan yang "
                    "berhasil dideteksi."
                )


# =========================================================
# KAMERA
# =========================================================

else:

    st.markdown("---")

    st.subheader("📷 Kamera")

    st.write(
        "Gunakan kamera untuk mengambil foto ikan "
        "dan menganalisisnya menggunakan YOLO11n."
    )

    # -----------------------------------------------------
    # CAMERA
    # -----------------------------------------------------

    camera_photo = st.camera_input(
        "📷 Buka Kamera"
    )

    # -----------------------------------------------------
    # CAMERA PHOTO
    # -----------------------------------------------------

    if camera_photo:

        st.markdown("---")

        st.subheader(
            "🖼️ Foto Kamera"
        )

        camera_image = Image.open(
            camera_photo
        ).convert("RGB")

        camera_col1, camera_col2 = (
            st.columns([1.5, 1])
        )

        # ---------------------------------------------
        # PREVIEW
        # ---------------------------------------------

        with camera_col1:

            st.image(
                camera_image,
                caption="Foto dari Kamera",
                use_container_width=True
            )

        # ---------------------------------------------
        # INFO
        # ---------------------------------------------

        with camera_col2:

            st.success(
                "✅ Foto berhasil diambil."
            )

            st.write(
                "Foto siap diproses "
                "menggunakan YOLO11n."
            )

            st.caption(
                f"Mode: **{detection_mode}**"
            )

            st.caption(
                f"Threshold: "
                f"**{confidence_percent}%**"
            )

            process_camera = st.button(
                "🔍 Deteksi Foto Kamera",
                type="primary",
                use_container_width=True
            )

        # -------------------------------------------------
        # PROCESS CAMERA
        # -------------------------------------------------

        if process_camera:

            with st.spinner(
                "🤖 YOLO11n sedang menganalisis gambar..."
            ):

                try:

                    result = detect(
                        camera_image,
                        confidence=confidence
                    )

                    detections = extract_detections(
                        result
                    )

                    st.markdown("---")

                    st.subheader(
                        "🎯 Hasil Deteksi Kamera"
                    )

                    # -------------------------------------
                    # ADA DETEKSI
                    # -------------------------------------

                    if detections:

                        result_image = (
                            result.plot()
                        )

                        camera_filename = (
                            "kamera_"
                            + camera_photo.name
                        )

                        output_filename = (
                            f"hasil_{camera_filename}"
                        )

                        saved_image = save_result(
                            result,
                            output_filename
                        )

                        saved_csv = (
                            save_detection_data(
                                camera_filename,
                                detections
                            )
                        )

                        result_col1, result_col2 = (
                            st.columns([1.5, 1])
                        )

                        # ---------------------------------
                        # GAMBAR
                        # ---------------------------------

                        with result_col1:

                            st.image(
                                result_image,
                                caption=(
                                    "Hasil Deteksi "
                                    "YOLO11n"
                                ),
                                use_container_width=True
                            )

                        # ---------------------------------
                        # DETAIL
                        # ---------------------------------

                        with result_col2:

                            st.markdown(
                                "#### 🎯 Detail Deteksi"
                            )

                            st.metric(
                                "Jumlah Objek",
                                len(detections)
                            )

                            st.caption(
                                f"Mode: "
                                f"{detection_mode}"
                            )

                            st.caption(
                                f"Threshold: "
                                f"{confidence_percent}%"
                            )

                            for detection in detections:

                                st.info(
                                    f"🐟 "
                                    f"**{detection['Kelas Ikan']}**\n\n"
                                    f"Confidence: "
                                    f"**{detection['Confidence']}**"
                                )

                        # ---------------------------------
                        # BOUNDING BOX
                        # ---------------------------------

                        st.markdown("---")

                        st.markdown(
                            "#### 📐 Detail Bounding Box"
                        )

                        bbox_data = []

                        for detection in detections:

                            bbox_data.append({

                                "Kelas Ikan":
                                    detection[
                                        "Kelas Ikan"
                                    ],

                                "Confidence":
                                    detection[
                                        "Confidence"
                                    ],

                                "X1":
                                    detection["X1"],

                                "Y1":
                                    detection["Y1"],

                                "X2":
                                    detection["X2"],

                                "Y2":
                                    detection["Y2"]

                            })

                        st.dataframe(
                            bbox_data,
                            use_container_width=True,
                            hide_index=True
                        )

                        # ---------------------------------
                        # STATUS
                        # ---------------------------------

                        st.success(
                            f"💾 Hasil tersimpan: "
                            f"{saved_image.name}"
                        )

                        st.success(
                            f"📊 Data tersimpan: "
                            f"{saved_csv.name}"
                        )

                    # -------------------------------------
                    # TIDAK ADA DETEKSI
                    # -------------------------------------

                    else:

                        st.warning(
                            "⚠️ Tidak ada ikan yang "
                            "terdeteksi pada foto kamera "
                            f"dengan threshold "
                            f"{confidence_percent}%."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Gagal melakukan deteksi: {e}"
                    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "AI-Fish • YOLO11n Computer Vision"
)