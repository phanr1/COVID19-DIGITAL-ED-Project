import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

# Load data from ./data foler
percent_comp = pd.read_csv("./data/percent_comp.csv")
percent_race = pd.read_csv("./data/percent_race.csv")
school_hours = pd.read_csv("./data/percent_race.csv")

# Page elements
st.title("Clean Pulse Data Exploration")

st.header("Observations and Visualizations")
st.markdown('''
            * The cleaned Pulse data includes 23 categories
            * The dates run from 2020-04-23 to 2021-06-23
            * Key features include income, race, number of children in household, 
            computer and internet availability, and parents’ education level
            * See the [data dictionary](https://docs.google.com/spreadsheets/d/1I6wM8sZd5sp630gwJvGTRz2JV_57Rgso/edit?usp=sharing&ouid=108315874599219905076&rtpof=true&sd=true)  for a full list of features
            ''')

st.subheader("Plotting Data as Time Series")

def plot_df(df, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:blue')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)

fig = plot_df(percent_comp, x=percent_comp.index, y=percent_comp["mean"], title="Percentage of Household with Computer Available More Than Rarely")

st.pyplot(fig, clear_figure=True)
st.caption("Computer availability as a percentage for all respondents over the whole survey time period. There is a clear increase in September 2020.")
