import streamlit as st
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

class Model:
    def __init__(self, 
                 CPM: float = 0.015, 
                 WebinarLength: int = 75, 
                 AverageUtilization: float = 0.5, 
                 LineType: str = 'ListenOnly',
                 TimesRevenue: float = 3.5
                 ):    
        self.CPM = CPM
        self.WebinarLength = WebinarLength
        self.AverageUtilization = AverageUtilization
        self.LineType = LineType
        self.TimesRevenue = TimesRevenue
        
        
        if LineType == 'QnA':
            self.DeliveryLabor = 152.5
        elif LineType == 'ListenOnly':
            self.DeliveryLabor = 62.5
            

    def distribution(self, NumRuns: int, Distribution: str = 'Normal'):
        if Distribution == 'Normal':
            # Generate a skewed distribution using beta distribution
            # Parameters chosen to create right skew centered around AverageUtilization
            alpha = 2 + (self.AverageUtilization * 8)  # Increases with higher utilization
            beta = 2 + ((1-self.AverageUtilization) * 8)  # Decreases with higher utilization
            self.utilization_values = np.random.beta(alpha, beta, NumRuns)
            runs = self.utilization_values
        elif Distribution == 'Uniform':
            half_width = 0.2
            low = max(0, self.AverageUtilization - half_width)
            high = min(1, self.AverageUtilization + half_width)
            self.utilization_values = np.random.uniform(low, high, NumRuns)
            runs = self.utilization_values
        else:
            raise ValueError(f"Invalid distribution: {Distribution}")
        
        self.lines25 = [(rn * 25 * self.CPM * self.WebinarLength) + self.DeliveryLabor for rn in runs]
        self.lines50 = [(rn * 50 * self.CPM * self.WebinarLength) + self.DeliveryLabor for rn in runs]
        self.lines100 = [(rn * 100 * self.CPM * self.WebinarLength) + self.DeliveryLabor for rn in runs]
        self.lines200 = [(rn * 200 * self.CPM * self.WebinarLength) + self.DeliveryLabor for rn in runs]
        self.lines300 = [(rn * 300 * self.CPM * self.WebinarLength) + self.DeliveryLabor for rn in runs]
        
        # Calculate ideal revenues first
        ideal_revenue25 = np.mean(self.lines25) * self.TimesRevenue
        ideal_revenue50 = np.mean(self.lines50) * self.TimesRevenue
        ideal_revenue100 = np.mean(self.lines100) * self.TimesRevenue
        ideal_revenue200 = np.mean(self.lines200) * self.TimesRevenue
        ideal_revenue300 = np.mean(self.lines300) * self.TimesRevenue
        
        self.gross_margins25 = [(ideal_revenue25 - self.lines25[i]) / ideal_revenue25 for i in range(len(self.lines25))]
        self.gross_margins50 = [(ideal_revenue50 - self.lines50[i]) / ideal_revenue50 for i in range(len(self.lines50))]
        self.gross_margins100 = [(ideal_revenue100 - self.lines100[i]) / ideal_revenue100 for i in range(len(self.lines100))]
        self.gross_margins200 = [(ideal_revenue200 - self.lines200[i]) / ideal_revenue200 for i in range(len(self.lines200))]
        self.gross_margins300 = [(ideal_revenue300 - self.lines300[i]) / ideal_revenue300 for i in range(len(self.lines300))]
        
        return ideal_revenue25, ideal_revenue50, ideal_revenue100, ideal_revenue200, ideal_revenue300

# Streamlit app

st.title("Audio Dial-in Simulation")

# Replace the input container with sidebar inputs
with st.sidebar:
    st.markdown("### Configuration")
    CPM = st.number_input("CPM", value=0.015)
    WebinarLength = st.number_input("Webinar Length", value=75)
    AverageUtilization = st.slider("Average Utilization", 0.0, 1.0, 0.5)
    
    st.markdown("---")  # Adds a visual separator
    
    LineType = st.selectbox("Line Type", ['QnA', 'ListenOnly'], index=0)
    NumRuns = st.number_input("Number of Simulations", value=1000, step=1)
    Distribution = st.selectbox("Distribution", ['Normal', 'Uniform'])
    TimesRevenue = st.slider("Revenue Multiplier", min_value=1.0, max_value=10.0, value=3.5, step=0.1)

model = Model(CPM, WebinarLength, AverageUtilization, LineType, TimesRevenue)
ideal_revenues = model.distribution(NumRuns, Distribution)
st.markdown("### Output")
# Add distribution plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=model.utilization_values, stat='density', kde=True, ax=ax)
ax.set_xlabel('Utilization')
ax.set_ylabel('Probability Density')
ax.set_title(f'{Distribution} Distribution of Utilization')
st.pyplot(fig)

# Add gross margins distribution plot
# Create separate plots for each line count in two columns
col1, col2 = st.columns(2)

with col1:
    # 25 Lines plot
    fig25, ax25 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=model.gross_margins25, stat='count', alpha=0.5, ax=ax25, color='#FF9999')
    ax25.set_xlabel('Gross Margin ($)')
    ax25.set_ylabel('Number of Occurrences') 
    ax25.set_title('Distribution of Gross Margins - 25 Lines')
    st.pyplot(fig25)

    # 100 Lines plot
    fig100, ax100 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=model.gross_margins100, stat='count', alpha=0.5, ax=ax100, color='#99FF99')
    ax100.set_xlabel('Gross Margin ($)')
    ax100.set_ylabel('Number of Occurrences')
    ax100.set_title('Distribution of Gross Margins - 100 Lines')
    st.pyplot(fig100)

    # 300 Lines plot
    fig300, ax300 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=model.gross_margins300, stat='count', alpha=0.5, ax=ax300, color='#FF99FF')
    ax300.set_xlabel('Gross Margin ($)')
    ax300.set_ylabel('Number of Occurrences')
    ax300.set_title('Distribution of Gross Margins - 300 Lines')
    st.pyplot(fig300)

with col2:
    # 50 Lines plot
    fig50, ax50 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=model.gross_margins50, stat='count', alpha=0.5, ax=ax50, color='#9999FF')
    ax50.set_xlabel('Gross Margin ($)')
    ax50.set_ylabel('Number of Occurrences')
    ax50.set_title('Distribution of Gross Margins - 50 Lines')
    st.pyplot(fig50)

    # 200 Lines plot
    fig200, ax200 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=model.gross_margins200, stat='count', alpha=0.5, ax=ax200, color='#FFFF99')
    ax200.set_xlabel('Gross Margin ($)')
    ax200.set_ylabel('Number of Occurrences')
    ax200.set_title('Distribution of Gross Margins - 200 Lines')
    st.pyplot(fig200)

st.markdown("### Final Output")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 20px'>
            <p style='font-size: 16px; font-weight: bold; margin-bottom: 5px'>Ideal Revenue at 3.5x (25 lines)</p>
            <p style='font-size: 24px; color: #0066cc; margin: 0'>${:,.2f}</p>
        </div>
        
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 20px'>
            <p style='font-size: 16px; font-weight: bold; margin-bottom: 5px'>Ideal Revenue at 3.5x (100 lines)</p>
            <p style='font-size: 24px; color: #0066cc; margin: 0'>${:,.2f}</p>
        </div>
        
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px'>
            <p style='font-size: 16px; font-weight: bold; margin-bottom: 5px'>Ideal Revenue at 3.5x (300 lines)</p>
            <p style='font-size: 24px; color: #0066cc; margin: 0'>${:,.2f}</p>
        </div>
    """.format(round(ideal_revenues[0], 2), round(ideal_revenues[2], 2), round(ideal_revenues[4], 2)), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 20px'>
            <p style='font-size: 16px; font-weight: bold; margin-bottom: 5px'>Ideal Revenue at 3.5x (50 lines)</p>
            <p style='font-size: 24px; color: #0066cc; margin: 0'>${:,.2f}</p>
        </div>
        
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px'>
            <p style='font-size: 16px; font-weight: bold; margin-bottom: 5px'>Ideal Revenue at 3.5x (200 lines)</p>
            <p style='font-size: 24px; color: #0066cc; margin: 0'>${:,.2f}</p>
        </div>
    """.format(round(ideal_revenues[1], 2), round(ideal_revenues[3], 2)), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Define the fixed target values
target_values = {
    'ListenOnly': {25: 250, 50: 450, 100: 800, 200: 1500, 300: 2250},
    'QnA': {25: 500, 50: 800, 100: 1300, 200: 2000, 300: 2750}
}

# Get current target values based on selected LineType
current_targets = target_values[LineType]

st.markdown("""
            
            
| Number of Lines | Model Predicted Revenue | Target Revenue | Difference |
|----------------|------------------------|----------------|------------|
| 25 lines       | ${:,.2f} | ${:,.2f} | ${:,.2f} |
| 50 lines       | ${:,.2f} | ${:,.2f} | ${:,.2f} |
| 100 lines      | ${:,.2f} | ${:,.2f} | ${:,.2f} |
| 200 lines      | ${:,.2f} | ${:,.2f} | ${:,.2f} |
| 300 lines      | ${:,.2f} | ${:,.2f} | ${:,.2f} |
""".format(
    ideal_revenues[0], current_targets[25], ideal_revenues[0] - current_targets[25],
    ideal_revenues[1], current_targets[50], ideal_revenues[1] - current_targets[50],
    ideal_revenues[2], current_targets[100], ideal_revenues[2] - current_targets[100],
    ideal_revenues[3], current_targets[200], ideal_revenues[3] - current_targets[200],
    ideal_revenues[4], current_targets[300], ideal_revenues[4] - current_targets[300]
))
