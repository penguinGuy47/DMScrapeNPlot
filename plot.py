import plotly.graph_objs as go
import numpy as np

# 
with open('output.txt', 'r') as file:
    # Read all lines into a list
    prices = [float(line.strip()) for line in file.readlines()]

# Create a range of dates for the x-axis
from datetime import datetime, timedelta

start_date = datetime.today() - timedelta(days=1000)
dates = [start_date + timedelta(days=i) for i in range(1000)]

x_values = list(range(1, len(prices) + 1))

# Uncomment if text file contains prices from newest to oldest
# prices.reverse()

# Create an interactive line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
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
        type="linear"
    ),
    height=600,
    width=1400
)

fig.show()
