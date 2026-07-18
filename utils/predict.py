"""
Modul untuk load kedua model dan melakukan prediksi.
PENTING: preprocessing (normalisasi) TIDAK perlu dilakukan manual di sini,
karena sudah dibakukan sebagai bagian dari arsitektur model saat training
(lihat train_model.py -> build_model -> x = preprocess_fn(x)).
Model menerima input mentah dengan nilai pixel 0-255.
"""

import time
import numpy as np
from tensorflow.keras.models import load_model

from utils.labels import CLASS_NAMES
from utils.preprocessing import load_and_preprocess_image

print("Loading model MobileNetV2...")
mobilenet_model = load_model("models/mobilenetv2_instruments.h5")

print("Loading model EfficientNetB0...")
efficientnet_model = load_model("models/efficientnetb0_instruments.h5")

print("Kedua model berhasil dimuat.")


def predict_single_model(image_file, model_choice="mobilenetv2"):
    img_array = load_and_preprocess_image(image_file)  # hasil: 0-255, shape (1,224,224,3)

    start_time = time.time()

    if model_choice == "mobilenetv2":
        predictions = mobilenet_model.predict(img_array, verbose=0)[0]
    else:
        predictions = efficientnet_model.predict(img_array, verbose=0)[0]

    inference_time_ms = round((time.time() - start_time) * 1000, 2)

    return _format_prediction_result(predictions, model_choice, inference_time_ms)


def predict_both_models(image_file):
    img_array = load_and_preprocess_image(image_file)

    start_time = time.time()
    pred_mnv2 = mobilenet_model.predict(img_array, verbose=0)[0]
    time_mnv2 = round((time.time() - start_time) * 1000, 2)

    start_time = time.time()
    pred_effnet = efficientnet_model.predict(img_array, verbose=0)[0]
    time_effnet = round((time.time() - start_time) * 1000, 2)

    return {
        "mobilenetv2": _format_prediction_result(pred_mnv2, "mobilenetv2", time_mnv2),
        "efficientnetb0": _format_prediction_result(pred_effnet, "efficientnetb0", time_effnet),
    }


def _format_prediction_result(predictions, model_name, inference_time_ms):
    top3_idx = np.argsort(predictions)[-3:][::-1]
    top3_results = [
        {"label": CLASS_NAMES[idx], "confidence": round(float(predictions[idx]) * 100, 2)}
        for idx in top3_idx
    ]
    return {
        "model": model_name,
        "predicted_label": top3_results[0]["label"],
        "confidence": top3_results[0]["confidence"],
        "top3": top3_results,
        "inference_time_ms": inference_time_ms,
    }