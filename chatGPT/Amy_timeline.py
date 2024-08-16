import numpy as np
import matplotlib.pyplot as plt

# Define events with dates and colors
events = [
    {"name": "Hominins Walk", "date": -7000000, "color": "brown"},
    {"name": "Modern Homo sapiens", "date": -300000, "color": "red"},
    {"name": "Homo Floresiensis", "date": -100000, "color": "black"},
    {"name": "Humans in Americas", "date": -15000, "color": "goldenrod"},
    {"name": "Dog domesticated", "date": -10000, "color": "green"},
    {"name": "Corn domesticated", "date": -9000, "color": "orange"},
    {"name": "First wheel", "date": -4000, "color": "darkblue"},
    {"name": "First pyramid", "date": -2630, "color": "blue"},
    {"name": "Great Wall", "date": -700, "color": "darkgray"},
    {"name": "Roman collapse", "date": 80, "color": "purple"},
    {"name": "Cahokia peak", "date": 1050, "color": "teal"},
]

# Sort events by date
events = sorted(events, key=lambda x: x['date'])

# Prepare dates for plotting
dates = np.array([-event['date'] if event['date'] < 0 else event['date'] for event in events])
dates[dates == 0] = 1  # Avoid zero in log scale
log_dates = np.log10(dates)

# Plot timeline
plt.figure(figsize=(20, 7))
plt.plot(log_dates, [1] * len(log_dates), color='gray', linestyle='-', linewidth=2)

# Plot events
for i, event in enumerate(events):
    plt.scatter(log_dates[i], 1, marker='o', color=event['color'], s=100)
    date_label = f"{event['name']} ({abs(event['date'])} {'BCE' if event['date'] < 0 else 'CE'})"
    plt.text(log_dates[i] - 0.05, 1 - 0.001, date_label, rotation=45, ha='left', va='bottom',
             fontsize=10, fontfamily='serif', color=event['color'])

# Customize plot
plt.yticks([])
plt.xlabel("Years From Present Day (August 15th, 2024)", fontsize=12, fontfamily='serif')
plt.title("Timeline on a Logarithmic Scale", fontsize=14)
plt.xticks(np.log10([1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]),
           ['1', '10', '100', '1,000', '10,000', '100,000', '1,000,000', '10,000,000'],
           fontsize=12, fontfamily='serif')
plt.xlim(log_dates.min() - 1.5, log_dates.max() + 1)
plt.grid(True, which="major", linestyle="--", color="lightgray")
plt.show()
