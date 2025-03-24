# Exercise 01 - Data Center Energy Analysis

This folder contains the Python code and report related to the **Data Center Energy Analysis** assignment for the **Energy Technologies** course.

## 📄 Overview
The objective of this exercise is to analyze the energy performance of a data center through various environmental conditions and evaluate the Power Usage Effectiveness (PUE) metric. The provided code calculates and visualizes critical parameters such as:

- **Outdoor Temperature**
- **Outdoor Dew Point**
- **Outdoor and Indoor Relative Humidity**
- **Indoor Temperature vs. Outdoor Dew Point**
- **Temperature Out Rack vs. Outdoor Temperature**
- **Power Usage Effectiveness (PUE)**

## 🛠️ Code Description
The Python script (`ET_DataCenter_Assign.py`) performs the following tasks:
- Imports necessary libraries (e.g., `pandas`, `matplotlib`, `numpy`).
- Reads data from the provided Excel file.
- Defines conditions for "OPEN", "STAY OPEN", or "CLOSED" system states based on temperature, dew point, and humidity limits.
- Implements a logic loop to manage transitions between these states.
- Plots various parameters with appropriate conditions and visual limits.

## 📊 Output
The code generates multiple plots to visualize:
- Outdoor Temperature conditions
- Outdoor Dew Point behavior
- Outdoor and Indoor Relative Humidity trends
- PUE (Power Usage Effectiveness)

These plots provide insights into the system's performance and conditions for optimal operation.

## 📂 Files in This Folder
- **`ET_DataCenter_Assign.py`** - Python script for data analysis and visualization
- **`DataCenterReport_AlessiGiada.pdf`** - Detailed report explaining the methodology, analysis, and results
- **`Data Center Data Personal.xlsx`** - Data file containing environmental and energy performance data

## 📋 Notes
- Ensure the data file path is correctly specified in the code.
- The logic conditions implemented for "OPEN", "STAY OPEN", and "CLOSED" states follow the specified environmental limits for safe operation.

For further details, refer to the provided report.

