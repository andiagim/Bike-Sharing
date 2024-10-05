import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='ticks')

def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df['hr'].value_counts().reset_index(name='cnt')
    return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df[(day_df['dteday'] >= '2011-01-01') & (day_df['dteday'] < '2012-12-31')]
    return day_df_count_2011

def total_registered_df(day_df):
    reg_df = day_df.resample('D', on='dteday')['registered'].sum().reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

def total_casual_df(day_df):
    cas_df = day_df.resample('D', on='dteday')['casual'].sum().reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby('hr')['cnt'].sum().reset_index()
    return sum_order_items_df

def macem_season(day_df):
    season_df = day_df.groupby('season')['cnt'].sum().reset_index()
    return season_df

days_df = pd.read_csv("dashboard/main_data.csv")
hours_df = pd.read_csv("dashboard/main_data0.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
 
    st.image("dashboard/logo.jpeg")
    
        
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)


st.header('Bike Sharing Dataset :sparkles:')

cols = st.columns(3)

total_orders = day_df_count_2011.cnt.sum()
cols[0].metric("Total Sharing Bike", value=total_orders)

total_sum = reg_df.register_sum.sum()
cols[1].metric("Total Registered", value=total_sum)

total_sum = cas_df.casual_sum.sum()
cols[2].metric("Total Casual", value=total_sum)

st.subheader("Jumlah penyewaan sepeda naik turun mengikuti pergantian musim")
season_averages = days_df.groupby("season")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(season_averages['season'], season_averages['cnt'], 
       color=[plt.cm.Blues(val / season_averages['cnt'].max()) for val in season_averages['cnt']])

ax.set_ylabel("Average Rental Count")
ax.set_title("Average Bicycle Rentals Per Season")
ax.set_xticks(season_averages['season'])
fig.tight_layout()
st.pyplot(fig)

st.subheader("Pengaruh dari kondisi lingkungan sekitar terhadap kepopuleran layanan penyewaan sepeda")
average_cnt_by_weathersit = hours_df.groupby("weathersit")["cnt"].mean()

fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(x=average_cnt_by_weathersit.index, y=average_cnt_by_weathersit.values, ax=ax)
ax.set_xlabel("Weather Situation")
ax.set_ylabel("Average Bike Rentals")
ax.set_title("Relationship Between Weather Situation and Bike Rentals")
fig.tight_layout()
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(days_df["temp"], days_df["cnt"])

slope, intercept = np.polyfit(days_df["temp"], days_df["cnt"], 1)
x = np.linspace(days_df["temp"].min(), days_df["temp"].max(), 100)
y = slope * x + intercept

ax.plot(x, y, color='red')
ax.set_title("Regression Analysis based on Temperature")
ax.set_xlabel("Temperature (Celsius)")
ax.set_ylabel("Total Bikes Rented")
fig.tight_layout()
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(10, 6))

sns.regplot(data=days_df, x="atemp", y="cnt", 
            scatter_kws={'alpha':0.5}, line_kws={'color': 'red', 'label': 'Regresi Linear'}, ax=ax)

ax.set_title("Relationship between Perceived Temperature and Bike Rentals")
ax.set_xlabel("Perceived Temperature (°C)")
ax.set_ylabel("Total Bike Rentals")
fig.tight_layout()
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(10, 6))

x = days_df['hum']
y = days_df['cnt']

slope, intercept = np.polyfit(x, y, 1)

ax.scatter(x, y, label='Data')
ax.plot(x, slope*x + intercept, color='red', label='Regresi Line')
ax.set_title('Regression Analysis based on Humidity')
ax.set_xlabel('Humidity')
ax.set_ylabel('Total Bikes Rented')
ax.legend()
fig.tight_layout()
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(10, 6))

sns.regplot(data=days_df, x='windspeed', y='cnt',
            line_kws={'color': 'red', 'label': 'Regresi Linear'}, ax=ax)

ax.set_title('Relationship between Wind Speed and Bike Rentals')
ax.set_xlabel('Wind Speed (m/s)')
ax.set_ylabel('Number of Bikes Rented')
ax.legend()
fig.tight_layout()
st.pyplot(fig)

st.subheader("Perbandingan perbedaan jumlah penyewaan sepeda di hari libur dan hari biasa")

holiday_counts = days_df.groupby(by=["holiday", "yr"]).agg({"cnt": "sum"}).reset_index()
holiday_pivot = holiday_counts.pivot_table(index="yr", columns="holiday", values="cnt")

plt.figure(figsize=(10,6))
plt.plot(holiday_pivot.index, holiday_pivot[0], label='Non-Holiday', marker='o')
plt.plot(holiday_pivot.index, holiday_pivot[1], label='Holiday', marker='o')

plt.title('Perbandingan Jumlah Hari Libur dan Non-Libur')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Hari')
plt.legend()

st.pyplot(plt.gcf())
