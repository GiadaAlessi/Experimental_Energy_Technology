import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def check_loop(row):
    cond1 = 7 < row['temperature out (ºC)'] < 40
    cond2 = -3 < row['Dew point out (ºC)'] < 22
    cond3 = 15 < row['relative humidty out (%)'] < 80
    cond4 = -3 < row['Dew point in (ºC)'] < 22
    cond5 = 15 < row['relative humidty In (%)'] < 80
    cond6 = row['temperature in (ºC)'] > row['Dew point out (ºC)']
    cond7 = row['temp. Out Rack (ºC)'] > row['temperature out (ºC)']

    if cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7:
        return 'STAY OPEN'
    elif cond1 and cond2 and cond3 and cond4 and cond5 and cond6:
        return 'OPEN'
    else:
        return 'CLOSED'

# Load Excel file
excel_file = r"C:\Users\giada\Desktop\ET\Data Center Assignment\Data Center Data Personal.xlsx"
df = pd.read_excel(excel_file)

# Calculate PUE
df['Total Facility Energy (kW)'] = df['L1 (kW)'] + df['L2 (kW)'] + df['L3 (kW)'] + df['Fan1 (kW)'] + df['Fan2 (kW)'] + df['Fan3 (kW)'] + df['Cluster (kW)']
df['PUE'] = df['Total Facility Energy (kW)'] / df['Cluster (kW)']

# Initialize plotting variables
Time_plot = np.arange(0, len(df) * 0.0912, 0.0912)
condition = []
if check_loop(df.iloc[0]) == 'STAY OPEN':
    condition.append("OPEN")
elif check_loop(df.iloc[0]) == 'OPEN':
    condition.append("OPEN")
else:
    condition.append("CLOSED")

# Logic loop for state transitions
count_time_closed = count_open = count_closed = 0
Time = 5
for i in range(1, len(df)):
    row = df.iloc[i]
    t_step = 5
    Time += t_step
    if 1 <= count_time_closed <= 60:
        condition.append("CLOSED")
        count_closed += 1
        count_time_closed = count_closed * t_step
        count_open = 0
    elif check_loop(row) == 'CLOSED' and condition[i-1] == 'CLOSED':
        condition.append("CLOSED")
        if count_time_closed == 0:
            count_time_closed = 1
            count_open = 0
    elif check_loop(row) == 'CLOSED' and condition[i-1] == 'OPEN':
        condition.append("OPEN")
        count_time_closed = 0
        count_open = 0
    elif check_loop(row) == 'OPEN' and condition[i-1] == 'CLOSED':
        count_time_closed = 0
        condition.append("OPEN" if count_open != 0 else "CLOSED")
        if count_open == 0:
            count_time_closed = 1
        count_open += 1
    elif check_loop(row) == 'OPEN' and check_loop(df.iloc[i-1]) == 'STAY OPEN':
        count_time_closed = 0
        count_open = 0
        condition.append("CLOSED")
    elif check_loop(row) == 'OPEN' and condition[i-1] == 'OPEN':
        count_time_closed = 0
        count_open += 1
        condition.append("OPEN")
        if t_step * count_open > 10:
            count_open = 0
            condition.append("CLOSED")
    elif check_loop(row) == 'STAY OPEN' and check_loop(df.iloc[i-1]) == 'STAY OPEN':
        count_time_closed = 0
        count_open = 0
        condition.append("OPEN")
    elif check_loop(row) == 'STAY OPEN' and condition[i-1] == 'CLOSED':
        count_time_closed = 0
        count_open = 0
        condition.append("CLOSED")
    elif check_loop(row) == 'STAY OPEN' and condition[i-1] == 'OPEN':
        count_time_closed = 0
        count_open = 0
        condition.append("OPEN")

# 1. Plot Outdoor Temperature with Limits
plt.figure(figsize=(12, 6))

# Plot outdoor temperature segments with correct line styles
for i in range(1, len(Time_plot)):
    if condition[i] == "OPEN":
        plt.plot(Time_plot[i-1:i+1], df['temperature out (ºC)'][i-1:i+1], color='blue', linestyle='-')
    else:
        plt.plot(Time_plot[i-1:i+1], df['temperature out (ºC)'][i-1:i+1], color='blue', linestyle=':')

# Plot limits as a single line to ensure they are continuous and not broken up
plt.plot(Time_plot, [7] * len(Time_plot), color='black', linestyle='--', label='Temp. Min Limit')
plt.plot(Time_plot, [40] * len(Time_plot), color='red', linestyle='--', label='Temp. Max Limit')

plt.xlabel('Time (hours)')
plt.ylabel('Temperature (ºC)')
plt.title('Condition 1 - Outdoor Temperature')
plt.legend()
plt.grid(True)
plt.show()

# 2. Outdoor Dew Temperature with Limits
plt.figure(figsize=(12, 6))

# Plot outdoor dew temperature segments with correct line styles
for i in range(1, len(Time_plot)):
    if condition[i] == "OPEN":
        plt.plot(Time_plot[i-1:i+1], df['Dew point out (ºC)'][i-1:i+1], color='orange', linestyle='-')
    else:
        plt.plot(Time_plot[i-1:i+1], df['Dew point out (ºC)'][i-1:i+1], color='orange', linestyle=':')

plt.plot(Time_plot, [-3] * len(Time_plot), color='black', linestyle='--', label='Dew Temp. Min Limit')
plt.plot(Time_plot, [22] * len(Time_plot), color='red', linestyle='--', label='Dew Temp. Max Limit')

plt.xlabel('Time (hours)')
plt.ylabel('Dew Point Temperature (ºC)')
plt.title('Condition 2 - Outdoor Dew Temperature')
plt.legend()
plt.grid(True)
plt.show()

# 3. Outdoor Relative Humidity with Limits
plt.figure(figsize=(12, 6))

for i in range(1, len(Time_plot)):
    if condition[i] == "OPEN":
        plt.plot(Time_plot[i-1:i+1], df['relative humidty out (%)'][i-1:i+1], color='purple', linestyle='-')
    else:
        plt.plot(Time_plot[i-1:i+1], df['relative humidty out (%)'][i-1:i+1], color='purple', linestyle=':')

plt.plot(Time_plot, [15] * len(Time_plot), color='black', linestyle='--', label='Humidity Min Limit')
plt.plot(Time_plot, [80] * len(Time_plot), color='red', linestyle='--', label='Humidity Max Limit')

plt.xlabel('Time (hours)')
plt.ylabel('Relative Humidity (%)')
plt.title('Condition 3 - Outdoor Relative Humidity')
plt.legend()
plt.grid(True)
plt.show()

# 4. Indoor Dew Temperature with Limits
plt.figure(figsize=(12, 6))

for i in range(1, len(Time_plot)):
    if condition[i] == "OPEN":
        plt.plot(Time_plot[i-1:i+1], df['Dew point in (ºC)'][i-1:i+1], color='green', linestyle='-')
    else:
        plt.plot(Time_plot[i-1:i+1], df['Dew point in (ºC)'][i-1:i+1], color='green', linestyle=':')

plt.plot(Time_plot, [-3] * len(Time_plot), color='black', linestyle='--', label='Dew Temp. Min Limit')
plt.plot(Time_plot, [22] * len(Time_plot), color='red', linestyle='--', label='Dew Temp. Max Limit')

plt.xlabel('Time (hours)')
plt.ylabel('Dew Point Temperature (ºC)')
plt.title('Condition 4 - Indoor Dew Temperature')
plt.legend()
plt.grid(True)
plt.show()

# 5. Indoor Relative Humidity with Limits
plt.figure(figsize=(12, 6))

for i in range(1, len(Time_plot)):
    if condition[i] == "OPEN":
        plt.plot(Time_plot[i-1:i+1], df['relative humidty In (%)'][i-1:i+1], color='red', linestyle='-')
    else:
        plt.plot(Time_plot[i-1:i+1], df['relative humidty In (%)'][i-1:i+1], color='red', linestyle=':')

plt.plot(Time_plot, [15] * len(Time_plot), color='black', linestyle='--', label='Humidity Min Limit')
plt.plot(Time_plot, [80] * len(Time_plot), color='red', linestyle='--', label='Humidity Max Limit')

plt.xlabel('Time (hours)')
plt.ylabel('Relative Humidity (%)')
plt.title('Condition 5 - Indoor Relative Humidity')
plt.legend()
plt.grid(True)
plt.show()

# 6. Plot PUE
plt.figure(figsize=(12, 6))

# Plot PUE as a single continuous line
plt.plot(Time_plot, df['PUE'], color='magenta', label='PUE', linewidth=2)

plt.xlabel('Time (hours)')
plt.ylabel('PUE')
plt.title('Power Usage Effectiveness (PUE) Over Time')
plt.legend()
plt.grid(True)
plt.show()

# 7. Indoor Temperature vs. Outdoor Dew Temperature
plt.figure(figsize=(12, 6))

# Plot segments for indoor and outdoor dew temperature with conditions
for i in range(1, len(Time_plot)):
    if condition[i] == "OPEN":
        plt.plot(Time_plot[i-1:i+1], df['temperature in (ºC)'][i-1:i+1], color='blue', linestyle='-')
        plt.plot(Time_plot[i-1:i+1], df['Dew point out (ºC)'][i-1:i+1], color='orange', linestyle='-')
    else:
        plt.plot(Time_plot[i-1:i+1], df['temperature in (ºC)'][i-1:i+1], color='blue', linestyle=':')
        plt.plot(Time_plot[i-1:i+1], df['Dew point out (ºC)'][i-1:i+1], color='orange', linestyle=':')

plt.xlabel('Time (hours)')
plt.ylabel('Temperature (ºC)')
plt.title('Condition 6 - Indoor Temperature > Outdoor Dew Temperature')
plt.legend(['Indoor Temperature', 'Outdoor Dew Temperature'])
plt.grid(True)
plt.show()

# 8. Temperature Out Rack vs. Outdoor Temperature
plt.figure(figsize=(12, 6))

# Plot segments for temperature out rack vs. outdoor temperature with conditions
for i in range(1, len(Time_plot)):
    if condition[i] == "OPEN":
        plt.plot(Time_plot[i-1:i+1], df['temp. Out Rack (ºC)'][i-1:i+1], color='red', linestyle='-')
        plt.plot(Time_plot[i-1:i+1], df['temperature out (ºC)'][i-1:i+1], color='blue', linestyle='-')
    else:
        plt.plot(Time_plot[i-1:i+1], df['temp. Out Rack (ºC)'][i-1:i+1], color='red', linestyle=':')
        plt.plot(Time_plot[i-1:i+1], df['temperature out (ºC)'][i-1:i+1], color='blue', linestyle=':')

plt.xlabel('Time (hours)')
plt.ylabel('Temperature (ºC)')
plt.title('Condition 7 - Temperature Out Rack > Outdoor Temperature')
plt.legend(['Temperature Out Rack', 'Outdoor Temperature'])
plt.grid(True)
plt.show()
