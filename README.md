# 🐟 AI-Fish Dashboard

## Computer Vision Fish Detection System

AI-Fish Dashboard adalah aplikasi Computer Vision berbasis Python dan Streamlit yang digunakan untuk mendeteksi objek ikan dari gambar menggunakan model YOLO11n.

Aplikasi ini menyediakan proses mulai dari memasukkan gambar, melakukan deteksi menggunakan model AI, menampilkan hasil bounding box, menyimpan hasil deteksi, hingga melihat riwayat dan statistik deteksi.

---

## 🎯 Tujuan Project

Project ini dikembangkan sebagai implementasi Computer Vision untuk melakukan object detection pada beberapa jenis ikan.

Sistem dirancang agar pengguna dapat:

- Mengunggah satu atau beberapa gambar ikan.
- Melakukan proses deteksi menggunakan YOLO11n.
- Melihat bounding box hasil deteksi.
- Melihat kelas ikan dan confidence.
- Menyimpan hasil deteksi.
- Melihat riwayat hasil deteksi.
- Menghapus hasil deteksi yang tidak sesuai.
- Melihat statistik hasil deteksi melalui Dashboard.

---

## 🤖 Model AI

Model yang digunakan:

**YOLO11n**

Task:

**Object Detection**

Model dilatih menggunakan dataset ikan dengan 9 kelas.

### Kelas Ikan

1. Black Sea Sprat
2. Gilt-Head Bream
3. Hourse Mackerel
4. Red Mullet
5. Red Sea Bream
6. Sea Bass
7. Shrimp
8. Striped Red Mullet
9. Trout

---

## 📊 Dataset

Dataset yang digunakan adalah:

**A Large Scale Fish Dataset**

Dataset terdiri dari 9 kelas ikan dengan jumlah:

- 9.000 gambar RGB
- 9.000 ground-truth mask
- 1.000 gambar per kelas

Dataset kemudian dipersiapkan untuk kebutuhan object detection YOLO.

Ground-truth mask dikonversi menjadi bounding box YOLO.

---

## 📁 Pembagian Dataset

Dataset dibagi menjadi:

| Dataset | Jumlah | Persentase |
|---|---:|---:|
| Training | 6.300 | 70% |
| Validation | 1.350 | 15% |
| Testing | 1.350 | 15% |
| Total | 9.000 | 100% |

Pembagian dilakukan dengan mempertimbangkan duplicate group agar data yang identik tidak tersebar antar subset.

---

## ⚙️ Training Model

Konfigurasi training YOLO11n:

| Parameter | Nilai |
|---|---|
| Model | YOLO11n |
| Epoch | 50 |
| Image Size | 512 × 512 |
| Batch Size | 16 |
| Pretrained | Ya |
| Task | Object Detection |

---

## 📈 Hasil Evaluasi Model

Evaluasi dilakukan menggunakan test set internal yang terdiri dari 1.350 gambar.

Hasil evaluasi:

| Metric | Hasil |
|---|---:|
| Precision | 99.73% |
| Recall | 99.74% |
| mAP@50 | 99.50% |
| mAP@50-95 | 97.98% |

> Catatan: hasil tersebut merupakan evaluasi pada test set internal dan tidak secara otomatis menunjukkan performa model pada seluruh kondisi gambar di dunia nyata.

---

## 🖥️ Fitur Dashboard

### 🏠 Dashboard

Menampilkan:

- Total gambar
- Total ikan terdeteksi
- Kelas ikan terbanyak
- Rata-rata confidence
- Distribusi kelas ikan
- Rata-rata confidence per kelas
- Aktivitas deteksi terbaru
- Status sistem

### 🔎 Deteksi Ikan

Pengguna dapat:

1. Upload gambar.
2. Memproses gambar menggunakan YOLO11n.
3. Melihat hasil bounding box.
4. Melihat kelas ikan.
5. Melihat confidence.
6. Menyimpan hasil visual.
7. Menyimpan data hasil deteksi.

### 🖼️ Riwayat Hasil

Menampilkan:

- Data riwayat deteksi
- Filter berdasarkan kelas ikan
- Filter berdasarkan nama file
- Statistik riwayat
- Galeri hasil deteksi
- Fitur menghapus hasil deteksi yang tidak sesuai

### 🤖 Model AI

Menampilkan informasi mengenai:

- Model YOLO11n
- Object Detection
- Dataset
- Jumlah kelas
- Konfigurasi model
- Hasil evaluasi

---

## 📂 Struktur Project

```text
AI-Fish-Dashboard/
│
├── app.py
├── best.pt
├── requirements.txt
├── README.md
│
├── assets/
│   └── style.css
│
├── components/
│   ├── ui.py
│   └── detector.py
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Deteksi_Ikan.py
│   ├── 3_Model_AI.py
│   └── 4_Riwayat_Hasil.py
│
├── hasil_deteksi/
│   ├── visual/
│   └── data/
│       └── hasil_deteksi.csv
│
└── venv/