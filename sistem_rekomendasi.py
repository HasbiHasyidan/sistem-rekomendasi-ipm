import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
dataset = pd.read_csv('dataset IPM.csv')

# Preprocessing kolom numerik
kolom_numerik = ['Jumlah AHH', 'Jumlah RLS', 'Jumlah HLS', 'Pengeluaran', 'Jumlah IPM']
for col in kolom_numerik:
    dataset[col] = (
        dataset[col]
        .astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )

# Normalisasi (kecuali IPM)
numerical_cols = ['Jumlah AHH', 'Jumlah RLS', 'Jumlah HLS', 'Pengeluaran']
scaler = MinMaxScaler()
dataset_scaled = dataset.copy()
dataset_scaled[numerical_cols] = scaler.fit_transform(dataset[numerical_cols])

# Gap Score
dataset_scaled['Gap Score'] = 1 - dataset_scaled[numerical_cols].mean(axis=1)

# Clustering Peer Group (Hybrid Learning awal)
kmeans = KMeans(n_clusters=4, random_state=42)
dataset_scaled['Peer Group'] = kmeans.fit_predict(dataset_scaled[numerical_cols])

# Tambahkan kembali metadata
prioritas = dataset_scaled.copy()
prioritas['Jumlah IPM'] = dataset['Jumlah IPM']
prioritas['Kota'] = dataset['Kota']
prioritas['Provinsi'] = dataset['Provinsi']

# Fungsi untuk mencari dimensi terlemah
def weakest_dimension(row):
    scores = {
        'Kesehatan (AHH)': row['Jumlah AHH'],
        'Pendidikan - RLS': row['Jumlah RLS'],
        'Pendidikan - HLS': row['Jumlah HLS'],
        'Standar Hidup (PPK)': row['Pengeluaran'],
    }
    return min(scores, key=scores.get)

prioritas['Dimensi Terlemah'] = dataset[numerical_cols].apply(weakest_dimension, axis=1)

# Bar Chart Profil Kota
def plot_bar_profile(dimensions, values, title):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=dimensions, y=values, palette='pastel', ax=ax)
    ax.set_ylim(0, 1)
    ax.set_title(f"Profil Dimensi Kota: {title}")
    ax.set_ylabel("Skor Normalisasi")
    ax.set_xlabel("Dimensi")
    for i, v in enumerate(values):
        ax.text(i, v + 0.03, f"{v:.2f}", ha='center', fontweight='bold')
    return fig

# Streamlit UI
st.set_page_config(page_title="Sistem Rekomendasi IPM", layout="wide")
st.title("📊 Sistem Rekomendasi Prioritas Pembangunan Daerah Berbasis IPM")

# Sidebar filter
st.sidebar.header("Filter Pencarian")
provinsi = st.sidebar.selectbox("Pilih Provinsi", options=sorted(prioritas['Provinsi'].unique()))
filtered = prioritas[prioritas['Provinsi'] == provinsi].copy()

if filtered.empty:
    st.warning("Data tidak ditemukan untuk provinsi tersebut.")
    st.stop()

kota = st.sidebar.selectbox("Pilih Kota", options=sorted(filtered['Kota'].unique()))
filtered_kota = filtered[filtered['Kota'] == kota].iloc[0]

# Kota prioritas berdasarkan Gap Score & IPM
kota_terendah_gap = filtered.loc[filtered['Gap Score'].idxmin()]
kota_terendah_ipm = filtered.loc[filtered['Jumlah IPM'].idxmin()]
dimensi_terlemah_ipm = weakest_dimension(kota_terendah_ipm)

# Rekomendasi per dimensi
rekom_dict = {
    'Kesehatan (AHH)': 'Perkuat layanan kesehatan dan program gizi.',
    'Pendidikan - RLS': 'Tingkatkan akses pendidikan dasar.',
    'Pendidikan - HLS': 'Perluas akses pendidikan menengah/tinggi.',
    'Standar Hidup (PPK)': 'Dorong ekonomi lokal dan bantuan sosial.'
}

# Tab layout
tab1, tab2 = st.tabs(["Detail Kota", " Dashboard Provinsi"])

with tab1:
    st.subheader(f"Detail Kota: {kota}")
    st.write(f"**Provinsi:** {provinsi}")
    st.write(f"**IPM:** {filtered_kota['Jumlah IPM']:.2f}")
    st.write(f"**Gap Score:** {filtered_kota['Gap Score']:.2f}")
    st.write(f"**Dimensi Terlemah:** {filtered_kota['Dimensi Terlemah']}")
    st.success(f"**Rekomendasi:** {rekom_dict[filtered_kota['Dimensi Terlemah']]}")

    st.markdown(
        """
        **Penjelasan istilah:**
        - **AHH**: Angka Harapan Hidup (indikator Kesehatan)  
        - **RLS**: Rata-rata Lama Sekolah (pendidikan dasar)  
        - **HLS**: Harapan Lama Sekolah (pendidikan menengah/tinggi)  
        - **PPK**: Pengeluaran Per Kapita (indikator standar hidup)
        """
    )

    # Bar chart
    dimensi_labels = ['Kesehatan (AHH)', 'Pendidikan - RLS', 'Pendidikan - HLS', 'Standar Hidup (PPK)']
    dimensi_values = filtered_kota[numerical_cols].tolist()
    fig_bar = plot_bar_profile(dimensi_labels, dimensi_values, kota)
    st.pyplot(fig_bar)

with tab2:
    st.subheader(f"Dashboard Provinsi: {provinsi}")

    avg_ipm = filtered['Jumlah IPM'].mean()
    st.metric(label="IPM Rata-rata Provinsi", value=f"{avg_ipm:.2f}")

    st.markdown("##  Rekomendasi Prioritas Pembangunan di Provinsi Ini")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Berdasarkan Gap Score (Ketimpangan)")
        st.write(f"- Kota: **{kota_terendah_gap['Kota']}**")
        st.write(f"- Gap Score: {kota_terendah_gap['Gap Score']:.2f}")
        st.write(f"- Dimensi Terlemah: {kota_terendah_gap['Dimensi Terlemah']}")
        st.success(f"Rekomendasi: {rekom_dict[kota_terendah_gap['Dimensi Terlemah']]}")

    with col2:
        st.markdown("#### Berdasarkan IPM Terendah (Pembangunan Umum)")
        st.write(f"- Kota: **{kota_terendah_ipm['Kota']}**")
        st.write(f"- IPM: {kota_terendah_ipm['Jumlah IPM']:.2f}")
        st.write(f"- Dimensi Terlemah: **{dimensi_terlemah_ipm}**")
        st.success(f"Rekomendasi: {rekom_dict[dimensi_terlemah_ipm]}")

    # Data table
    st.markdown("### Tabel Kota di Provinsi")
    tabel_kota = filtered[['Kota', 'Jumlah IPM', 'Gap Score', 'Peer Group']].sort_values('Gap Score')
    st.dataframe(tabel_kota.reset_index(drop=True))

    # Histogram IPM
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.histplot(filtered['Jumlah IPM'], bins=10, kde=True, ax=ax1, color='skyblue')
    ax1.set_title('Distribusi IPM di Provinsi')
    ax1.set_xlabel('Jumlah IPM')
    ax1.set_ylabel('Jumlah Kota')
    st.pyplot(fig1)

    # Visualisasi Peer Group
    st.markdown("### Visualisasi Peer Group (Wilayah Sejenis)")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=filtered, x='Jumlah IPM', y='Gap Score', hue='Peer Group', palette='tab10', ax=ax2)
    ax2.set_title('Scatterplot IPM vs Gap Score per Peer Group')
    st.pyplot(fig2)

st.markdown("---")
st.caption("Sistem ini membantu menentukan prioritas pembangunan berdasarkan analisis IPM, Gap Score, dan clustering wilayah sejenis.")
