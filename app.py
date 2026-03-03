import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

st.title("📈 Stock Price Prediction App")

st.info("For Indian stocks use .NS (Example: RELIANCE.NS)")

# Popular stocks dropdown
popular_stocks = {
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN"
}

selected_stock = st.selectbox("Select Popular Stock", list(popular_stocks.keys()))

# Custom input
custom_stock = st.text_input("Or Enter Custom Stock Symbol (Example: RELIANCE.NS)")

# Decide final stock symbol
if custom_stock:
    stock_symbol = custom_stock.upper()
else:
    stock_symbol = popular_stocks[selected_stock]

if st.button("Predict"):
    model = load_model("lstm_model.h5") # load model
    data = yf.download(stock_symbol,start="2015-01-01")#download data
    if data.empty:
        st.error("Invalid stock symbol. Please try again.")
    else:
        close_data = data[['Close']]

        scaler = MinMaxScaler(feature_range=(0,1)) # scaling
        scaled_data = scaler.fit_transform(close_data)

        #Get last 60 days
        last_60_days = scaled_data[-60:]
        last_60_days = last_60_days.reshape(1,60,1)

        # Predict
        next_day = model.predict(last_60_days)
        next_day_price = scaler.inverse_transform(next_day)
        st.subheader(f"Based on past 60 days, the predicted closing price for {stock_symbol} tomorrow is: ${next_day_price[0][0]:.2f}")
        #st.subheader(f"Predicted Next Day Price: ${next_day_price[0][0]:.2f}")

        #plot chart
        st.subheader("Historical Closing Price")
        plt.figure(figsize=(10,5))
        plt.plot(close_data)
        plt.xlabel("Date")
        plt.ylabel("Price")
        st.pyplot(plt)    
        
    