import sqlite3
import random
from datetime import datetime, timedelta

# Koneksi ke database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Ambil data buyer
cursor.execute("SELECT buyer_id, nama FROM pembeli")
buyers = cursor.fetchall()

# Ambil data varian_product (yang ada stok > 0)
cursor.execute("""
SELECT id_varian, id_barang, nama_barang, varian, harga_satuan, diskon, stok 
FROM varian_product WHERE stok > 0
""")
varian_list = cursor.fetchall()

def random_date(start, end):
    """Generate random datetime between start and end"""
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

start_date = datetime.now() - timedelta(days=180)  # 6 bulan lalu
end_date = datetime.now()

transaksi_count = 100

for i in range(transaksi_count):
    # Pilih buyer acak
    buyer = random.choice(buyers)
    pembeli_id = buyer[0]
    buyer_nama = buyer[1]
    
    # Tanggal transaksi random di 6 bulan terakhir
    tanggal_transaksi = random_date(start_date, end_date).strftime("%Y-%m-%d")
    
    # Insert transaksi
    cursor.execute("INSERT INTO detail_transaksi (pembeli_id) VALUES (?)", (pembeli_id))
    transaksi_id = cursor.lastrowid
    
    # Pilih jumlah barang yang dibeli dalam transaksi ini (1 sampai 5 jenis barang)
    barang_beli_count = random.randint(1, 5)
    
    total_transaksi = 0
    
    for _ in range(barang_beli_count):
        varian = random.choice(varian_list)
        id_varian = varian[0]
        id_barang = varian[1]
        nama_barang = varian[2]
        varian_nama = varian[3]
        harga_satuan = varian[4]
        diskon = varian[5]
        stok = varian[6]
        
        # Jumlah beli, maksimal stok yang ada
        qty = random.randint(1, min(10, stok))
        
        # Hitung total harga per item setelah diskon
        harga_diskon = harga_satuan * (100 - diskon) / 100
        total_harga = int(qty * harga_diskon)
        
        total_transaksi += total_harga
        
        # Insert ke detail_transaksi
        cursor.execute("""
        INSERT INTO detail_transaksi (
            transaksi_id, pembeli_id, pembeli_nama, barang, qty, harga_satuan, diskon, total_harga, 
            varian_barangjam, pembeli_id, total_transaksi, metode_pembayaran
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transaksi_id, pembeli_id, buyer_nama, nama_barang, qty, harga_satuan, diskon, total_harga,
            varian_nama, pembeli_id, 0, random.choice(['Tunai', 'Debit', 'E-Wallet'])
        ))
        
        # Update stok di varian_product
        new_stok = stok - qty
        cursor.execute("UPDATE varian_product SET stok = ? WHERE id_varian = ?", (new_stok, id_varian))
    
    # Update total_transaksi di semua detail transaksi yg terkait transaksi ini
    cursor.execute("UPDATE detail_transaksi SET total_transaksi = ? WHERE transaksi_id = ?", (total_transaksi, transaksi_id))

conn.commit()
conn.close()

print("Generate 100 transaksi dan detail_transaksi selesai!")
