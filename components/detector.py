from pathlib import Path
from datetime import datetime
import csv

from ultralytics import YOLO


# =========================================================
# PATH PROJECT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "best.pt"

OUTPUT_DIR = (
    BASE_DIR
    / "hasil_deteksi"
    / "visual"
)

CSV_PATH = (
    BASE_DIR
    / "hasil_deteksi"
    / "data"
    / "hasil_deteksi.csv"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CSV_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# MODEL
# =========================================================

_model = None


def get_model():

    global _model

    if _model is None:

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"File model tidak ditemukan:\n"
                f"{MODEL_PATH}"
            )

        _model = YOLO(
            str(MODEL_PATH)
        )

    return _model


# =========================================================
# DETECTION
# =========================================================

def detect(
    image,
    confidence=0.25
):

    model = get_model()

    results = model.predict(
        source=image,
        imgsz=512,
        conf=confidence,
        verbose=False
    )

    return results[0]


# =========================================================
# EXTRACT DETECTIONS
# =========================================================

def extract_detections(result):

    detections = []

    # Jika tidak ada bounding box
    if result.boxes is None:

        return detections

    # Jika bounding box kosong
    if len(result.boxes) == 0:

        return detections

    for box in result.boxes:

        # -------------------------------------------------
        # CLASS
        # -------------------------------------------------

        class_id = int(
            box.cls[0].item()
        )

        # -------------------------------------------------
        # CONFIDENCE
        # -------------------------------------------------

        confidence = float(
            box.conf[0].item()
        )

        # -------------------------------------------------
        # BOUNDING BOX
        # -------------------------------------------------

        coordinates = (
            box.xyxy[0]
            .cpu()
            .tolist()
        )

        x1 = float(
            coordinates[0]
        )

        y1 = float(
            coordinates[1]
        )

        x2 = float(
            coordinates[2]
        )

        y2 = float(
            coordinates[3]
        )

        # -------------------------------------------------
        # SIMPAN DATA
        # -------------------------------------------------

        detection = {

            "Kelas Ikan":
                result.names[class_id],

            "Confidence":
                f"{confidence * 100:.2f}%",

            "X1":
                round(x1, 2),

            "Y1":
                round(y1, 2),

            "X2":
                round(x2, 2),

            "Y2":
                round(y2, 2)

        }

        detections.append(
            detection
        )

    return detections


# =========================================================
# SAVE RESULT IMAGE
# =========================================================

def save_result(
    result,
    filename
):

    output_path = (
        OUTPUT_DIR
        / filename
    )

    result.save(
        filename=str(
            output_path
        )
    )

    return output_path


# =========================================================
# SAVE DETECTION DATA
# =========================================================

def save_detection_data(
    filename,
    detections
):

    # -----------------------------------------------------
    # CEK FILE CSV
    # -----------------------------------------------------

    file_exists = (
        CSV_PATH.exists()
        and CSV_PATH.stat().st_size > 0
    )

    # -----------------------------------------------------
    # BUKA CSV
    # -----------------------------------------------------

    with open(
        CSV_PATH,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        if not file_exists:

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

        # -------------------------------------------------
        # WAKTU
        # -------------------------------------------------

        waktu = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # -------------------------------------------------
        # DATA DETEKSI
        # -------------------------------------------------

        for detection in detections:

            writer.writerow([

                waktu,

                filename,

                detection.get(
                    "Kelas Ikan",
                    "-"
                ),

                detection.get(
                    "Confidence",
                    "0%"
                ),

                detection.get(
                    "X1",
                    0
                ),

                detection.get(
                    "Y1",
                    0
                ),

                detection.get(
                    "X2",
                    0
                ),

                detection.get(
                    "Y2",
                    0
                )

            ])

    return CSV_PATH