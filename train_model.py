"""
SCRIPT TRAINING — dijalankan sekali secara terpisah (di lokal atau Google Colab),
BUKAN bagian dari aplikasi Flask. Jalankan dengan: python train_model.py

Alur: load dataset -> bangun model transfer learning -> train -> evaluasi -> simpan .h5 + grafik
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2, EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# ============================================================
# 1. KONFIGURASI
# ============================================================
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
DATASET_DIR = "dataset"  # berisi folder train/, valid/, test/
RESULTS_DIR = "static/images/results"
MODELS_DIR = "models"

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# ============================================================
# 2. LOAD DATASET
# ============================================================
train_ds = tf.keras.utils.image_dataset_from_directory(
    os.path.join(DATASET_DIR, "train"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical",  # one-hot encoding, karena multi-class
)

valid_ds = tf.keras.utils.image_dataset_from_directory(
    os.path.join(DATASET_DIR, "valid"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical",
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    os.path.join(DATASET_DIR, "test"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical",
    shuffle=False,  # PENTING: jangan diacak, supaya urutan label saat evaluasi tetap sinkron
)

CLASS_NAMES = train_ds.class_names
NUM_CLASSES = len(CLASS_NAMES)
print(f"Jumlah kelas: {NUM_CLASSES}")
print(f"Urutan kelas: {CLASS_NAMES}")
print(">>> COPY urutan kelas di atas ke utils/labels.py supaya label prediksi nanti akurat!")

# ============================================================
# 3. AUGMENTASI DATA
# ============================================================
# Augmentasi cuma diterapkan ke data training, TIDAK ke valid/test
# (valid/test harus mencerminkan data asli untuk evaluasi yang fair)
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.15),
    tf.keras.layers.RandomZoom(0.15),
    tf.keras.layers.RandomContrast(0.1),
])

# Optimasi loading data (caching + prefetch, mempercepat training)
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
valid_ds = valid_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)


# ============================================================
# 4. FUNGSI BANGUN MODEL (Transfer Learning)
# ============================================================
def build_model(base_model_fn, preprocess_fn, model_name):
    """
    Fungsi generik untuk membangun model transfer learning.
    base_model_fn: MobileNetV2 atau EfficientNetB0 (belum dipanggil)
    preprocess_fn: fungsi preprocessing khusus arsitektur tsb
    """
    inputs = tf.keras.Input(shape=(224, 224, 3))

    x = data_augmentation(inputs)      # augmentasi di dalam graph model
    x = preprocess_fn(x)               # normalisasi sesuai arsitektur

    base_model = base_model_fn(
        include_top=False,          # buang classifier bawaan ImageNet (1000 kelas)
        weights="imagenet",         # pakai bobot hasil pretrain di ImageNet
        input_tensor=x,
    )
    base_model.trainable = False    # FREEZE dulu di tahap awal (feature extraction)

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dropout(0.3)(x)             # mencegah overfitting
    outputs = Dense(NUM_CLASSES, activation="softmax", name="classifier")(x)

    model = Model(inputs, outputs, name=model_name)
    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model, base_model


def fine_tune_model(model, base_model, unfreeze_layers=30):
    """
    Tahap ke-2: unfreeze beberapa layer terakhir base model,
    lalu training ulang dengan learning rate KECIL supaya bobot ImageNet tidak rusak.
    """
    base_model.trainable = True
    for layer in base_model.layers[:-unfreeze_layers]:
        layer.trainable = False  # tetap freeze layer awal, cuma unfreeze bagian akhir

    model.compile(
        optimizer=Adam(learning_rate=1e-5),  # LR jauh lebih kecil dari tahap awal
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


# ============================================================
# 5. FUNGSI TRAINING LENGKAP (dipakai untuk kedua arsitektur)
# ============================================================
def train_and_evaluate(base_model_fn, preprocess_fn, model_name):
    print(f"\n{'='*50}\nTRAINING: {model_name}\n{'='*50}")

    model, base_model = build_model(base_model_fn, preprocess_fn, model_name)

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        ModelCheckpoint(
            f"{MODELS_DIR}/{model_name}_instruments.h5",
            monitor="val_accuracy",
            save_best_only=True,
        ),
    ]

    # --- Tahap 1: Feature extraction (base model freeze) ---
    history1 = model.fit(
        train_ds, validation_data=valid_ds,
        epochs=EPOCHS, callbacks=callbacks,
    )

    # --- Tahap 2: Fine-tuning (unfreeze sebagian layer) ---
    model = fine_tune_model(model, base_model)
    history2 = model.fit(
        train_ds, validation_data=valid_ds,
        epochs=10, callbacks=callbacks,
    )

    # Gabung history dari 2 tahap training untuk grafik yang mulus
    full_history = {
        "accuracy": history1.history["accuracy"] + history2.history["accuracy"],
        "val_accuracy": history1.history["val_accuracy"] + history2.history["val_accuracy"],
        "loss": history1.history["loss"] + history2.history["loss"],
        "val_loss": history1.history["val_loss"] + history2.history["val_loss"],
    }

    # ---- Simpan grafik accuracy & loss ----
    plot_training_history(full_history, model_name)

    # ---- Evaluasi ke test set + confusion matrix ----
    evaluate_and_plot_confusion_matrix(model, model_name)

    # ---- Simpan model final (in case checkpoint terakhir belum ke-save) ----
    model.save(f"{MODELS_DIR}/{model_name}_instruments.h5")

    return model, full_history


# ============================================================
# 6. FUNGSI VISUALISASI (grafik-grafik yang muncul setelah training)
# ============================================================
def plot_training_history(history, model_name):
    """Grafik accuracy & loss per epoch, disimpan sebagai PNG untuk ditampilkan di web/laporan."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(history["accuracy"], label="Train Accuracy")
    axes[0].plot(history["val_accuracy"], label="Validation Accuracy")
    axes[0].set_title(f"{model_name} - Accuracy per Epoch")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend()

    axes[1].plot(history["loss"], label="Train Loss")
    axes[1].plot(history["val_loss"], label="Validation Loss")
    axes[1].set_title(f"{model_name} - Loss per Epoch")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Loss")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{model_name}_training_history.png", dpi=150)
    plt.close()
    print(f"Grafik training history disimpan: {RESULTS_DIR}/{model_name}_training_history.png")


def evaluate_and_plot_confusion_matrix(model, model_name):
    """Evaluasi model ke test set, simpan confusion matrix + classification report."""
    y_true = []
    y_pred = []

    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))

    # ---- Confusion matrix ----
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(14, 12))
    sns.heatmap(cm, annot=False, cmap="Blues", xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Prediksi")
    plt.ylabel("Label Asli")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{model_name}_confusion_matrix.png", dpi=150)
    plt.close()

    # ---- Classification report (precision, recall, f1-score per kelas) ----
    report = classification_report(y_true, y_pred, target_names=CLASS_NAMES)
    with open(f"{RESULTS_DIR}/{model_name}_classification_report.txt", "w") as f:
        f.write(report)

    print(f"\nClassification Report - {model_name}:\n{report}")


# ============================================================
# 7. JALANKAN TRAINING UNTUK KEDUA ARSITEKTUR
# ============================================================
if __name__ == "__main__":
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mnv2_preprocess
    from tensorflow.keras.applications.efficientnet import preprocess_input as effnet_preprocess

    mobilenet, hist_mnv2 = train_and_evaluate(MobileNetV2, mnv2_preprocess, "mobilenetv2")
    efficientnet, hist_effnet = train_and_evaluate(EfficientNetB0, effnet_preprocess, "efficientnetb0")

    print("\n>>> TRAINING SELESAI. Cek folder models/ dan static/images/results/ untuk hasilnya.")