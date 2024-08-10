import matplotlib.pyplot as plt
import numpy as np

# Generate 1000 random data points between 4000 and 25000
np.random.seed(0)  # Seed for reproducibility
random_prices = np.random.randint(4000, 25001, size=1000)

# Plotting the generated data
plt.figure(figsize=(40, 6))
plt.plot(random_prices, marker='o', markersize=3, linestyle='-', linewidth=0.5, color='b')
plt.title("Sample Price Trend")
plt.xlabel("Data Points")
plt.ylabel("Price (USD)")
plt.grid(True)

# Show the plot
plt.show()
