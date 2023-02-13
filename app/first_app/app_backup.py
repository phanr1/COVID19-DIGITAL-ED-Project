import streamlit as st
import pandas as pd

#Load dataframe

pred_df = pd.read_csv("./data/predictions_output.csv")

#Declare values

income_slider_vals = ["0-25k", "25-35k", "35-50k", "50-75k", "75-100k", "100-150k", "150-200k", "200k-∞"]

race_dropdown_vals = ["Hispanic", "White", "Black", "Asian", "Other"]

internet_dropdown_vals = ["Never", "Rarely", "Sometimes", "Usually", "Always"]

quartiles = ["100%", "75%", "50%", "25%"]

vs_html =   ''' <p style="color:cornflowerblue; 
                font-size: 100px;">vs.</p>
            '''

target_hours_val = 4

segment_val = 0.5079 * 100 # Default based on segment: Hispanic, 50-75k, Sometimes

#Get quartile values from dataframe

def get_quartiles(df, val):
    q_values = []
    for i, v in enumerate(val):
        q_values.append(df.quantile(v))
    return q_values

q_values = get_quartiles(pred_df["predicted_probability"][pred_df["SCHLHRS"] == 4], [1, .75, .5, .25])
#Initalize botton values

if "race_val" not in st.session_state:
    st.session_state["race_val"] = "Hispanic"

if 'income_val' not in st.session_state:
    st.session_state["income_val"] = "50-75k"

if 'internet_val' not in st.session_state:
    st.session_state["internet_val"] = "Sometimes"

if 'segment_val' not in st.session_state:
    st.session_state["segment_val"] = segment_val

if 'quart_val' not in st.session_state:
    st.session_state["quart_val"] = float(q_values[0]) * 100

def seg_val_tracker(new_seg_val):
    st.session_state.segment_val = float(new_seg_val) * 100

def quartile_val_tracker(idx):
    st.session_state["quart_val"] = float(q_values[idx]) * 100

#Start Page content

#Title and introduction

st.title("The Digital Divide During COVID")

st.write('''
            Digital resources are essential for students facing school closures
            during the pandemic. This calculator illustrates how factors like race, income, 
            and internet access correlate with the likelihood that a student receives at
            least four hours of virtual, live instruction per week.
            ''')

#Top, four-column container

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Likelihood", f"{st.session_state.segment_val:.1f}%")
    st.image('./media/person_light_blue.png')

with col2:
    st.markdown(vs_html, unsafe_allow_html=True)

with col3:
    st.metric("Likelihood", f"{st.session_state.quart_val:.1f}%")
    st.image('./media/person_medium_blue.png')

with col4:
    st.write("Quartiles")
    Q1 = st.button("Q1", key="Q1", on_click=quartile_val_tracker, args=(0, ))
    Q2 = st.button("Q2", key="Q2", on_click=quartile_val_tracker, args=(1, ))
    Q3 = st.button("Q3", key="Q3", on_click=quartile_val_tracker, args=(2, ))
    Q4 = st.button("Q4", key="Q4", on_click=quartile_val_tracker, args=(3, ))


#Bottom stacked container with bottons

with st.form("segment_form"):
    st.header("Factors")
    race_val = st.selectbox("Race", race_dropdown_vals, 
                    help="select a value")
    income_val = st.select_slider("Income", 
                    options = income_slider_vals, 
                    help = "select a value",
                    value= "50-75k")
    internet_val = st.select_slider("Internet availability",
                    options = internet_dropdown_vals, 
                    help = "select a value", 
                    value="Sometimes")
    submitted = st.form_submit_button("Submit", 
                                        on_click=seg_val_tracker, #Below passes segment value from pandas df to callback function
                                        args=(pred_df[(pred_df["RACE_ETHNICITY"] == race_val) \
                                        & (pred_df["INCOME"] == income_slider_vals.index(income_val) + 1)\
                                        & (pred_df["INTRNTAVAIL"] == internet_dropdown_vals.index(internet_val) + 1)\
                                        & (pred_df["SCHLHRS"] == target_hours_val)].iloc[:,[5]].values.astype(float), 
                                    ))
