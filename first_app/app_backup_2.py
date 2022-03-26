import streamlit as st
import pandas as pd

#Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

#Load dataframe

pred_df = pd.read_csv("./data/predictions_output.csv")

#Declare values

income_slider_vals = ["0-25k", "25-35k", "35-50k", "50-75k", "75-100k", "100-150k", "150-200k", "200k-∞"]

race_dropdown_vals = ["Hispanic", "White", "Black", "Asian", "Other"]

internet_dropdown_vals = ["Never", "Rarely", "Sometimes", "Usually", "Always"]

quartiles = ["100%", "75%", "50%", "25%"]

target_hours_val = 4

left_bar_color = "#7fcdbb"
right_bar_color = "#3182bd"

#Get quartile values from dataframe

def get_quartiles(df, val):
    q_values = []
    for i, v in enumerate(val):
        q_values.append(df.quantile(v))
    return q_values

q_values = get_quartiles(pred_df["predicted_probability"][pred_df["SCHLHRS"] == 4], [1, .75, .5, .25])

def seg_val_tracker(race_val, income_val, internet_val, target_hours_val):
    new_seg_val = pred_df[(pred_df["RACE_ETHNICITY"] == race_val) \
    & (pred_df["INCOME"] == income_slider_vals.index(income_val) + 1)\
    & (pred_df["INTRNTAVAIL"] == internet_dropdown_vals[::-1].index(internet_val) + 1)\
    & (pred_df["SCHLHRS"] == target_hours_val)].iloc[:,[5]].values.astype(float)
    st.session_state["segment_val"] = float(new_seg_val) * 100

def quartile_val_tracker(idx):
    st.session_state["quart_val"] = float(q_values[idx]) * 100

if 'quart_val' not in st.session_state:
    st.session_state["quart_val"] = float(q_values[0]) * 100

if 'segment_val' not in st.session_state:
    st.session_state["segment_val"] = 0.5079 * 100 # Default based on segment: Hispanic, 50-75k, Sometimes
#Start Page content

#Title and introduction

st.header("How likely was it that a student had 4 or more days of virtual contact with a teacher in the 2020-2021 school year?")
st.write(" ")
st.write(st.session_state.segment_val)
#Two-column container

col1, col2, col3 = st.columns([3, 3, .5])

height1 = st.session_state.segment_val * 2.5

with col1:
    segment_likelihood = f'''<html>
                                <p style="color:{left_bar_color}; font-size:30px; text-align:center;">likelihood</p>
                            </html>
                        '''
    st.markdown(segment_likelihood, unsafe_allow_html=True)
    segement_html = f'''<html>
                            <body>
                            <div class="container">
                            <p style="color:{left_bar_color}; font-size:80px;">{st.session_state.segment_val:.1f}%
                                <div class="child" style="width:150px;height:{height1}px;border:1px solid {left_bar_color};background-color:{left_bar_color};"></div>
                            </p>
                            </div>
                            </body>
                        </html>
                    '''
    st.markdown(segement_html, unsafe_allow_html=True)
    segment_prompt = f'''<html>
                            <p style="color:{left_bar_color}; font-size:20px; text-align:center;">Select a combination of factors to calculate the probability</p>
                        </html>
                    '''
    st.markdown(segment_prompt, unsafe_allow_html=True)

with col2:
    quart_likelihood = f'''<html>
                                <p style="color:{right_bar_color}; font-size:30px; text-align:center;">likelihood</p>
                            </html>
                        '''
    st.markdown(quart_likelihood, unsafe_allow_html=True)
    height2 = st.session_state.quart_val * 2.5
    quart_val_html = f'''<html>
                            <body>
                            <div class="container">
                            <p style="color:{right_bar_color}; font-size:80px;">{st.session_state.quart_val:.1f}%
                                <div class="child" style="width:150px;height:{height2}px;border:1px solid {right_bar_color};background-color:{right_bar_color};"></div>
                            </p>
                            </div>
                            </body>
                        </html>
                    '''
    st.markdown(quart_val_html, unsafe_allow_html=True)
    segment_prompt = f'''<html>
                        <p style="color:{right_bar_color}; font-size:20px; text-align:center;">Choose a quartile of the population for the comparison group</p>
                    </html>
                '''
    st.markdown(segment_prompt, unsafe_allow_html=True)
with col3:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    Q1 = st.button("Q1", key="Q1", on_click=quartile_val_tracker, args=(0, ))
    Q2 = st.button("Q2", key="Q2", on_click=quartile_val_tracker, args=(1, ))
    Q3 = st.button("Q3", key="Q3", on_click=quartile_val_tracker, args=(2, ))
    Q4 = st.button("Q4", key="Q4", on_click=quartile_val_tracker, args=(3, ))


#Bottom form

with st.form("segment_form"):
    st.header("Factors")
    race_val = st.selectbox("Race", race_dropdown_vals, 
                    help="select a value")
    income_val = st.select_slider("Income", 
                    options = income_slider_vals, 
                    help = "select a value")
    internet_val = st.select_slider("Internet availability",
                    options = internet_dropdown_vals, 
                    help = "select a value")
    submitted = st.form_submit_button("Submit", on_click=seg_val_tracker, #Below passes segment value from pandas df to callback function
                                    args=(race_val, income_val, internet_val, target_hours_val, ))

st.write(internet_dropdown_vals[::-1].index(internet_val) + 1)