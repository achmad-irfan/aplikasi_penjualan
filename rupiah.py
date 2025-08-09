def format_rp(n):
    # Buang desimal, ubah ribuan pake titik
    return f"Rp {int(n):,}".replace(",", ".")