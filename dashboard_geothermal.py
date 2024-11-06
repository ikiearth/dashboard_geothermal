import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
            daya_spekulatif = luas_prospek * data["daya_per_satuan_luas"] * (data["konversi_energi"] / 100)
            return {
                "kategori": kategori,
                "daya_spekulatif": daya_spekulatif,
                "satuan": "MWe"
            }
    return None

# Konfigurasi Tampilan Streamlit
st.set_page_config(
    page_title="Geothermal Energy Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("Dashboard Daya Spekulatif Panas Bumi")
st.write("Masukkan data di bawah ini untuk menghitung daya spekulatif pada lapangan panas bumi.")

# Sidebar untuk Input Data
st.sidebar.header("Input Data")
luas_prospek = st.sidebar.number_input("Luas Prospek (km²)", min_value=0.0, value=5.17, step=0.01)
suhu_reservoir = st.sidebar.number_input("Suhu Reservoir (°C)", min_value=0.0, value=273.0, step=1.0)

# Button untuk Menghitung Daya
if st.sidebar.button("Hitung Daya Spekulatif"):
    hasil = hitung_daya_spekulatif(luas_prospek, suhu_reservoir)
    
    if hasil:
        st.subheader("Hasil Perhitungan Daya Spekulatif")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Kategori Temperatur:** {hasil['kategori']}")
            st.write(f"**Daya Spekulatif:** {hasil['daya_spekulatif']} {hasil['satuan']}")
        
        with col2:
            # Grafik Daya Spekulatif
            fig, ax = plt.subplots()
            ax.bar(["Daya Spekulatif"], [hasil['daya_spekulatif']], color='skyblue')
            ax.set_ylabel("Daya (MWe)")
            ax.set_title("Grafik Daya Spekulatif")
            st.pyplot(fig)
    else:
        st.error("Tidak ada kategori suhu yang sesuai untuk perhitungan daya spekulatif.")

# Informasi Pembagian Kelas Suhu
st.markdown("---")
st.subheader("Pembagian Kelas Temperatur Panas Bumi")
st.write("Pembagian kelas temperatur panas bumi berdasarkan batas temperatur (SNI, 1999):")

# Menampilkan tabel dalam bentuk DataFrame
data_table = pd.DataFrame({
    "Kategori": ["Temperatur rendah", "Temperatur sedang", "Temperatur tinggi"],
    "Batas Suhu (°C)": ["<125", "125-225", ">225"],
    "Daya per Satuan Luas (MWe/km²)": [10, 12.5, 15],
    "Konversi Energi (%)": [10, 12.5, 15]
})
st.table(data_table)

# Footer
st.markdown("---")
st.markdown("### Tentang Dashboard")
st.info("Dashboard ini dirancang untuk mempermudah perhitungan daya spekulatif pada lapangan panas bumi. "
        "Anda dapat memasukkan luas prospek dan suhu reservoir untuk mendapatkan hasil estimasi daya.")
