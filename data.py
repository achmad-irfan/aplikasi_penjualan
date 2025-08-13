import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import utils

def dashboard():
    # Buka database
    conn = sqlite3.connect("sales.db")
    data_db= """
                   SELECT 
                    dt.id_transaksi , 
                    pj.tanggal as Tanggal, 
                    pj.jam as jam, 
                    pj.buyer_id, 
                    pmb.nama AS nama_pembeli, 
                    dt.varian_barang, 
                    vr.nama_barang as Produk,
                    vr.kategori as Kategori,
                    vr.lokasi as Lokasi, 
                    dt.qty as Qty, 
                    dt.harga_satuan, 
                    dt.qty * dt.harga_satuan as Total,
                    dt.diskon
                    FROM detail_transaksi dt
                    LEFT JOIN penjualan pj 
                        ON dt.id_transaksi = pj.id
                    LEFT JOIN pembeli pmb 
                        ON pj.buyer_id = pmb.buyer_id
                    LEFT JOIN varian_product vr 
                        ON dt.varian_barang = vr.id_varian;
                   """
    df= pd.read_sql_query(data_db,conn)
    
    # Ambil data pengeluaran
    pengeluaran= "SELECT * FROM pengeluaran"
    data_pengeluaran=pd.read_sql(pengeluaran,conn)
    
    
    # Menu
    menu= st.selectbox("Menu",["Dashboard","Laporan Keuangan"],index=1)
    if menu=="Dashboard":
        # st.sidebar.header("📊 Filter Data")
        # start_date = st.sidebar.date_input("Dari Tanggal", df["Tanggal"].min())
        # end_date = st.sidebar.date_input("Sampai Tanggal", df["Tanggal"].max())
        # kategori_filter = st.sidebar.multiselect("Kategori Produk", df["Kategori"].unique())
        # lokasi_filter = st.sidebar.multiselect("Lokasi Pembeli", df["Lokasi"].unique())

        # # Filter data
        # df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
        # df["jam"]=pd.to_datetime(df["jam"])
        # df_filtered = df[(df["Tanggal"] >= pd.to_datetime(start_date)) & (df["Tanggal"] <= pd.to_datetime(end_date))]
        # if kategori_filter:
        #     df_filtered = df_filtered[df_filtered["Kategori"].isin(kategori_filter)]
        # if lokasi_filter:
        #     df_filtered = df_filtered[df_filtered["Lokasi"].isin(lokasi_filter)]

        # =======================
        # 3. KPI Summary
        # =======================
        st.title("📦 Dashboard Penjualan")
        
        st.subheader("📊 Filter Data")
        col1, col2= st.columns(2)
        with col1:
            start_date = st.date_input("Dari Tanggal", df["Tanggal"].min())
            end_date = st.date_input("Sampai Tanggal", df["Tanggal"].max())
        with col2:
            kategori_filter = st.multiselect("Kategori Produk", df["Kategori"].unique())
            lokasi_filter = st.multiselect("Lokasi Pembeli", df["Lokasi"].unique())

        # Filter data
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
        df["jam"]=pd.to_datetime(df["jam"])
        df_filtered = df[(df["Tanggal"] >= pd.to_datetime(start_date)) & (df["Tanggal"] <= pd.to_datetime(end_date))]
        if kategori_filter:
            df_filtered = df_filtered[df_filtered["Kategori"].isin(kategori_filter)]
        if lokasi_filter:
            df_filtered = df_filtered[df_filtered["Lokasi"].isin(lokasi_filter)]
            
            
            
        col1, col2, col3, col4 = st.columns([2,1,1,1])
        col1.metric("Total Penjualan", f"Rp {df_filtered['Total'].sum():,.0f}")
        col2.metric("Jumlah Transaksi", f"{len(df_filtered):,}")
        col3.metric("Total Unit Terjual", f"{df_filtered['Qty'].sum():,}")
        col4.metric("Rata-rata Per Transaksi", f"Rp {df_filtered['Total'].mean():,.0f}")

        col1, col2= st.columns(2)
        with col1:
            # =======================
            # 4. Chart - Tren Penjualan
            # =======================
            df_tren = df_filtered.groupby("Tanggal")["Total"].sum().reset_index()
            # fig_tren = px.line(df_tren, x="Tanggal", y="Total", markers=True, title="Tren Penjualan Harian")
            # st.plotly_chart(fig_tren, use_container_width=True)
            
            fig_tren = go.Figure()

            # Tambah trace garis
            fig_tren.add_trace(
                go.Scatter(
                    x=df_tren["Tanggal"],
                    y=df_tren["Total"],
                    mode="lines+markers",  # garis + titik
                    name="Total Penjualan",
                    line=dict(color="green", width=3),
                    marker=dict(size=8)
                )
            )

            # Atur layout
            fig_tren.update_layout(
                title="Tren Penjualan Harian",
                xaxis_title="Tanggal",
                yaxis_title="Total",
                template="plotly_dark"
            )
            
            fig_tren.add_shape(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,   # 0-1 itu full area figure termasuk judul
                line=dict(color="black", width=3)
            )
                        
            st.plotly_chart(fig_tren, use_container_width=True) 

            # =======================
            # 5. Chart - Top Produk
            # =======================
            df_top_produk = (
                df_filtered.groupby("Produk")["Qty"]
                .sum()
                .reset_index()
                .sort_values(by="Qty", ascending=False)
                .head(10)
            )

            fig_produk = go.Figure()
            fig_produk.add_trace(
                go.Bar(
                    x=df_top_produk["Produk"],
                    y=df_top_produk["Qty"],
                    text=df_top_produk["Qty"],
                    textposition="outside",
                    marker=dict(color="royalblue")
                )
            )
            fig_produk.update_layout(
                title="Top 10 Produk Terlaris",
                xaxis_title="Produk",
                yaxis_title="Jumlah Terjual",
                template="plotly_white",
                margin=dict(l=60, r=60, t=80, b=60)
            )
            # Border luar chart
            fig_produk.add_shape(
                type="rect", xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2)
            )
            st.plotly_chart(fig_produk, use_container_width=True)
            
            
            
        with col2:
            # =======================
            # 6. Distribusi Kategori
            # =======================
            df_kategori = (
                df_filtered.groupby("Kategori")["Total"]
                .sum()
                .reset_index()
            )

            fig_kategori = go.Figure()
            fig_kategori.add_trace(
                go.Pie(
                    labels=df_kategori["Kategori"],
                    values=df_kategori["Total"],
                    hole=0,  # 0 untuk pie chart penuh
                    textinfo="label+percent",
                    insidetextorientation="radial"
                )
            )
            fig_kategori.update_layout(
                title="Persentase Penjualan per Kategori",
                template="plotly_white",
                margin=dict(l=60, r=60, t=80, b=60)
            )
            fig_kategori.add_shape(
                type="rect", xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2)
            )
            st.plotly_chart(fig_kategori, use_container_width=True)

            # =======================
            # 7. Rata-Rata Transaksi per Jam
            # =======================
            df_filtered["jam"] = pd.to_datetime(df_filtered["jam"])
            df_filtered["hour"] = df_filtered["jam"].dt.hour

            df_avg_jam = (
                df_filtered.groupby("hour")["id_transaksi"]
                .count()
                .reset_index()
            )

            fig_avg_jam = go.Figure()
            fig_avg_jam.add_trace(
                go.Bar(
                    x=df_avg_jam["hour"],
                    y=df_avg_jam["id_transaksi"],
                    text=df_avg_jam["id_transaksi"],
                    textposition="outside",
                    marker=dict(color="orange")
                )
            )
            fig_avg_jam.update_layout(
                title="Rata-rata Penjualan per Jam",
                xaxis_title="Jam",
                yaxis_title="Jumlah Transaksi",
                template="plotly_white",
                margin=dict(l=60, r=60, t=80, b=60)
            )
            fig_avg_jam.add_shape(
                type="rect", xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2)
            )
            st.plotly_chart(fig_avg_jam, use_container_width=True)  
        
        # =======================
        # 8. Tabel Transaksi
        # =======================
        st.subheader("📋 Detail Transaksi")
        st.dataframe(df_filtered.sort_values(by="Tanggal", ascending=False), use_container_width=True)
    
    # Laporan Keuangan
    if menu=="Laporan Keuangan":
        # Pilih Bulan
        bulan= st.selectbox("Pilih Bulan",["May","June","July"])
        
        # Ambil data pengeluaran
        data_pengeluaran["tanggal"]=pd.to_datetime(data_pengeluaran["tanggal"],errors='coerce')
        data_pengeluaran_filterd= data_pengeluaran[data_pengeluaran['tanggal'].dt.month_name()==bulan]
        
        # Ambil data penjualan
        df["Tanggal"]=pd.to_datetime(df["Tanggal"],errors='coerce')
        df_filterd= df[df['Tanggal'].dt.month_name()==bulan]
        
        # Laporan
        col1, col2 = st.columns(2)
        total_penjualan = df_filterd['Total'].sum()
        total_pengeluaran = data_pengeluaran_filterd['nominal'].sum()
        neraca = total_penjualan - total_pengeluaran

        # Tampilkan metric
        col1.metric("Total Penjualan", utils.format_rp(total_penjualan))
        col2.metric("Total Pengeluaran", utils.format_rp(total_pengeluaran))
        st.metric("Neraca Keuangan", utils.format_rp(neraca))
        