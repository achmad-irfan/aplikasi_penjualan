import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import struk
import utils

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
        
    if "pay" not in st.session_state:
        st.session_state.pay= []

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
            nama_barang = st.selectbox("Pilih Barang", [b[1] for b in barang_list])
            qty = st.number_input("Qty", min_value=1, step=1)

            submitted = st.form_submit_button("Tambah ke Keranjang")

            if submitted:
                # Cari kode, harga, diskon & stok barang
                selected_barang = next(b for b in barang_list if b[1] == nama_barang)
                kode_barang, _, harga, stok,diskon = selected_barang
                total = harga * qty
                
                for item in st.session_state.cart:
                    if item["nama_barang"]== nama_barang:
                        item["qty"] += qty
                        harga_setelah_diskon = item["harga"] * (1 - int(item["diskon"]) / 100)
                        item["total"] = harga_setelah_diskon * item["qty"]
                        break
                else:
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
                col3_.write(f"{utils.format_rp(row['total'])}")
                diskon_jumlah = float(row['diskon'])/100 * float(row['total'])
                col4_.write(f" \- {utils.format_rp(diskon_jumlah)}")
                harga_setelah_diskon = row['total'] - diskon_jumlah
                col5_.write(f"{utils.format_rp(harga_setelah_diskon)}")
                if col6_.button("🗑", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()

        else:
            st.info("Keranjang masih kosong.")

        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            df_cart['diskon'] = df_cart['diskon'].astype(float)
            df_cart['harga'] = df_cart['harga'].astype(float)

            # Hitung harga diskon (misal diskon dalam persen, 0.2 untuk 20%)
            df_cart['harga_diskon'] = df_cart['diskon']* df_cart['harga']/100
            df_cart['after_diskon'] = df_cart['total']-(df_cart['harga_diskon']*df_cart["qty"])
            harga_diskon= df_cart['harga_diskon'].sum()
            
            # Hitung grand total dari kolom after_diskon
            grand_total = df_cart['after_diskon'].sum()
            st.write(f"**Total Belanja:**  {utils.format_rp(grand_total)}")
        
            # Pilih Metode Pembayaran
            metode=st.selectbox("Metode Pembayaran", ["Cash","QRIS","Card"])
            st.session_state.pay=metode
            
            if st.session_state.pay == "Cash":
                sumber=""
                nomor_kartu=""
                aproval_edc=""
                st.subheader("Uang Tunai:")

                # Inisialisasi Uang Tunai
                if "uang_tunai" not in st.session_state:
                    st.session_state.uang_tunai = 0

                # Tombol nominal
                cols = st.columns(6)
                nominals = [2000, 5000, 10000, 20000, 50000, 100000]

                for col, nominal in zip(cols, nominals):
                    if col.button(f"{utils.format_rp(nominal)}"):
                        st.session_state.uang_tunai += nominal
                        st.rerun()  # refresh supaya number_input langsung update

                # Number input selalu muncul & bisa diedit manual
                st.session_state.uang_tunai = st.number_input(
                    "Masukkan Uang Tunai",
                    min_value=0,
                    value=st.session_state.uang_tunai,
                    step=1000
                )
                
                uang_tunai= st.session_state.uang_tunai
                #Jumlah Uang Tunai
                st.success(f"Total Uang:  {utils.format_rp(st.session_state.uang_tunai)}")
                
                # Kembalian
                kembalian = st.session_state.uang_tunai - grand_total
                if kembalian <0:
                    st.error(f"Uang kurang - {utils.format_rp(kembalian)}")
                else:
                    st.success(f"Total Kembalian:  {utils.format_rp(kembalian)}") 

        
                    
            if st.session_state.pay == "QRIS":
                uang_tunai=""
                kembalian=""
                nomor_kartu=""
                aproval_edc=""
                st.subheader("QRIS")
                st.image(utils.create_qr("Toko Amaanh","Bank BCA",2355555555))
                sumber = st.selectbox("Source",["ShopeePay","OVO","BCA","Mobile","DANA","GoPay"],index=0)
                konfirmasi= st.selectbox("Pembayaran Diterima",["Ya","Belum"], index=1)
                
                # Cek pembayaran Masuk apa belum
                if konfirmasi=="Belum":
                    st.error("Pembayaran Belum Diterima")
                    st.stop()
                else:
                    st.success("Pembayaran Diterima")
                
            if st.session_state.pay == "Card":
                sumber=""
                uang_tunai=""
                kembalian=""
                st.subheader("Card")
                nomor_kartu = st.text_input("Masukkan 4 digit terakhir kartu", max_chars=4)
                aproval_edc = st.text_input("Masukkan 4 digit EDC", max_chars=4)
                konfirmasi= st.selectbox("Transaksi diapporove",["Ya","Ditolak"], index=1)
                # Cek transaksi diapprove atau tidak
                if konfirmasi=="Ditolak":
                    st.error("Transaksi ditolak")
                    st.stop()
                else:
                    st.success("Transaksi diapprove")
                        
        if st.button("Simpan Penjualan"):
            jam_str = jam.strftime("%H:%M:%S")
            
            # Data Buyer
            cursor.execute("SELECT buyer_id FROM pembeli WHERE nama=? AND hp=?", (buyer, telp))
            result_buyer = cursor.fetchone()
            
            if result_buyer:
                buyer_id = result_buyer[0]
            else:
                cursor.execute("INSERT INTO pembeli (nama, hp) VALUES (?, ?)", (buyer, telp))
                buyer_id = cursor.lastrowid  
            
            # Data Transaksi
            cursor.execute("""
                INSERT INTO PENJUALAN (tanggal,jam, buyer_id, total_transaksi,metode_pembayaran)
                values (?,?,?,?,?)                 
                """, (tanggal,jam_str,buyer_id, grand_total, metode))
            
            cursor.execute("""
                           SELECT id from penjualan WHERE buyer_id=? 
                           and tanggal=?
                           and jam=?
                           and total_transaksi=?
                           and metode_pembayaran=?
                           """, (buyer_id,tanggal,jam_str,grand_total,metode))
            
            result_id = cursor.lastrowid
            
            
            for item in st.session_state.cart:
                cursor.execute("""
                    INSERT INTO detail_transaksi (transaksi_id, pembeli_id, pembeli_nama,
                    barang, qty, harga_satuan, diskon, total_harga )
                    VALUES (?, ?, ?, ?, ?, ?,?,?)
                """, (result_id,
                      buyer_id, 
                      buyer,
                      item["kode_barang"],
                      item["qty"], 
                      item["harga"],
                      item["diskon"],
                      item["total"]))

            cursor.execute("""
                UPDATE barang
                SET stok = stok - ?
                WHERE kode_barang = ?
            """, (item["qty"], item["kode_barang"]))

            conn.commit()
            st.success("Penjualan berhasil disimpan dan stok barang diperbarui!")
            
            # Panggil program cetak struk
            struk.cetak_struk(df_cart, grand_total, harga_diskon, st.session_state.pay,
                             uang_tunai=uang_tunai, kembalian=kembalian, sumber=sumber,
                             nomor_kartu=nomor_kartu, aproval_edc=aproval_edc)
            st.session_state.cart.clear()
            st.rerun()
           
    if st.button("Refresh"):
        st.session_state.cart.clear()
        st.rerun()























