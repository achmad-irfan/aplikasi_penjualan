import streamlit as st
import penjualan,product,pengeluaran
import pathlib

st.set_page_config(page_title="Aplikasi Penjualan", layout="wide")

# # Function to load CSS from the 'assets' folder
# def load_css(file_path):
#     with open(file_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# # Load the external CSS
# css_path = pathlib.Path("styles.css")
# load_css(css_path)


# Sidebar menu
menu = st.sidebar.selectbox("Menu:", ["Penjualan", "Product", "Pengeluaran"], index=1 )



# Navigasi
match menu:
    case "Penjualan":
        penjualan.penjualan()
    case "Product":
        product.stok()
    case "Pengeluaran":
        pengeluaran.pengeluaran()
        

