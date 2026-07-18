"""
Daftar nama kelas alat musik, urutannya PERSIS sama dengan hasil training
(diambil dari log 'Urutan kelas' saat train_model.py dijalankan).
JANGAN diubah urutannya kecuali kamu training ulang dan urutannya berubah.
"""

CLASS_NAMES = [
    "Didgeridoo", "Tambourine", "Xylophone", "acordian", "alphorn",
    "bagpipes", "banjo", "bongo drum", "casaba", "castanets",
    "clarinet", "clavichord", "concertina", "drums", "dulcimer",
    "flute", "guiro", "guitar", "harmonica", "harp",
    "marakas", "ocarina", "piano", "saxaphone", "sitar",
    "steel drum", "trombone", "trumpet", "tuba", "violin",
]

NUM_CLASSES = len(CLASS_NAMES)