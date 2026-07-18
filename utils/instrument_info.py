"""
Informasi edukatif untuk tiap kelas alat musik.
Dipakai di halaman hasil klasifikasi dan halaman dataset,
supaya web tidak cuma menampilkan nama tapi juga penjelasan singkat.
"""

INSTRUMENT_INFO = {
    "Didgeridoo": {"kategori": "Tiup", "deskripsi": "Alat musik tiup tradisional suku Aborigin Australia, berbentuk tabung panjang dari kayu berongga."},
    "Tambourine": {"kategori": "Perkusi", "deskripsi": "Alat musik pukul berbentuk lingkaran dengan keping logam di sisinya, dimainkan dengan dipukul atau digoyang."},
    "Xylophone": {"kategori": "Perkusi", "deskripsi": "Alat musik pukul bernada, terdiri dari bilah kayu dengan ukuran berbeda yang dipukul menggunakan stik."},
    "acordian": {"kategori": "Aerofon (Free Reed)", "deskripsi": "Alat musik dengan bellow (kotak angin) dan tuts, populer dalam musik rakyat Eropa."},
    "alphorn": {"kategori": "Tiup", "deskripsi": "Alat musik tiup kayu sangat panjang, tradisional dari pegunungan Alpen Swiss."},
    "bagpipes": {"kategori": "Tiup", "deskripsi": "Alat musik tiup dengan kantong udara, identik dengan musik tradisional Skotlandia."},
    "banjo": {"kategori": "Senar (Petik)", "deskripsi": "Alat musik petik berdawai dengan badan bundar bermembran, umum dalam musik country/bluegrass."},
    "bongo drum": {"kategori": "Perkusi", "deskripsi": "Sepasang drum kecil yang dimainkan dengan tangan, berasal dari musik Afro-Kuba."},
    "casaba": {"kategori": "Perkusi", "deskripsi": "Alat musik goyang (shaker) berupa labu berisi biji-bijian atau dililit manik, dari Afrika Barat."},
    "castanets": {"kategori": "Perkusi", "deskripsi": "Sepasang keping kayu/kerang kecil yang diketuk dengan jari, identik dengan tarian flamenco Spanyol."},
    "clarinet": {"kategori": "Tiup (Single Reed)", "deskripsi": "Alat musik tiup kayu dengan satu reed tunggal, umum dalam orkestra dan musik jazz."},
    "clavichord": {"kategori": "Senar (Keyboard)", "deskripsi": "Alat musik keyboard kuno bersenar, cikal bakal piano, populer di era Barok."},
    "concertina": {"kategori": "Aerofon (Free Reed)", "deskripsi": "Alat musik bellow berbentuk heksagonal, mirip akordeon namun lebih kecil dan portabel."},
    "drums": {"kategori": "Perkusi", "deskripsi": "Satu set drum yang terdiri dari beberapa drum dan simbal, tulang punggung ritme dalam band modern."},
    "dulcimer": {"kategori": "Senar (Pukul/Petik)", "deskripsi": "Alat musik dawai yang dimainkan dengan dipetik atau dipukul palu kecil, populer dalam musik rakyat Amerika."},
    "flute": {"kategori": "Tiup", "deskripsi": "Alat musik tiup tanpa reed, suara dihasilkan dari hembusan udara melewati lubang tiup."},
    "guiro": {"kategori": "Perkusi", "deskripsi": "Alat musik gesek beralur dari labu atau kayu, dimainkan dengan digosok tongkat, khas musik Latin."},
    "guitar": {"kategori": "Senar (Petik)", "deskripsi": "Alat musik petik berdawai enam, salah satu alat musik paling populer di dunia."},
    "harmonica": {"kategori": "Tiup (Free Reed)", "deskripsi": "Alat musik tiup kecil yang dimainkan dengan mulut, umum dalam musik blues dan folk."},
    "harp": {"kategori": "Senar (Petik)", "deskripsi": "Alat musik dawai besar berbentuk segitiga, dipetik dengan kedua tangan, umum dalam orkestra klasik."},
    "marakas": {"kategori": "Perkusi", "deskripsi": "Sepasang alat musik goyang (shaker) berisi biji-bijian, khas musik Latin Amerika."},
    "ocarina": {"kategori": "Tiup", "deskripsi": "Alat musik tiup kecil berbentuk oval dari tanah liat/keramik, sudah ada sejak zaman kuno."},
    "piano": {"kategori": "Senar (Keyboard)", "deskripsi": "Alat musik keyboard dengan dawai yang dipukul palu internal saat tuts ditekan."},
    "saxaphone": {"kategori": "Tiup (Single Reed)", "deskripsi": "Alat musik tiup logam dengan reed tunggal, ikon utama dalam musik jazz."},
    "sitar": {"kategori": "Senar (Petik)", "deskripsi": "Alat musik dawai panjang dari India, dikenal dengan suara resonansi khasnya dalam musik klasik Hindustan."},
    "steel drum": {"kategori": "Perkusi", "deskripsi": "Alat musik pukul bernada dari drum logam yang dibentuk, berasal dari Trinidad dan Tobago."},
    "trombone": {"kategori": "Tiup (Brass)", "deskripsi": "Alat musik tiup logam dengan slide untuk mengubah nada, umum dalam orkestra dan jazz band."},
    "trumpet": {"kategori": "Tiup (Brass)", "deskripsi": "Alat musik tiup logam dengan tiga piston/katup, dikenal dengan suara nyaring dan cerah."},
    "tuba": {"kategori": "Tiup (Brass)", "deskripsi": "Alat musik tiup logam berukuran besar dengan nada terendah dalam keluarga brass."},
    "violin": {"kategori": "Senar (Gesek)", "deskripsi": "Alat musik dawai yang dimainkan dengan digesek busur, alat musik utama dalam orkestra klasik."},
}


def get_instrument_info(label):
    """Ambil info instrumen berdasarkan nama label hasil prediksi."""
    return INSTRUMENT_INFO.get(label, {"kategori": "Tidak diketahui", "deskripsi": "Informasi belum tersedia untuk kelas ini."})