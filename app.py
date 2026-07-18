"""
Aplikasi Flask utama.
"""

import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from utils.predict import predict_single_model, predict_both_models
from utils.labels import CLASS_NAMES
from utils.instrument_info import get_instrument_info, INSTRUMENT_INFO

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dataset")
def dataset_page():
    # Gabungkan nama kelas dengan info kategorinya untuk ditampilkan di galeri
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

    if not file or file.filename == "":
        return render_template("index.html", error="Silakan pilih gambar terlebih dahulu.")

    if not allowed_file(file.filename):
        return render_template("index.html", error="Format file harus PNG, JPG, atau JPEG.")

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    with open(filepath, "rb") as reopened_file:
        if mode == "compare":
            result = predict_both_models(reopened_file)
            info_a = get_instrument_info(result["mobilenetv2"]["predicted_label"])
            info_b = get_instrument_info(result["efficientnetb0"]["predicted_label"])
            result["mobilenetv2"]["info"] = info_a
            result["efficientnetb0"]["info"] = info_b
        else:
            result = predict_single_model(reopened_file, model_choice)
            result["info"] = get_instrument_info(result["predicted_label"])

    return render_template(
        "result.html",
        mode=mode,
        result=result,
        image_url="/" + filepath,
    )


if __name__ == "__main__":
    import os
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
