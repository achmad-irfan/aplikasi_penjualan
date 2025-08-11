

def format_rp(n):
    # Buang desimal, ubah ribuan pake titik
    return f"Rp {int(n):,}".replace(",", ".")

def create_qr(toko, bank, rekening):
    import qrcode
    import io
    # data
    
    # gabungkan data
    data_qr= f"{toko}\nBank: {bank}\nNoRek:{rekening}"
    
    # create QR
    qr = qrcode.QRCode(
    version=1,  # ukuran QR
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4)
    
    qr.add_data(data_qr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()  # return bytes  





