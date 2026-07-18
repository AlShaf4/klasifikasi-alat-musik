"""
Script sekali-jalan untuk menyimpan ulang model .h5 yang sudah ada
ke format SavedModel, yang jauh lebih stabil untuk deployment
lintas environment (lokal vs Railway/cloud).
Jalankan ini SEKALI di lokal setelah training selesai.
"""

from tensorflow.keras.models import load_model

print("Loading model MobileNetV2 (.h5)...")
mnv2 = load_model("models/mobilenetv2_instruments.h5")
print("Menyimpan ulang sebagai SavedModel...")
mnv2.export("models/mobilenetv2_instruments")  # menghasilkan FOLDER, bukan file

print("Loading model EfficientNetB0 (.h5)...")
effnet = load_model("models/efficientnetb0_instruments.h5")
print("Menyimpan ulang sebagai SavedModel...")
effnet.export("models/efficientnetb0_instruments")

print("Selesai. Cek folder models/, sekarang ada folder baru selain file .h5.")
