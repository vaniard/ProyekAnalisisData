import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

file_path = "all_df(1).csv"
df = pd.read_csv(file_path, parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])

st.title("E-commerce Data Dashboard")
st.markdown('<div style="text-align:justify">Brazilian E-commerce Public Dataset by Olist📊.</div>', unsafe_allow_html=True)

st.subheader("Jumlah Pesanan per Status")
status_counts = df["order_status"].value_counts()
fig, ax = plt.subplots()
status_counts.plot(kind="bar", ax=ax, color='skyblue')
ax.set_xlabel("Status Pesanan")
ax.set_ylabel("Jumlah Pesanan")
st. pyplot(fig)

st.subheader("Distribusi Pesanan berdasarkan Skor Ulasan")
fig, ax = plt.subplots()
sns.countplot(x=df["review_score"].dropna(), ax=ax, palette="Blues")
ax.set_xlabel("Skor Ulasan")
ax.set_ylabel("Jumlah Ulasan")
st.pyplot(fig)

st.subheader("Rata-rata Waktu Pengiriman")
df["delivery_time"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
fig, ax = plt.subplots()
sns.histplot(df['delivery_time'].dropna(), bins=20, kde=True, ax=ax, color='orange')
ax.set_xlabel("Hari Pengiriman")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

st.subheader("Penjualan berdasarkan Kategori Produk")
kategori_penjualan = df.groupby("product_category_name_english")["price"].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
kategori_penjualan.plot(kind="bar", ax=ax, color='lightcoral')
ax.set_xlabel("Produk Kategori")
ax.set_ylabel("Total Penjualan")
st.pyplot(fig)

st.subheader("Metode Pembayaran Pelanggan")
payment_counts = df["payment_type"].value_counts()
fig, ax = plt.subplots()
payment_counts.plot(kind="pie", autopct='%1.1f%%', ax=ax, colors=['lightblue', 'lightgreen', 'lightcoral', 'lightyellow'])
ax.set_ylabel("")
st.pyplot(fig)

st.subheader("RFM Analisis")
import datetime as dt 

snapshot_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
rfm_df = df.groupby("customer_unique_id").agg({
	"order_purchase_timestamp" : lambda x: (snapshot_date - x.max()).days,
	"order_id" : "count",
	"payment_value" : "sum"
	}).rename(columns={
	"order_purchase_timestamp" : "Recency",
	"order_id" : "Frequency",
	"payment_value" : "Monetary"
	})

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.histplot(rfm_df["Recency"], bins=20, kde=True, ax=axes[0], color='skyblue')
axes[0].set_title("Distribusi Recency")
sns.histplot(rfm_df["Frequency"], bins=20, kde=True, ax=axes[1], color='lightgreen')
axes[1].set_title("Distribusi Frequency")
sns.histplot(rfm_df["Monetary"], bins=20, kde=True, ax=axes[2], color='lightcoral')
axes[2].set_title("Distribusi Monetary")
st.pyplot(fig)

st.subheader("Produk yang Paling Banyak dan Paling Sedikit Dibeli Pelanggan")
produk_penjualan = df.groupby("product_category_name_english")["order_id"].count().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
produk_penjualan.head(5).plot(kind="bar", ax=ax, color='blue', label="Terbanyak")
produk_penjualan.tail(5).plot(kind="bar", ax=ax, color='skyblue' , label="Tersedikit")
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Jumlah Penjualan")
ax.legend()
st.pyplot(fig)

st.subheader("Top 5 Most Purchased Products")
st.dataframe(produk_penjualan.head(5).reset_index().rename(columns={"product_category_name_english": "Product Category", "order_id": "Total Purchases"}))

st.subheader("Top 5 Least Purchased Products")
st.dataframe(produk_penjualan.tail(5).reset_index().rename(columns={"product_category_name_english": "Product Category", "order_id": "Total Purchases"}))