import streamlit as st
import penjualan,stok,pengeluaran
st.set_page_config(page_title="Aplikasi Penjualan", layout="wide")

# Sidebar menu
menu = st.sidebar.selectbox("Menu:", ["Penjualan", "Stok", "Pengeluaran"])



# Navigasi
match menu:
    case "Penjualan":
        penjualan.penjualan()
    case "Stok":
        stok.stok()
    case "Pengeluaran":
        pengeluaran.pengeluaran()
        

