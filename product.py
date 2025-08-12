import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import utils

def stok():
    st.header("📦 Halaman Stok")
    
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    # Ambil semua data barang
    cursor.execute("SELECT * FROM varian_product")
    barang_list = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    data_stok = st.selectbox("Menu", ["Data", "Tambah", "Tracking"], index=2)

    match data_stok:
        # Data stok
        case "Data":
            st.subheader("Data Stok Barang")
            if barang_list:
                df = pd.DataFrame(barang_list, columns=col_names)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Belum ada data barang di database.")
                
        # Tambah stok
        case "Tambah":
            st.subheader("Tambah / Lihat Info Stok")
            with st.form("update_stok_form"):
                tanggal = st.date_input("Tanggal", value=datetime.today())
                jam = st.time_input("Jam", value=datetime.now().time())
                kode_barang = st.selectbox("ID Varian Product", [b[0] for b in barang_list])
                jumlah_input = st.number_input("Tambah Stok", min_value=1, step=1)

                col1, col2 = st.columns(2)
                with col1:
                    cek_info = st.form_submit_button("Lihat Informasi")
                with col2:
                    tambah_stok = st.form_submit_button("Tambah Stok")

            # Logika jika tombol ditekan
            if cek_info:
                cursor.execute("""
                    SELECT nama_barang, merek, kategori, harga_satuan, stok, expired_date
                    FROM varian_product 
                    WHERE id_varian=?
                """, (kode_barang,))
                data = cursor.fetchone()
                if data:
                    nama_barang, merek, kategori, harga_satuan, stok, expired_date = data
                    st.success(f"Nama Barang : {nama_barang}")
                    st.success(f"Merek       : {merek}")
                    st.success(f"Kategori    : {kategori}")
                    st.success(f"Harga       : {utils.format_rp(harga_satuan)}")
                    st.success(f"Stok Terkini: {stok}")
                    st.success(f"Expired Date: {expired_date}")
                else:
                    st.error("Barang tidak ditemukan.")

            elif tambah_stok:
                cursor.execute("""
                    UPDATE varian_product
                    SET stok = stok + ?
                    WHERE id_varian = ?
                """, (jumlah_input, kode_barang))
                conn.commit()
                st.success(f"Stok barang ID {kode_barang} berhasil ditambah {jumlah_input}.")
        case "Tracking":
            st.subheader("📍 Tracking Produk")

            # Input pencarian
            search_type = st.radio("Cari Berdasarkan:", ["ID Varian", "Nama Produk"], horizontal=True)
            if search_type == "ID Varian":
                search_value = st.text_input("Masukkan ID Varian")
            else:
                search_value = st.text_input("Masukkan Nama Produk")

            if st.button("🔍 Cari"):
                if search_type == "ID Varian":
                    cursor.execute("SELECT * FROM varian_product WHERE id_varian = ?", (search_value,))
                else:
                    cursor.execute("SELECT * FROM varian_product WHERE nama_barang LIKE ?", (f"%{search_value}%",))

                product = cursor.fetchone()

                if product:
                    # Ambil nama kolom
                    col_names_barang = [desc[0] for desc in cursor.description]
                    df_product = pd.DataFrame([product], columns=col_names_barang)

                    # Tampilkan info barang
                    st.markdown("### 📦 Posisi Sekarang")
                    st.dataframe(df_product, use_container_width=True)

                    # Ambil stok
                    stok_sekarang = product[col_names_barang.index("stok")]
                    st.info(f"**Stok Terkini:** {stok_sekarang}")

                    # Ambil riwayat penjualan
                    st.markdown("### 📜 Riwayat Penjualan")
                    query_penjualan = """
                        SELECT p.tanggal, p.jam, dt.qty, dt.harga_satuan, (dt.qty * dt.harga_satuan) AS total
                        FROM detail_transaksi dt
                        JOIN penjualan p ON dt.id_transaksi = p.id
                        WHERE dt.varian_barang = ?
                        ORDER BY p.tanggal DESC, p.jam DESC
                    """
                    cursor.execute(query_penjualan, (product[0],))  # product[0] = id_varian
                    penjualan_data = cursor.fetchall()
                    col_names_penjualan = [desc[0] for desc in cursor.description]

                    if penjualan_data:
                        df_penjualan = pd.DataFrame(penjualan_data, columns=col_names_penjualan)
                        df_penjualan["Tanggal"] = pd.to_datetime(df_penjualan["tanggal"]).dt.strftime("%d-%m-%Y")
                        df_penjualan["Jumlah"] = df_penjualan["qty"].astype(int)
                        df_penjualan["Total Harga"] = df_penjualan["total"].apply(lambda x: utils.format_rp(x))
                        
                        styled_df = df_penjualan.style.set_properties(**{'background-color': 'black',
                           'color': 'lawngreen',
                           'border': '2px solid blue'})

                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.warning("Belum ada riwayat penjualan untuk produk ini.")
                else:
                    st.error("Produk tidak ditemukan.")
            
                    
    conn.close()
