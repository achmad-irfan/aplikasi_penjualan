import streamlit as st
import sqlite3
from datetime import date

def pengeluaran():
    st.header("💸 Halaman Pengeluaran")

    # Koneksi database
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    # Buat tabel pengeluaran jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pengeluaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            kategori TEXT NOT NULL,
            deskripsi TEXT,
            nominal REAL NOT NULL,
            metode TEXT
        )
    """)
    conn.commit()

    # --- Form Tambah Pengeluaran ---
    st.subheader("➕ Tambah Pengeluaran")
    with st.form("form_pengeluaran", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("Tanggal", value=date.today())
            kategori = st.selectbox("Kategori", [
                "Pembelian Barang",
                "Gaji Karyawan",
                "Sewa Tempat",
                "Listrik/Air/Internet",
                "Transportasi/Ongkos Kirim",
                "Peralatan/Maintenance",
                "Lain-lain"
            ])
        with col2:
            nominal = st.number_input("Nominal (Rp)", min_value=0, step=1000)
            metode = st.selectbox("Metode Pembayaran", ["Tunai", "Transfer Bank", "E-Wallet", "Lainnya"])

        deskripsi = st.text_area("Deskripsi", placeholder="Contoh: Bayar listrik bulan Agustus")

        submitted = st.form_submit_button("Simpan Pengeluaran")
        if submitted:
            cursor.execute("""
                INSERT INTO pengeluaran (tanggal, kategori, deskripsi, nominal, metode)
                VALUES (?, ?, ?, ?, ?)
            """, (tanggal.strftime("%Y-%m-%d"), kategori, deskripsi, nominal, metode))
            conn.commit()
            st.success("✅ Pengeluaran berhasil disimpan!")

    st.divider()

    # --- Filter Data ---
    st.subheader("📊 Daftar Pengeluaran")
    col1, col2 = st.columns(2)
    with col1:
        filter_bulan = st.text_input("Filter Bulan (YYYY-MM)", placeholder="2025-08")
    with col2:
        filter_kategori = st.selectbox("Filter Kategori", ["Semua"] + [
            "Pembelian Barang",
            "Gaji Karyawan",
            "Sewa Tempat",
            "Listrik/Air/Internet",
            "Transportasi/Ongkos Kirim",
            "Peralatan/Maintenance",
            "Lain-lain"
        ])

    query = "SELECT tanggal, kategori, deskripsi, nominal, metode FROM pengeluaran WHERE 1=1"
    params = []

    if filter_bulan:
        query += " AND strftime('%Y-%m', tanggal) = ?"
        params.append(filter_bulan)

    if filter_kategori != "Semua":
        query += " AND kategori = ?"
        params.append(filter_kategori)

    query += " ORDER BY tanggal DESC"

    cursor.execute(query, params)
    data = cursor.fetchall()

    # --- Tampilkan Tabel ---
    if data:
        st.table({
            "Tanggal": [row[0] for row in data],
            "Kategori": [row[1] for row in data],
            "Deskripsi": [row[2] for row in data],
            "Nominal (Rp)": [f"{row[3]:,.0f}" for row in data],
            "Metode": [row[4] for row in data]
        })

        # Total pengeluaran
        total = sum([row[3] for row in data])
        st.success(f"💰 Total Pengeluaran: Rp {total:,.0f}")
    else:
        st.info("Belum ada data pengeluaran.")

    conn.close()
