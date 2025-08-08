import sqlite3

# Koneksi ke database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Ubah harga_satuan NULL atau kosong menjadi 0
cursor.execute("""
   CREATE TABLE BUYER(
       BUYER_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
       NAMA TEXT NOT NULL,
       HP TEXT NOT NULL
   )
""")

conn.commit()
conn.close()

print("Tabel buyer jadi")