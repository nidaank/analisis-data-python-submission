import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
sns.set(style='dark')

# Function
def create_weekday_bike_df(df):
    #Mengelompokkan tren penyewaan sepeda berdasarkan hari dalam seminggu
    weekday_bike_df = df.groupby(by="weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).sort_values(by="cnt", ascending=False).copy()

    # Mapping dari angka hari ke nama hari
    weekday_labels = {
        0: "Sunday", 1: "Monday", 2: "Tuesday", 
        3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"
    }

    # Menambahkan kolom nama hari
    weekday_bike_df["weekday_name"] = weekday_bike_df.index.map(weekday_labels)

    return weekday_bike_df

def create_hourly_bike_rentals_df(df):
    #Mengelompokkan data penyewaan sepeda berdasarkan jam dan hari kerja.
    hourly_bike_rentals_df = df.groupby(["hr", "workingday"]).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    return hourly_bike_rentals_df

def create_season_bike_df(df):
    # Mengelompokkan jumlah penyewaan sepeda berdasarkan musim
    season_bike_df = df.groupby(by="season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).sort_values(by="cnt", ascending=False).copy()

    # Mapping dari angka musim ke nama musim
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

    # Menambahkan kolom nama musim
    season_bike_df["season_name"] = season_bike_df.index.map(season_labels)

    return season_bike_df

def create_hourly_bike_clusters(df, n_clusters=3):
    # Mengelompokkan data berdasarkan jam
    hourly_bike_df = df.groupby(["hr"]).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()

    # Menggunakan fitur jam dan jumlah penyewaan untuk clustering
    features = hourly_bike_df[["hr", "cnt"]]

    # Normalisasi data agar skala seragam
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Menerapkan K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    hourly_bike_df["cluster"] = kmeans.fit_predict(features_scaled)

    return hourly_bike_df, kmeans

# Load data
main_data = pd.read_csv("dashboard/main_data.csv")

# Konversi kolom datetime dan urutkan berdasarkan tanggal
datetime_columns = ["dteday"]
main_data.sort_values(by="dteday", inplace=True)
main_data.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    main_data[column] = pd.to_datetime(main_data[column])

# Menentukan tanggal minimum dan maksimum
min_date = main_data["dteday"].min()
max_date = main_data["dteday"].max()

# Menentukan jam minimum dan maksimum
min_hour = 0
max_hour = 23

# Sidebar untuk filter
with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/22091590?s=200&v=4")
    
    # Filter Rentang Waktu (Tanggal)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Filter Rentang Waktu (Jam)
    start_hour, end_hour = st.slider(
        label="Rentang Jam",
        min_value=min_hour,
        max_value=max_hour,
        value=(min_hour, max_hour),
        step=1
    )

# Filter DataFrame berdasarkan rentang tanggal dan jam
main_df = main_data[
    (main_data["dteday"] >= pd.to_datetime(str(start_date))) & 
    (main_data["dteday"] <= pd.to_datetime(str(end_date))) &
    (main_data["hr"] >= start_hour) & 
    (main_data["hr"] <= end_hour)
]

# Menampilkan hasil filter
#st.write("Data yang telah difilter:")
#st.dataframe(main_df)

# Menyiapkan berbagai dataframe
weekday_bike_df = create_weekday_bike_df(main_df)
hourly_bike_rentals_df = create_hourly_bike_rentals_df(main_df)
season_bike_df = create_season_bike_df(main_df)
hourly_bike_df = create_hourly_bike_clusters(main_df, n_clusters=3)[0]  # Ambil DataFrame

#visualisasi
# Header dan subheader
st.header("Dashboard Penyewaan Sepeda 🚴‍♂️")
st.subheader("Tren Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")

# Tampilkan metrik
col1, col2 = st.columns(2)

with col1:
    total_rentals = weekday_bike_df["cnt"].sum()
    st.metric("Total Penyewaan", value=total_rentals)

with col2:
    most_popular_day = weekday_bike_df["weekday_name"].iloc[0]
    st.metric("Hari dengan Penyewaan Terbanyak", value=most_popular_day)

# Membuat plot
fig, ax = plt.subplots(figsize=(12, 6))

# Warna untuk highlight hari dengan penyewaan tertinggi
colors = ["#D3D3D3"] * 7  # Semua abu-abu
max_index = weekday_bike_df["cnt"].idxmax()  # Cari hari dengan penyewaan tertinggi
max_position = list(weekday_bike_df.index).index(max_index)
colors[max_position] = "#72BCD4"  # Highlight hari tertinggi

# Plot bar chart
sns.barplot(x="weekday_name", y="cnt", data=weekday_bike_df, ax=ax, palette=colors)

# Label dan judul
ax.set_xlabel(None)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Hari", fontsize=15)
ax.set_xticklabels(weekday_bike_df["weekday_name"], rotation=45)

# Tampilkan chart di Streamlit
st.pyplot(fig)

# Subheader 2
st.subheader("Perbedaan pola penyewaan sepeda antara hari kerja dan akhir pekan")

# Membuat plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plot data untuk hari kerja
sns.lineplot(
    data=hourly_bike_rentals_df[hourly_bike_rentals_df["workingday"] == 1]
        .groupby("hr")["cnt"].mean().reset_index(),
    x="hr", y="cnt",
    label="Hari Kerja", marker="o", linestyle="-"
)

# Plot data untuk akhir pekan
sns.lineplot(
    data=hourly_bike_rentals_df[hourly_bike_rentals_df["workingday"] == 0]
        .groupby("hr")["cnt"].mean().reset_index(),
    x="hr", y="cnt",
    label="Akhir Pekan", marker="o", linestyle="-"
)

# Judul dan label
plt.title("Perbedaan Pola Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan", fontsize=14)
plt.xlabel("Jam dalam Sehari", fontsize=12)
plt.ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
plt.xticks(range(0, 24))  # Set sumbu X dengan angka jam 0-23
plt.legend()
plt.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(fig)

#Subheader 3
st.subheader("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")

# Menampilkan total penyewaan sepeda
total_rentals = season_bike_df["cnt"].sum()
most_rented_season = season_bike_df["season_name"].iloc[0]

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Penyewaan", value=total_rentals)
with col2:
    st.metric("Musim dengan Penyewaan Tertinggi", value=most_rented_season)

# Plot bar chart
fig, ax = plt.subplots(figsize=(10, 5))

# Warna untuk highlight musim dengan penyewaan tertinggi
colors = ["#D3D3D3"] * 4  # Default semua abu-abu
max_index = season_bike_df["cnt"].idxmax()  # Cari musim dengan penyewaan tertinggi
max_position = season_bike_df.index.get_loc(max_index)  # Dapatkan posisinya
colors[max_position] = "#72BCD4"  # Highlight musim dengan penyewaan tertinggi

ax = sns.barplot(
    x="cnt", 
    y="season_name",  
    data=season_bike_df,
    palette=colors
)

# Menambahkan judul dan label
ax.set_title("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda", fontsize=15)
ax.set_xlabel("Jumlah Penyewaan Sepeda", fontsize=12)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=12)

st.pyplot(fig)

# Subheader 4
st.subheader("Clustering Penyewaan Sepeda Berdasarkan Jam")

# Menampilkan informasi cluster
total_clusters = len(hourly_bike_df["cluster"].unique())

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Cluster", value=total_clusters)
with col2:
    peak_hour = hourly_bike_df.loc[hourly_bike_df["cnt"].idxmax(), "hr"]
    st.metric("Jam Puncak Penyewaan", value=f"{peak_hour}:00")

# Visualisasi hasil clustering
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(
    data=hourly_bike_df, 
    x="hr", 
    y="cnt", 
    hue="cluster", 
    palette="viridis", 
    s=100
)

# Menambahkan judul dan label
ax.set_title("Clustering Penyewaan Sepeda Berdasarkan Jam", fontsize=15)
ax.set_xlabel("Jam dalam Sehari", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
ax.set_xticks(range(0, 24))
ax.legend(title="Cluster")
ax.grid(True)

st.pyplot(fig)

# Menambahkan Footnote
st.caption("All rights reserved. Developed by Nida'an Khafiyya")