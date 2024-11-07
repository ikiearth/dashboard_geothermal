import streamlit as st

# Data parameter berdasarkan kategori suhu
data_reservoir = {
    "Temperatur rendah": {
        "batas_temp": (0, 125),
        "temp_akhir_cut_off": 90,
        "daya_per_satuan_luas": 10,  # MWe/km^2
        "konversi_energi": 10  # %
    },
    "Temperatur sedang": {
        "batas_temp": (125, 225),
        "temp_akhir_cut_off": 120,
        "daya_per_satuan_luas": 12.5,  # MWe/km^2
        "konversi_energi": 12.5  # %
    },
    "Temperatur tinggi": {
        "batas_temp": (225, float('inf')),
        "temp_akhir_cut_off": 180,
        "daya_per_satuan_luas": 15,  # MWe/km^2
        "konversi_energi": 15  # %
    }
}

# Fungsi untuk menghitung daya spekulatif
def hitung_daya_spekulatif(luas_prospek, suhu_reservoir):
    for kategori, data in data_reservoir.items():
        batas_min, batas_max = data["batas_temp"]
        if batas_min <= suhu_reservoir < batas_max:
            daya_spekulatif = luas_prospek * data["daya_per_satuan_luas"]
            return {
                "kategori": kategori,
                "daya_spekulatif": daya_spekulatif,
                "satuan": "MWe"
            }
    return None

# Fungsi untuk konversi energi
def hitung_konversi_energi(luas_prospek, suhu_reservoir):
    for kategori, data in data_reservoir.items():
        batas_min, batas_max = data["batas_temp"]
        if batas_min <= suhu_reservoir < batas_max:
            daya_spekulatif = luas_prospek * data["daya_per_satuan_luas"] * (data["konversi_energi"] / 100)
            return {
                "kategori": kategori,
                "daya_spekulatif": daya_spekulatif,
                "satuan": "MWe"
            }
    return None

# Streamlit App
st.title("Dashboard Daya Spekulatif Panas Bumi")
st.write("Created by: Mukhammad Sholikhuddin - Kelompok GeoVentur4")
st.write("Masukkan data di bawah ini untuk menghitung daya spekulatif pada lapangan panas bumi.")

# Input nama lapangan dari user
nama_lapangan = st.text_input("Nama Lapangan Panas Bumi", "")

# Pilihan metode input
st.subheader("Input Luas Prospek")
input_method_luas = st.radio("Pilih metode input untuk Luas Prospek:", ("Slider", "Ketik Nilai"))

if input_method_luas == "Slider":
    luas_prospek = st.slider("Luas Prospek (km²)", min_value=0.0, max_value=300.0, value=5.17, step=0.01)
else:
    luas_prospek = st.number_input("Luas Prospek (km²)", min_value=0.0, value=5.17, step=0.01)

st.subheader("Input Suhu Reservoir")
input_method_suhu = st.radio("Pilih metode input untuk Suhu Reservoir:", ("Slider", "Ketik Nilai"))

if input_method_suhu == "Slider":
    suhu_reservoir = st.slider("Suhu Reservoir (°C)", min_value=0, max_value=350, value=273, step=1)
else:
    suhu_reservoir = st.number_input("Suhu Reservoir (°C)", min_value=0, max_value=350, value=273, step=1)

# Hasil perhitungan otomatis tanpa tombol
if nama_lapangan:
    hasil = hitung_daya_spekulatif(luas_prospek, suhu_reservoir)
    hasil_energi = hitung_konversi_energi(luas_prospek, suhu_reservoir)
    
    if hasil:
        st.success(f"Hasil Perhitungan Daya Spekulatif untuk Lapangan: {nama_lapangan}")
        st.write(f"**Kategori Temperatur:** {hasil['kategori']}")
        st.write(f"**Daya Spekulatif:** {hasil['daya_spekulatif']} {hasil['satuan']}")
        st.write(f"**Konversi Energi:** {hasil_energi['daya_spekulatif']} {hasil['satuan']}")
    else:
        st.error("Tidak ada kategori suhu yang sesuai untuk perhitungan daya spekulatif.")
else:
    st.warning("Silakan masukkan nama lapangan.")

# Tabel Pembagian Kelas Suhu
st.write("Pembagian kelas temperatur panas bumi berdasarkan batas temperatur (SNI, 1999):")
st.dataframe({
    "Kategori": ["Temperatur rendah", "Temperatur sedang", "Temperatur tinggi"],
    "Batas Suhu (°C)": ["<125", "125-225", ">225"],
    "Daya per Satuan Luas (MWe/km²)": [10, 12.5, 15],
    "Konversi Energi (%)": [10, 12.5, 15]
})
