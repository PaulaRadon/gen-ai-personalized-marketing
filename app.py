import os
import replicate
import requests
import streamlit as st
from bs4 import BeautifulSoup

# App title and configuration
st.set_page_config(page_title="Gen AI Personalized Marketing")
st.title('Gen AI Personalized Marketing')

# Section to input user attributes
st.header('👤Provide User Attributes')

# Function to set preset values for the first button
def set_preset_values_1():
    st.session_state.name = "John Doe"
    st.session_state.age = 30
    st.session_state.email = "john.doe@example.com"
    st.session_state.interests = "Technology, Sports"
    st.session_state.location = "New York"

# Function to set preset values for the second button
def set_preset_values_2():
    st.session_state.name = "Jane Smith"
    st.session_state.age = 25
    st.session_state.email = "jane.smith@example.com"
    st.session_state.interests = "Travel, Cooking"
    st.session_state.location = "Los Angeles"

# Initialize session state if not already initialized
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'age' not in st.session_state:
    st.session_state.age = 0
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'interests' not in st.session_state:
    st.session_state.interests = ""
if 'location' not in st.session_state:
    st.session_state.location = ""

# Set up the input fields
if st.button("Set Preset 1 - John Doe"):
    set_preset_values_1()

if st.button("Set Preset 2 - Jane Smith"):
    set_preset_values_2()

name = st.text_input("Name", value=st.session_state.name, key='name')
age = st.number_input("Age", min_value=0, value=st.session_state.age, key='age')
email = st.text_input("Email", value=st.session_state.email, key='email')
interests = st.text_input("Interests", value=st.session_state.interests, key='interests')
location = st.text_input("Location", value=st.session_state.location, key='location')

# Section to provide marketing context
st.header('📄Provide Marketing Context')

# Initialize variable for marketing context
input_job_context = ''

# Define states for buttons
if 'write_background_button_clicked' not in st.session_state:
    st.session_state.write_background_button_clicked = False

# Define callback function for button state
def click_write_background_button():
    st.session_state.write_background_button_clicked = True

# Button to write background info
st.button("Write Your Background Info", on_click=click_write_background_button)

# Text area for marketing email info if the button is clicked
if st.session_state.write_background_button_clicked:
    input_job_context = st.text_area("Marketing Email Info")

# Function to apply custom CSS styles
def apply_styles():
    with open("style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    st.markdown("""
        <style>
        .card {
            margin: 10px;
            padding: 10px;
            border-radius: 8px;
            background-color: #f9f9f9;
            color: #000000;
            box-shadow: 2px 2px 5px grey;
            height: 300px;
            overflow-y: auto;
        }
        .card h2 {
            color: #000000;
        }
        </style>
        """, unsafe_allow_html=True)

# Apply the custom styles
apply_styles()

# Section for personalized marketing content
st.header('📝Personalized Marketing Content')

# Initialize state for marketing email button
if 'marketing_email_button_clicked' not in st.session_state:
    st.session_state.marketing_email_button_clicked = False

# Callback function for marketing email button
def click_marketing_email_button():
    st.session_state.marketing_email_button_clicked = True

# Button to generate marketing email
st.button("Generate Marketing Email", on_click=click_marketing_email_button)

# Function to generate marketing email using Snowflake Arctic LLM
def generate_marketing_email(applicant_context, job_context):
    temperature = 0.01
    top_p = 0.9
    prompt = []
    prompt.append("\n" + ''.join(person_info) + "")
    prompt.append("\n" + ''.join(input_job_context) + "")
    prompt.append("user Hi, I would like to generate a marketing email ")
    prompt.append("assistant")
    prompt.append("")
    prompt_str = "\n".join(prompt)
    
    output = replicate.run("snowflake/snowflake-arctic-instruct",
                           input={"prompt": prompt_str,
                                  "prompt_template": r"{prompt}",
                                  "temperature": temperature,
                                  "top_p": top_p})
    return output

# Generate and display the marketing email if the button is clicked
if st.session_state.marketing_email_button_clicked:
    st.subheader("Generated Marketing Email")
    person_info = f"Name: {st.session_state.name}, Age: {st.session_state.age}, Email: {st.session_state.email}, Interests: {st.session_state.interests}, Location: {st.session_state.location}"
    marketing_email_response = "".join(generate_marketing_email(person_info, input_job_context))
    st.write(marketing_email_response)

# Sidebar for Replicate credentials
with st.sidebar:
    st.title('Gen AI Personalized Marketing')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your Replicate API token.', icon='⚠️')
            st.markdown("**Don't have an API token?** Head over to [Replicate](https://replicate.com) to sign up for one.")

    os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Sidebar footer
st.sidebar.caption('Built by [@PaulaRadon](https://github.com/PaulaRadon) for the [2024 The Future of AI is Open Hackathon](https://arctic-streamlit-hackathon.devpost.com/).')
st.sidebar.caption('App hosted on [Streamlit Community Cloud](https://streamlit.io/cloud). Model hosted by [Replicate](https://replicate.com/snowflake/snowflake-arctic-instruct).')
st.sidebar.caption('This App referenced the [Snowflake Arctic Streamlit Example](https://github.com/streamlit/snowflake-arctic-st-demo/tree/main) as a starting point.')
