"""
Fungsi-fungsi untuk mempersiapkan gambar sebelum masuk ke model.
Dipakai baik saat training maupun saat prediksi di web app,
supaya perlakuan gambarnya konsisten.
"""

import numpy as np
from PIL import Image

IMG_SIZE = (224, 224)  # ukuran input standar MobileNetV2 & EfficientNetB0


def load_and_preprocess_image(image_path_or_file):
    """
    Load gambar dari path file atau file object (hasil upload Flask),
    lalu resize dan ubah jadi array numpy siap pakai model.

    Parameter:
        image_path_or_file: path string ATAU file-like object dari request.files

    Return:
        numpy array dengan shape (1, 224, 224, 3), nilai pixel 0-255 (float32)
    """
    img = Image.open(image_path_or_file).convert("RGB")  # pastikan 3 channel (RGB)
    img = img.resize(IMG_SIZE)

    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)  # jadi (1, 224, 224, 3) untuk batch

    return img_array


def preprocess_for_mobilenetv2(img_array):
    """MobileNetV2 butuh normalisasi khusus: nilai pixel di-scale ke rentang -1 sampai 1."""
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    return preprocess_input(img_array.copy())


def preprocess_for_efficientnetb0(img_array):
    """EfficientNetB0 punya normalisasi built-in di dalam arsitekturnya sendiri,
    jadi cukup pastikan nilai pixel masih di rentang 0-255 (tidak perlu di-scale manual)."""
    from tensorflow.keras.applications.efficientnet import preprocess_input
    return preprocess_input(img_array.copy())