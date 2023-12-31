import streamlit as st
from pers_teslim import LongShortTrader, Client
import pandas as pd

st.title('Crypto Trading Bot')

api_key = st.sidebar.text_input("bd494f60c4ed0287c4173e1e11f5b142a615e117e882ebebd901be7d38923a1d", value='', type='password')
api_secret = st.sidebar.text_input("d613bba14cdedbae1df707e97b0a6046ec63a1924dbf9452c3dc4fc749014776", value='', type='password')

# Create a Binance client
client = Client(api_key, api_secret, testnet=True)

# Get account information
account_info = client.get_account()

# Initialize the trader
symbol = "BTCUSDT"
interval = "1m"
units = 0.001
trader = LongShortTrader(client, symbol, interval, units)

# Get the most recent data
trader.get_most_recent(days=1/24)

# Define the strategy
trader.define_strategy(sma_s=15, sma_m=50, sma_l=200)

# Display a line chart of the closing prices
st.line_chart(trader.data['Close'])

# Display SMA windows
st.sidebar.text("SMA Short: " + str(trader.sma_s))
st.sidebar.text("SMA Medium: " + str(trader.sma_m))
st.sidebar.text("SMA Long: " + str(trader.sma_l))

# Display Binance Test Net account info
st.subheader('Binance Test Net Account Info')
st.dataframe(pd.DataFrame.from_dict(account_info))

# Display BTC/USD price info
btc_price_info = client.get_symbol_ticker(symbol=symbol)
st.subheader('BTC/USD Price Info')
st.dataframe(pd.DataFrame.from_dict([btc_price_info]))

# Display buy and sell signals
buys, sells = trader.get_signals()
buys_df = pd.DataFrame(buys, columns=['Date', 'Price'])
sells_df = pd.DataFrame(sells, columns=['Date', 'Price'])
st.subheader('Buy signals')
st.dataframe(buys_df)
st.subheader('Sell signals')
st.dataframe(sells_df)

# Calculate and display performance metrics
trader.evaluate_performance(buys, sells)
st.subheader('Performance Metrics')
st.dataframe(trader.performance_metrics)
