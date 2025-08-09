from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
from datetime import datetime
import streamlit as st
import rupiah

def cetak_struk(df_cart, total_bayar, nama_file="struk.pdf"):
    # Defini ukuran struk
    lebar = 80 * mm
    tinggi = 200 * mm
    buffer= BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(lebar, tinggi))
    
    y= tinggi - 10*mm
    #Judul
   
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(lebar/2, y, "TOKO MAKMUR SEJAHTERA")
    y -= 6*mm
    pdf.drawCentredString(lebar/2, y, "Arjosari, Kota Malang")
    y -= 7*mm
    
    # Tanggal
    pdf.setFont("Helvetica", 8)
    pdf.drawString(5*mm, y, f"Tanggal: {datetime.now().strftime('%d-%m-%Y')}")
    y -= 6*mm
    pdf.drawString(5*mm, y, f"Jam: {datetime.now().strftime('%H:%M:%S')}")
    y -= 6*mm
    
    # Garis pembatas
    pdf.line(5*mm, y, lebar-5*mm, y)
    y -= 6*mm
    
    # Item belanja
    pdf.setFont("Helvetica", 7)
    # Header tabel
    pdf.drawString(5*mm, y, "Product")
    pdf.drawString(25*mm, y, "Qty")
    pdf.drawString(30*mm, y, "Harga")
    pdf.drawString(47.5*mm, y, "Diskon")
    pdf.drawString(60*mm, y, "Subtotal")
    y -= 5*mm
    pdf.line(5*mm, y, lebar-5*mm, y)  # garis bawah header
    y -= 5*mm

    # Data dari df_cart
    for i, row in df_cart.iterrows():
        pdf.drawString(5*mm, y, str(row["nama_barang"]))
        pdf.drawString(25*mm, y, str(row["qty"]))
        pdf.drawString(30*mm, y, f"{rupiah.format_rp(row['harga_satuan'])}")
        pdf.drawString(47.5*mm, y, f"{int(row['diskon'])}%")
        pdf.drawString(60*mm, y, f"{rupiah.format_rp(row['after_diskon'])}")
        y -= 5*mm

    y-=5*mm
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(lebar/2, y, "Terima kasih telah Berbelanja")
    
    
    pdf.showPage() 
    pdf.save()
    
        # 🔹 Simpan buffer ke file fisik
    with open(nama_file, "wb") as f:
        f.write(buffer.getvalue())
        
        
    print(f"✅ Struk berhasil dibuat: {nama_file}")
