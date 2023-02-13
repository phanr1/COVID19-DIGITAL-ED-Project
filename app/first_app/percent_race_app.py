import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="My App",
    page_icon=":shark:"
)

# Load data from ./data folder
percent_comp = pd.read_csv("./data/percent_comp.csv", parse_dates=["DATE"], index_col=[0])
school_hours = pd.read_csv("./data/percent_race.csv", index_col=[0])

small_set = percent_comp[:100]

# Page elements
st.title("Clean Pulse Data Exploration")

@st.cache()
def load_data():
    df = pd.read_csv(
        "./data/percent_race.csv", parse_dates=["DATE"], index_col=[0]
    )
    return df


# Read in the cereal data
percent_race = load_data()

st.subheader('Percent Access to Computers by Race')

labels={"RRACE": "Race"}
newnames = {"1":"White", "2": "Black", "3": "Asian", "4": "Other/Multi"}
fig = px.line(percent_race, x=percent_race.index, y="mean", color="RRACE", labels=labels)
fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )



st.plotly_chart(fig)