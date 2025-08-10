from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
from datetime import datetime
import streamlit as st
import rupiah

def cetak_struk(df_cart, grand_total, uang_tunai,kembalian,nama_file="struk.pdf"):
    # Defini ukuran struk
    lebar = 80 * mm
    tinggi = 200 * mm
    buffer= BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(lebar, tinggi))
    
    y= tinggi - 15*mm
    #Judul
   
    pdf.setFont("Helvetica-Bold", 10)
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
        pdf.drawString(30*mm, y, f"{rupiah.format_rp(row['harga'])}")
        pdf.drawString(47.5*mm, y, f"{int(row['diskon'])}%")
        pdf.drawString(60*mm, y, f"{rupiah.format_rp(row['after_diskon'])}")
        y -= 5*mm
        
    # Total Harga
    y -=4*mm
    pdf.drawRightString(lebar- 10*mm,y, f"Total Harga : {rupiah.format_rp(grand_total)}")
    y -= 5*mm
    pdf.drawRightString(lebar- 10*mm,y, f"Uang Tunai : {rupiah.format_rp(uang_tunai)}")
    y -= 5*mm
    pdf.drawRightString(lebar- 10*mm,y, f"Uang Kembalian : {rupiah.format_rp(kembalian)}")
    
    
    y-=15*mm
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(lebar/2, y, "Terima kasih telah Berbelanja")
    
    
    pdf.showPage() 
    pdf.save()
    
        # 🔹 Simpan buffer ke file fisik
    with open(nama_file, "wb") as f:
        f.write(buffer.getvalue())
        
        
    print(f"✅ Struk berhasil dibuat: {nama_file}")
