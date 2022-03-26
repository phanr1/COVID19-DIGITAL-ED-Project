import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="The Digital Divide",
    page_icon="🎓",
    layout="wide"
)
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

student_group_vals = ["No contact", "1 day of contact", "2-3 days of contact", "4 or more days"]

target_hours_val = 4

compar_hours_val = list(set(pred_df["SCHLHRS"]))

def seg_val_tracker(race_val, income_val, internet_val, target_hours_val):
    new_seg_val = pred_df[(pred_df["RACE_ETHNICITY"] == race_val) \
    & (pred_df["INCOME"] == income_slider_vals.index(income_val) + 1)\
    & (pred_df["INTRNTAVAIL"] == internet_dropdown_vals[::-1].index(internet_val) + 1)\
    & (pred_df["SCHLHRS"] == target_hours_val)].iloc[:,[5]].values.astype(float)
    return float(new_seg_val * 100)

left_bar_color = "#7fcdbb"
right_bar_color = "#3182bd"

#Start Page content

#Title

st.header("Demograpics determined the likelihood that a student had contact with a teacher during the pandemic.")

#Three-column container

col1, col2, col3 = st.columns(3)

with col1:

#Input form

    with st.form("segment_form"):
        st.subheader("Student Traits")
        race_val = st.selectbox("Race", race_dropdown_vals, 
                        help="select a value")
        income_val = st.select_slider("Income",
                        options = income_slider_vals,
                        value = "50-75k",
                        help = "select a value")
        internet_val = st.select_slider("Internet availability",
                        options = internet_dropdown_vals,
                        value="Sometimes",
                        help = "select a value")
        st.subheader("Compared to average student in group")
        hour_val = st.select_slider("Hours", student_group_vals, 
                        help="select a value")
        submitted = st.form_submit_button("Submit")


new_seg_val = seg_val_tracker(race_val, income_val, internet_val, target_hours_val)
index = student_group_vals.index(hour_val) + 1
mean_values = round(pred_df["predicted_probability"][pred_df["SCHLHRS"] == index].mean(), 1) * 100

st.write(pred_df["predicted_probability"][pred_df["SCHLHRS"] == index])
with col2:
    
    height1 = new_seg_val * 2.5
    segement_html = f'''<html>
                            <body>
                            <div class="container">
                            <p style="color:{left_bar_color}; font-size:60px;">{new_seg_val:.1f}%
                                <div class="child" style="width:150px;height:{height1}px;border:1px solid {left_bar_color};background-color:{left_bar_color};"></div>
                            </p>
                            </div>
                            </body>
                        </html>
                    '''
    st.markdown(segement_html, unsafe_allow_html=True)
    lower_internet_val = internet_val.lower()
    segment_likelihood = f'''<html>
                                <p style="color:{left_bar_color}; font-size:20px; text-align:center;">Likelihood that <mark>{race_val}s</mark> who <mark>{lower_internet_val}</mark> have internet avalibilty and live in a household with an income of <mark>{income_val}</mark> had virtual contact with a teacher <mark>four or more times</mark> per week.</p>
                            </html>
                        '''
    st.markdown(segment_likelihood, unsafe_allow_html=True)

with col3:
    height2 = mean_values * 2.5
    mean_val_html = f'''<html>
                            <body>
                            <div class="container">
                            <p style="color:{right_bar_color}; font-size:60px;">{mean_values:.1f}%
                                <div class="child" style="width:150px;height:{height2}px;border:1px solid {right_bar_color};background-color:{right_bar_color};"></div>
                            </p>
                            </div>
                            </body>
                        </html>
                    '''
    st.markdown(mean_val_html, unsafe_allow_html=True)
    mean_likelihood = f'''<html>
                                <p style="color:{right_bar_color}; font-size:20px; text-align:center;">Likelihood that the <mark>average</mark> student had virtual contact with a teacher <mark>four or more times</mark> per week.</p>
                            </html>
                        '''
    st.markdown(mean_likelihood, unsafe_allow_html=True)

st.write("*All values are for the 2020-2021 school year.")