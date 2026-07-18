"""
Aplikasi Flask utama — Klasifikasi Alat Musik
Gambar diproses langsung di memory (tidak disimpan ke disk),
supaya kompatibel dengan platform hosting yang filesystem-nya sementara/read-only.
"""

import io
import base64
from flask import Flask, render_template, request

from utils.predict import predict_single_model, predict_both_models
from utils.labels import CLASS_NAMES
from utils.instrument_info import get_instrument_info, INSTRUMENT_INFO

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # batas upload 5MB

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dataset")
def dataset_page():
    classes_with_info = [
        {"name": c, "kategori": INSTRUMENT_INFO.get(c, {}).get("kategori", "-")}
        for c in CLASS_NAMES
    ]
    return render_template("dataset.html", classes=classes_with_info, total_classes=len(CLASS_NAMES))


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/profil")
def profile_page():
    return render_template("profil.html")


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("image")
    mode = request.form.get("mode", "single")
    model_choice = request.form.get("model", "mobilenetv2")

    # ---- Validasi ----
    if not file or file.filename == "":
        return render_template("index.html", error="Silakan pilih gambar terlebih dahulu.")

    if not allowed_file(file.filename):
        return render_template("index.html", error="Format file harus PNG, JPG, atau JPEG.")

    try:
        # ---- Baca file langsung ke memory, TIDAK disimpan ke disk ----
        file_bytes = file.read()
        image_stream = io.BytesIO(file_bytes)

        # ---- Prediksi ----
        if mode == "compare":
            result = predict_both_models(image_stream)
            result["mobilenetv2"]["info"] = get_instrument_info(result["mobilenetv2"]["predicted_label"])
            result["efficientnetb0"]["info"] = get_instrument_info(result["efficientnetb0"]["predicted_label"])
        else:
            result = predict_single_model(image_stream, model_choice)
            result["info"] = get_instrument_info(result["predicted_label"])

        # ---- Encode gambar ke base64 supaya bisa ditampilkan ulang tanpa disimpan sebagai file ----
        mimetype = file.mimetype or "image/jpeg"
        image_base64 = base64.b64encode(file_bytes).decode("utf-8")
        image_data_url = f"data:{mimetype};base64,{image_base64}"

        return render_template(
            "result.html",
            mode=mode,
            result=result,
            image_url=image_data_url,
        )

    except Exception as e:
        return render_template("index.html", error=f"Terjadi kesalahan saat memproses gambar: {str(e)}")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
