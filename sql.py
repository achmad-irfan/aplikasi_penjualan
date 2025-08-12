import sqlite3
import random
from datetime import datetime, timedelta

# Koneksi ke database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Hapus data lama
cursor.execute("DELETE FROM detail_transaksi")
cursor.execute("DELETE FROM penjualan")
conn.commit()

# Ambil data pembeli & produk dari database
cursor.execute("SELECT buyer_id FROM pembeli")
pembeli_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_varian, harga_satuan FROM varian_product")
produk_data = cursor.fetchall()

if not pembeli_ids or not produk_data:
    raise ValueError("Tabel pembeli atau varian_product kosong!")

# Fungsi buat tanggal acak
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days),
                              seconds=random.randint(0, 86400))

start_date = datetime(2025, 5, 1)
end_date = datetime(2025, 7, 31)

penjualan_sql = []
detail_sql = []

penjualan_id = 1
detail_id = 1

for _ in range(2000):  # 2000 transaksi
    id_pembeli = random.choice(pembeli_ids)
    tgl = random_date(start_date, end_date)
    jam_transaksi = tgl.strftime("%H:%M:%S") 
    metode_bayar = random.choice(["Cash", "Debit", "QRIS", "E-Wallet"])

    # Setiap transaksi punya 1-5 item
    total_harga = 0
    items = random.randint(1, 5)
    id_produk_terpakai = []

    for _ in range(items):
        id_varian, harga = random.choice(produk_data)
        if id_varian in id_produk_terpakai:  # supaya tidak dobel produk
            continue
        qty = random.randint(1, 5)
        total_harga += harga * qty
        id_produk_terpakai.append(id_varian)

        detail_sql.append((
            detail_id,
            penjualan_id,
            id_varian,
            qty,
            harga
        ))
        detail_id += 1

    penjualan_sql.append((
        penjualan_id,
        id_pembeli,
        tgl.strftime("%Y-%m-%d"),
        jam_transaksi,
        total_harga,
        metode_bayar
    ))

    penjualan_id += 1

# Masukkan ke tabel penjualan
cursor.executemany("""
    INSERT INTO penjualan (id, buyer_id, tanggal, jam, total_transaksi, metode_pembayaran)
    VALUES (?, ?, ?, ?, ?,?)
""", penjualan_sql)

# Masukkan ke tabel detail_transaksi
cursor.executemany("""
    INSERT INTO detail_transaksi (transaksi_id, pembeli_id, varian_barang, qty, harga_satuan)
    VALUES (?, ?, ?, ?, ?)
""", detail_sql)

conn.commit()
conn.close()

print("✅ Dummy data berhasil dimasukkan ke sales.db")
