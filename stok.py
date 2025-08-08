import streamlit as st
import sqlite3
import pandas as pd

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
    
    # Jika ada data, tampilkan tabel
    if barang_list:
        df = pd.DataFrame(barang_list, columns=col_names)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Belum ada data barang di database.")


  

    