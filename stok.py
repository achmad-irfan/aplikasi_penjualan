import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

def stok():
    st.header("📦 Halaman Stok")
    # Koneksi database
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    # --- Ambil list barang ---
    cursor.execute("SELECT * FROM barang")
    barang_list = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    
    conn.close()
    
    data_stok= st.selectbox("Stok",["Data","Update"])
    
    match data_stok:
        # Data Stok
        case "Data":
            st.subheader("Data Stok Barang")
            # Jika ada data, tampilkan tabel
            if barang_list:
                df = pd.DataFrame(barang_list, columns=col_names)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Belum ada data barang di database.")
        
        # Update Stok:
        case "Update":
            st.subheader("Update Stok Barang")
            id_nama= col_names.index("nama_barang")
            id_stok= col_names.index("stok")
            with st.form("Update Stok"):
                tanggal = st.date_input("Tanggal", value=datetime.today())
                jam = st.time_input("Jam", value=datetime.now().time())
                nama_barang = st.selectbox("Pilih Barang", [b[0] for b in barang_list])
                jumlah = st.number_input("Jumlah",min_value=1,step=1)
                

            # if st.button("Update Stok"):
                
  

    