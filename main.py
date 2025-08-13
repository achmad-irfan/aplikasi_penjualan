import streamlit as st
import penjualan, product, pengeluaran, data

st.set_page_config(page_title="Aplikasi Penjualan", layout="wide")

# ===== Custom CSS =====
st.markdown("""
    <style>
        /* ===== SIDEBAR STYLE ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #198754 0%, #157347 100%);
            padding-top: 20px;
            box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
        }

        /* Judul menu di sidebar */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] label {
            color: white !important;
            font-weight: 600;
        }

        /* Selectbox container */
        [data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            padding: 2px 6px;
        }

        /* Text di dalam selectbox */
        [data-testid="stSidebar"] div[data-baseweb="select"] span {
            color: white !important;
            font-weight: 500 !important;
        }

        /* Dropdown list saat dibuka */
        [data-testid="stSidebar"] div[role="listbox"] {
            background-color: #198754 !important;
            border-radius: 8px;
        }

        /* Item di dropdown */
        [data-testid="stSidebar"] div[role="option"] {
            color: white !important;
            padding: 8px 12px;
        }

        /* Hover item dropdown */
        [data-testid="stSidebar"] div[role="option"]:hover {
            background-color: rgba(255, 255, 255, 0.15) !important;
            border-radius: 4px;
        }

        /* ===== MAIN CONTENT STYLE ===== */
        .element-container {
            border: 1px solid rgba(0, 0, 0, 0.15);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 16px;
            background-color: #B7CEEC;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        /* Heading style */
        h1, h2, h3 {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-weight: bold;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# ===== Sidebar Menu =====
menu = st.sidebar.selectbox(
    "Menu:",
    ["Penjualan", "Product", "Pengeluaran", "Laporan dan Data"],
    index=0
)

# ===== Navigation =====
match menu:
    case "Penjualan":
        penjualan.penjualan()
    case "Product":
        product.stok()
    case "Pengeluaran":
        pengeluaran.pengeluaran()
    case "Laporan dan Data":
        data.dashboard()
