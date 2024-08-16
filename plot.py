import plotly.graph_objs as go
import numpy as np
from datetime import datetime, timedelta

# 
with open('prices.txt', 'r') as file:
    prices = [float(line.strip()) for line in file.readlines()]

with open("dates.txt", "r") as file:
    dates = [line.strip() for line in file.readlines()]


all_dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in dates]

# Uncomment if text file contains prices from newest to oldest
# prices.reverse()

# Create an interactive line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=all_dates,
    y=prices,
    mode='lines',
    name='Price',
    line=dict(color='blue')
))

# Update layout to include range slider and selectors
fig.update_layout(
    title="Price Trend",
    xaxis_title="Date",
    yaxis_title="Price (DOGE)",
    xaxis=dict(
        rangeslider=dict(visible=True),  # Adds a range slider for the x-axis
        type="date"
    ),
    height=600,
    width=1400
)

fig.show()
