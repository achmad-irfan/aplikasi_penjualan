import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import struk
import rupiah

def penjualan():
    st.header("📦 Halaman Penjualan")
    # Koneksi database
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    # --- Ambil list barang ---
    cursor.execute("SELECT kode_barang, nama_barang, harga_satuan, stok, diskon FROM barang")
    barang_list = cursor.fetchall()

    # --- Session state untuk keranjang ---
    if "cart" not in st.session_state:
        st.session_state.cart = []

    #Layout 2 kolom
    col1, col2= st.columns(2)
    
    with col1:
    # Form tambah barang ke keranjang
        with st.form("form_tambah"):
            st.subheader("Produk Belanja")
            buyer = st.text_input("Pembeli",key="buyer")
            telp= st.text_input("No Telp")
            tanggal = st.date_input("Tanggal", value=datetime.today())
            jam = st.time_input("Jam", value=datetime.now().time())
            metode=st.selectbox("Metode Pembayaran", ["Cash","QRIS","Debet","Kredit","Voucher"])

            nama_barang = st.selectbox("Pilih Barang", [b[1] for b in barang_list])
            qty = st.number_input("Qty", min_value=1, step=1)

            submitted = st.form_submit_button("Tambah ke Keranjang")

            if submitted:
                # Cari kode, harga, diskon & stok barang
                selected_barang = next(b for b in barang_list if b[1] == nama_barang)
                kode_barang, _, harga, stok,diskon = selected_barang

            
                total = harga * qty 
                st.session_state.cart.append({
                    "kode_barang": kode_barang,
                    "nama_barang": nama_barang,
                    "harga": harga,
                    "qty": qty,
                    "total": total ,
                    "diskon" : diskon
                })
                st.success(f"{nama_barang} ditambahkan ke keranjang")
               

    with col2:
        st.subheader("Keranjang Belanja")

        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            df_cart = df_cart.drop(columns='kode_barang')
            
            col1_, col2_, col3_, col4_, col5_, col6_ = st.columns([2, 1, 3, 3, 3, 1])
            col1_.write("Nama Barang")
            col2_.write("Qty")
            col3_.write("Total Harga")
            col4_.write("Diskon")
            col5_.write("Harga Setelah Diskon")
            col6_.write("Aksi")

            for i, row in df_cart.iterrows():
                col1_, col2_, col3_, col4_, col5_, col6_ = st.columns([2, 1, 3, 3, 3, 1])
                col1_.write(row["nama_barang"])
                col2_.write(row["qty"])
                col3_.write(f"{rupiah.format_rp(row['total'])}")
                diskon_jumlah = float(row['diskon'])/100 * float(row['total'])
                col4_.write(f" \- {rupiah.format_rp(diskon_jumlah)}")
                harga_setelah_diskon = row['total'] - diskon_jumlah
                col5_.write(f"{rupiah.format_rp(harga_setelah_diskon)}")
                if col6_.button("🗑", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.experimental_rerun()

        else:
            st.info("Keranjang masih kosong.")

        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            df_cart['diskon'] = df_cart['diskon'].astype(float)
            df_cart['harga'] = df_cart['harga'].astype(float)

            # Hitung harga diskon (misal diskon dalam persen, 0.2 untuk 20%)
            df_cart['harga_diskon'] = df_cart['diskon']* df_cart['harga']/100
            df_cart['after_diskon'] = df_cart['total']-(df_cart['harga_diskon']*df_cart["qty"])
            
            # Hitung grand total dari kolom after_diskon
            grand_total = df_cart['after_diskon'].sum()
            
            st.write(f"**Total Belanja:**  {rupiah.format_rp(grand_total)}")
            if metode == "Cash":
                st.subheader("Uang Tunai:")
                
                # Inisiliasi Uang Tunai
                if "uang_tunai" not in st.session_state:
                    st.session_state.uang_tunai=0
                
                cols = st.columns(6)
                nominals = [2000, 5000, 10000, 20000, 50000, 100000]
                
                for col, nominal in zip(cols, nominals):
                     if col.button(f"{rupiah.format_rp(nominal)}"):  # hanya tambah kalau tombol ini diklik
                         st.session_state.uang_tunai += nominal
                st.session_state.uang_tunai = st.number_input(
                    "Masukkan Uang Tunai",
                     min_value=0,
                    value=st.session_state.uang_tunai,
                    step=1000 )
                
                #Jumlah Uang Tunai
                st.success(f"Total Uang:  {rupiah.format_rp(st.session_state.uang_tunai)}")
                
                
                # Kembalian
                kembalian = st.session_state.uang_tunai - grand_total
                if kembalian <0:
                    st.error(f"Uang kurang - {rupiah.format_rp(kembalian)}")
                else:
                    st.success(f"Total Kembalian:  {rupiah.format_rp(kembalian)}")           

            if st.button("Simpan Penjualan"):
                if st.session_state.uang_tunai< grand_total:
                    st.error("Uang pembeli kurang")
                else:
                    jam_str = jam.strftime("%H:%M:%S")
                    cursor.execute("""
                        INSERT INTO BUYER (nama, hp)
                        VALUES (?, ?)
                    """, (buyer, telp))

                    for item in st.session_state.cart:
                        cursor.execute("""
                            INSERT INTO penjualan (tanggal, jam, buyer, kode_barang, qty, total)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (tanggal, jam_str, buyer, item["kode_barang"], item["qty"], item["total"]))

                        cursor.execute("""
                            UPDATE barang
                            SET stok = stok - ?
                            WHERE kode_barang = ?
                        """, (item["qty"], item["kode_barang"]))

                    conn.commit()
                    st.success("Penjualan berhasil disimpan dan stok barang diperbarui!")
                    st.session_state.cart.clear()
                    
                    # panggil program struk
                    struk.cetak_struk(df_cart, kembalian)

           



