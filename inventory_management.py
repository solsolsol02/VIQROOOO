import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Manajemen Inventory & PPIC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data rekayasa untuk contoh
@st.cache_data
def load_data():
    # Data produk
    products = {
        'product_id': [f'P{str(i).zfill(3)}' for i in range(1, 21)],
        'product_name': [
            'Laptop ASUS X441', 'Smartphone Samsung A32', 'Monitor LG 24"', 
            'Keyboard Mechanical', 'Mouse Wireless', 'Headphone Bluetooth',
            'Printer Epson L3210', 'Tablet iPad 9th', 'SSD 500GB', 
            'RAM 8GB DDR4', 'Power Supply 650W', 'Casing PC ATX',
            'Webcam 1080p', 'Microphone USB', 'Router Wi-Fi 6',
            'Hard Disk 1TB', 'Cooler CPU', 'VGA Card GTX 1660',
            'Motherboard B450', 'Speaker 2.1'
        ],
        'category': [
            'Elektronik', 'Elektronik', 'Elektronik', 'Aksesori', 'Aksesori',
            'Aksesori', 'Elektronik', 'Elektronik', 'Komponen', 'Komponen',
            'Komponen', 'Komponen', 'Aksesori', 'Aksesori', 'Jaringan',
            'Komponen', 'Komponen', 'Komponen', 'Komponen', 'Aksesori'
        ],
        'unit_price': [
            7500000, 3200000, 1800000, 450000, 250000, 600000, 
            2800000, 4500000, 800000, 650000, 850000, 500000,
            400000, 350000, 1200000, 900000, 350000, 3200000, 
            1800000, 550000
        ],
        'stock': [
            45, 78, 32, 120, 150, 85, 25, 40, 95, 110, 65, 42,
            88, 76, 53, 60, 92, 28, 35, 67
        ]
    }
    
    # Data penjualan
    np.random.seed(42)
    sales_data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(1000):
        product_idx = np.random.randint(0, 20)
        product_id = products['product_id'][product_idx]
        quantity = np.random.randint(1, 10)
        price = products['unit_price'][product_idx]
        total_price = quantity * price
        date = start_date + timedelta(days=np.random.randint(0, 365))
        
        sales_data.append({
            'sale_id': f'S{str(i).zfill(4)}',
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': price,
            'total_price': total_price,
            'date': date
        })
    
    # Data supplier
    suppliers = {
        'supplier_id': [f'SUP{str(i).zfill(2)}' for i in range(1, 6)],
        'supplier_name': [
            'PT Elektronik Nusantara', 'CV Tech Solution', 
            'PT Komponen Indonesia', 'UD Aksesori Komputer',
            'PT Global Technology'
        ],
        'contact': [
            '021-5567890', '021-5567891', '021-5567892',
            '021-5567893', '021-5567894'
        ]
    }
    
    # Data pembelian
    purchases = []
    for i in range(200):
        supplier_idx = np.random.randint(0, 5)
        product_idx = np.random.randint(0, 20)
        quantity = np.random.randint(10, 100)
        price = products['unit_price'][product_idx] * 0.7  # Harga beli 70% dari harga jual
        total_price = quantity * price
        date = start_date + timedelta(days=np.random.randint(0, 365))
        
        purchases.append({
            'purchase_id': f'PUR{str(i).zfill(4)}',
            'product_id': products['product_id'][product_idx],
            'supplier_id': suppliers['supplier_id'][supplier_idx],
            'quantity': quantity,
            'unit_cost': price,
            'total_cost': total_price,
            'date': date
        })
    
    return {
        'products': pd.DataFrame(products),
        'sales': pd.DataFrame(sales_data),
        'suppliers': pd.DataFrame(suppliers),
        'purchases': pd.DataFrame(purchases)
    }

# Memuat data
data = load_data()
products_df = data['products']
sales_df = data['sales']
suppliers_df = data['suppliers']
purchases_df = data['purchases']

# Judul aplikasi
st.title("📊 Sistem Manajemen Inventory & PPIC")
st.markdown("---")

# Sidebar untuk navigasi
st.sidebar.title("Menu Navigasi")
menu_options = [
    "Dashboard Utama",
    "Analisis Penjualan",
    "Manajemen Inventory",
    "Forecasting Demand",
    "Analisis Supplier",
    "Laporan Keuangan"
]
selected_menu = st.sidebar.selectbox("Pilih Menu", menu_options)

# Dashboard Utama
if selected_menu == "Dashboard Utama":
    st.header("📈 Dashboard Utama")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = sales_df['total_price'].sum()
    total_products = products_df['product_id'].nunique()
    total_inventory_value = (products_df['stock'] * products_df['unit_price']).sum()
    avg_sale = sales_df['total_price'].mean()
    
    col1.metric("Total Penjualan", f"Rp {total_sales:,.0f}")
    col2.metric("Jumlah Produk", total_products)
    col3.metric("Nilai Inventory", f"Rp {total_inventory_value:,.0f}")
    col4.metric("Rata-rata Penjualan", f"Rp {avg_sale:,.0f}")
    
    # Grafik penjualan bulanan
    st.subheader("Trend Penjualan Bulanan")
    sales_df['month'] = sales_df['date'].dt.to_period('M').astype(str)
    monthly_sales = sales_df.groupby('month')['total_price'].sum().reset_index()
    
    fig = px.line(monthly_sales, x='month', y='total_price', 
                  title='Trend Penjualan Bulanan')
    st.plotly_chart(fig, use_container_width=True)
    
    # Produk terlaris
    st.subheader("10 Produk Terlaris")
    product_sales = sales_df.groupby('product_id').agg({
        'quantity': 'sum',
        'total_price': 'sum'
    }).reset_index()
    product_sales = product_sales.merge(products_df[['product_id', 'product_name']], on='product_id')
    top_products = product_sales.nlargest(10, 'quantity')
    
    fig = px.bar(top_products, x='product_name', y='quantity', 
                 title='Jumlah Penjualan per Produk')
    st.plotly_chart(fig, use_container_width=True)

# Analisis Penjualan
elif selected_menu == "Analisis Penjualan":
    st.header("📊 Analisis Penjualan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Filter Data")
        start_date = st.date_input("Tanggal Mulai", value=datetime(2023, 1, 1))
        end_date = st.date_input("Tanggal Akhir", value=datetime(2023, 12, 31))
        
        categories = st.multiselect(
            "Pilih Kategori",
            options=products_df['category'].unique(),
            default=products_df['category'].unique()
        )
    
    # Filter data
    filtered_sales = sales_df[
        (sales_df['date'].dt.date >= start_date) & 
        (sales_df['date'].dt.date <= end_date)
    ]
    filtered_sales = filtered_sales.merge(products_df[['product_id', 'category']], on='product_id')
    filtered_sales = filtered_sales[filtered_sales['category'].isin(categories)]
    
    with col2:
        st.subheader("Statistik Penjualan")
        total_filtered_sales = filtered_sales['total_price'].sum()
        avg_filtered_sales = filtered_sales['total_price'].mean()
        total_quantity = filtered_sales['quantity'].sum()
        
        st.metric("Total Penjualan (Filter)", f"Rp {total_filtered_sales:,.0f}")
        st.metric("Rata-rata Penjualan (Filter)", f"Rp {avg_filtered_sales:,.0f}")
        st.metric("Jumlah Item Terjual", total_quantity)
    
    # Visualisasi
    st.subheader("Visualisasi Penjualan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Penjualan per kategori
        sales_by_category = filtered_sales.groupby('category')['total_price'].sum().reset_index()
        fig = px.pie(sales_by_category, values='total_price', names='category', 
                     title='Distribusi Penjualan per Kategori')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 5 produk berdasarkan pendapatan
        top_products_revenue = filtered_sales.groupby('product_id').agg({
            'total_price': 'sum',
            'quantity': 'sum'
        }).reset_index()
        top_products_revenue = top_products_revenue.merge(
            products_df[['product_id', 'product_name']], on='product_id'
        )
        top_products_revenue = top_products_revenue.nlargest(5, 'total_price')
        
        fig = px.bar(top_products_revenue, x='product_name', y='total_price',
                     title='Top 5 Produk berdasarkan Pendapatan')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabel data penjualan
    st.subheader("Data Penjualan")
    st.dataframe(filtered_sales)

# Manajemen Inventory
elif selected_menu == "Manajemen Inventory":
    st.header("📦 Manajemen Inventory")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Status Inventory")
        
        # Hitung metrics inventory
        total_items = products_df['stock'].sum()
        out_of_stock = (products_df['stock'] == 0).sum()
        low_stock = ((products_df['stock'] > 0) & (products_df['stock'] <= 10)).sum()
        
        st.metric("Total Item dalam Inventory", total_items)
        st.metric("Produk Habis", out_of_stock)
        st.metric("Produk Stok Rendah (≤10)", low_stock)
    
    with col2:
        st.subheader("Filter Inventory")
        min_stock = st.slider("Stok Minimum", 0, 100, 0)
        max_stock = st.slider("Stok Maksimum", 0, 200, 200)
        selected_categories = st.multiselect(
            "Kategori Produk",
            options=products_df['category'].unique(),
            default=products_df['category'].unique()
        )
    
    # Filter inventory
    filtered_inventory = products_df[
        (products_df['stock'] >= min_stock) & 
        (products_df['stock'] <= max_stock) &
        (products_df['category'].isin(selected_categories))
    ]
    
    # Visualisasi inventory
    st.subheader("Visualisasi Inventory")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Inventory value by category
        inventory_value = filtered_inventory.copy()
        inventory_value['value'] = inventory_value['stock'] * inventory_value['unit_price']
        value_by_category = inventory_value.groupby('category')['value'].sum().reset_index()
        
        fig = px.bar(value_by_category, x='category', y='value', 
                     title='Nilai Inventory per Kategori')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Stock distribution
        fig = px.box(filtered_inventory, x='category', y='stock', 
                     title='Distribusi Stok per Kategori')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabel inventory
    st.subheader("Data Inventory")
    st.dataframe(filtered_inventory)

# Forecasting Demand
elif selected_menu == "Forecasting Demand":
    st.header("🔮 Forecasting Demand")
    
    st.subheader("Peramalan Permintaan Produk")
    
    # Pilih produk untuk forecasting
    selected_product = st.selectbox(
        "Pilih Produk",
        options=products_df['product_name'].tolist()
    )
    
    # Dapatkan ID produk yang dipilih
    product_id = products_df[products_df['product_name'] == selected_product]['product_id'].iloc[0]
    
    # Filter data penjualan untuk produk yang dipilih
    product_sales = sales_df[sales_df['product_id'] == product_id].copy()
    product_sales['month'] = product_sales['date'].dt.to_period('M').astype(str)
    monthly_sales = product_sales.groupby('month')['quantity'].sum().reset_index()
    
    if len(monthly_sales) > 1:
        # Metode forecasting sederhana (moving average)
        st.subheader("Peramalan dengan Moving Average")
        window = st.slider("Window Size untuk Moving Average", 2, 6, 3)
        
        # Hitung moving average
        monthly_sales['forecast'] = monthly_sales['quantity'].rolling(window=window).mean().shift(1)
        
        # Visualisasi
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly_sales['month'], y=monthly_sales['quantity'],
                                mode='lines+markers', name='Aktual'))
        fig.add_trace(go.Scatter(x=monthly_sales['month'], y=monthly_sales['forecast'],
                                mode='lines+markers', name='Forecast'))
        fig.update_layout(title=f'Peramalan Permintaan untuk {selected_product}',
                         xaxis_title='Bulan',
                         yaxis_title='Jumlah Terjual')
        st.plotly_chart(fig, use_container_width=True)
        
        # Tampilkan data forecasting
        st.subheader("Data Peramalan")
        st.dataframe(monthly_sales)
        
        # Rekomendasi pembelian
        current_stock = products_df[products_df['product_id'] == product_id]['stock'].iloc[0]
        avg_sales = monthly_sales['quantity'].mean()
        recommended_order = max(0, round(avg_sales * 1.5 - current_stock))
        
        st.subheader("Rekomendasi Pembelian")
        st.info(f"""
        Untuk produk **{selected_product}**:
        - Stok saat ini: {current_stock} unit
        - Rata-rata penjualan bulanan: {round(avg_sales)} unit
        - Rekomendasi pembelian: {recommended_order} unit
        """)
    else:
        st.warning("Data penjualan tidak cukup untuk melakukan peramalan. Pilih produk lain.")

# Analisis Supplier
elif selected_menu == "Analisis Supplier":
    st.header("🏭 Analisis Supplier")
    
    # Gabungkan data pembelian dengan supplier dan produk
    purchases_analysis = purchases_df.merge(
        suppliers_df, on='supplier_id'
    ).merge(
        products_df[['product_id', 'product_name', 'category']], on='product_id'
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance Supplier")
        
        # Hitung metrics supplier
        supplier_performance = purchases_analysis.groupby('supplier_name').agg({
            'total_cost': 'sum',
            'quantity': 'sum',
            'product_id': 'nunique'
        }).reset_index()
        supplier_performance = supplier_performance.rename(columns={
            'total_cost': 'total_pembelian',
            'quantity': 'total_item',
            'product_id': 'jumlah_produk'
        })
        
        st.dataframe(supplier_performance)
    
    with col2:
        st.subheader("Visualisasi Performance Supplier")
        
        fig = px.bar(supplier_performance, x='supplier_name', y='total_pembelian',
                     title='Total Pembelian per Supplier')
        st.plotly_chart(fig, use_container_width=True)
    
    # Analisis lebih detail untuk supplier tertentu
    st.subheader("Analisis Detail per Supplier")
    selected_supplier = st.selectbox(
        "Pilih Supplier",
        options=suppliers_df['supplier_name'].tolist()
    )
    
    supplier_id = suppliers_df[suppliers_df['supplier_name'] == selected_supplier]['supplier_id'].iloc[0]
    supplier_purchases = purchases_analysis[purchases_analysis['supplier_id'] == supplier_id]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Produk yang dibeli dari supplier ini
        products_from_supplier = supplier_purchases.groupby('product_name').agg({
            'quantity': 'sum',
            'total_cost': 'sum'
        }).reset_index()
        
        fig = px.pie(products_from_supplier, values='quantity', names='product_name',
                     title=f'Distribusi Pembelian dari {selected_supplier}')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Trend pembelian dari supplier ini
        supplier_purchases['month'] = supplier_purchases['date'].dt.to_period('M').astype(str)
        monthly_purchases = supplier_purchases.groupby('month')['total_cost'].sum().reset_index()
        
        fig = px.line(monthly_purchases, x='month', y='total_cost',
                      title=f'Trend Pembelian dari {selected_supplier}')
        st.plotly_chart(fig, use_container_width=True)

# Laporan Keuangan
elif selected_menu == "Laporan Keuangan":
    st.header("💰 Laporan Keuangan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Pendapatan vs Pengeluaran")
        
        # Hitung total pendapatan dari penjualan
        total_revenue = sales_df['total_price'].sum()
        
        # Hitung total pengeluaran dari pembelian
        total_expense = purchases_df['total_cost'].sum()
        
        # Hitung profit
        profit = total_revenue - total_expense
        
        st.metric("Total Pendapatan", f"Rp {total_revenue:,.0f}")
        st.metric("Total Pengeluaran", f"Rp {total_expense:,.0f}")
        st.metric("Laba/Rugi", f"Rp {profit:,.0f}", 
                 delta=f"{((profit/total_revenue)*100 if total_revenue > 0 else 0):.2f}%")
    
    with col2:
        st.subheader("Margin per Kategori")
        
        # Hitung margin per kategori
        category_revenue = sales_df.merge(
            products_df[['product_id', 'category']], on='product_id'
        ).groupby('category')['total_price'].sum().reset_index()
        
        category_cost = purchases_df.merge(
            products_df[['product_id', 'category']], on='product_id'
        ).groupby('category')['total_cost'].sum().reset_index()
        
        category_margin = category_revenue.merge(category_cost, on='category')
        category_margin['margin'] = category_margin['total_price'] - category_margin['total_cost']
        category_margin['margin_pct'] = (category_margin['margin'] / category_margin['total_price']) * 100
        
        fig = px.bar(category_margin, x='category', y='margin_pct',
                     title='Margin per Kategori (%)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.subheader("Analisis Profitabilitas Produk")
        
        # Hitung profit per produk
        product_revenue = sales_df.groupby('product_id')['total_price'].sum().reset_index()
        product_cost = purchases_df.groupby('product_id')['total_cost'].sum().reset_index()
        
        product_profit = product_revenue.merge(product_cost, on='product_id', how='outer').fillna(0)
        product_profit['profit'] = product_profit['total_price'] - product_profit['total_cost']
        
        # Gabungkan dengan nama produk
        product_profit = product_profit.merge(
            products_df[['product_id', 'product_name']], on='product_id'
        )
        
        # Ambil 5 produk paling menguntungkan
        top_profitable = product_profit.nlargest(5, 'profit')
        
        fig = px.bar(top_profitable, x='product_name', y='profit',
                     title='5 Produk Paling Menguntungkan')
        st.plotly_chart(fig, use_container_width=True)
    
    # ROI Analysis
    st.subheader("Analisis ROI (Return on Investment)")
    
    # Hitung ROI per produk
    product_roi = product_profit.copy()
    product_roi['roi'] = (product_roi['profit'] / product_roi['total_cost']) * 100
    product_roi = product_roi[product_roi['total_cost'] > 0]  # Hindari division by zero
    
    # Ambil 5 produk dengan ROI tertinggi
    top_roi = product_roi.nlargest(5, 'roi')
    
    fig = px.bar(top_roi, x='product_name', y='roi',
                 title='5 Produk dengan ROI Tertinggi')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Sistem Manajemen Inventory & PPIC © 2023 - Departemen Manajemen, PPIC, dan Inventory</p>
    </div>
    """,
    unsafe_allow_html=True
)