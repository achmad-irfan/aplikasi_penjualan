import streamlit as st
import sqlite3
from datetime import datetime

def penjualan():
    st.header("📦 Halaman Penjualan")
    # Koneksi database
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    # --- Ambil list barang ---
    cursor.execute("SELECT kode_barang, nama_barang, harga_satuan, stok FROM barang")
    barang_list = cursor.fetchall()

    # --- Session state untuk keranjang ---
    if "cart" not in st.session_state:
        st.session_state.cart = []


    # Form tambah barang ke keranjang
    with st.form("form_tambah"):
        buyer = st.text_input("Kode Pembeli")
        telp= st.text_input("No Telp")
        tanggal = st.date_input("Tanggal", value=datetime.today())
        jam = st.time_input("Jam", value=datetime.now().time())
        metode=st.selectbox("Metode Pembayaran", ["Cash","QRIS","Debet","Kredit","Voucher"])

        nama_barang = st.selectbox("Pilih Barang", [b[1] for b in barang_list])
        qty = st.number_input("Qty", min_value=1, step=1)

        submitted = st.form_submit_button("Tambah ke Keranjang")

        if submitted:
            # Cari kode, harga & stok barang
            selected_barang = next(b for b in barang_list if b[1] == nama_barang)
            kode_barang, _, harga, stok = selected_barang

        
            total = harga * qty
            st.session_state.cart.append({
                "kode_barang": kode_barang,
                "nama_barang": nama_barang,
                "harga": harga,
                "qty": qty,
                "total": total
            })
            st.success(f"{nama_barang} ditambahkan ke keranjang")

    # Tampilkan keranjang
    if st.session_state.cart:
        st.subheader("Keranjang Belanja")
        st.table(st.session_state.cart)
        grand_total = sum(item["total"] for item in st.session_state.cart)
        st.write(f"**Total Bayar:** Rp {grand_total:,}")

        if st.button("Simpan Penjualan"):
            jam_str = jam.strftime("%H:%M:%S")
            cursor.execute("""
                INSERT INTO BUYER (nama,hp)
                VALUES (?,?)""",(buyer,telp))
            for item in st.session_state.cart:
                # Simpan penjualan
                cursor.execute("""
                    INSERT INTO penjualan (tanggal, jam, buyer, kode_barang, qty, total)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (tanggal, jam_str, buyer, item["kode_barang"], item["qty"], item["total"]))

                # Kurangi stok barang
                cursor.execute("""
                    UPDATE barang
                    SET stok = stok - ?
                    WHERE kode_barang = ?
                """, (item["qty"], item["kode_barang"]))

            conn.commit()
            st.success("Penjualan berhasil disimpan dan stok barang diperbarui!")
            st.session_state.cart.clear()