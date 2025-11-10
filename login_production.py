import streamlit as st,pandas as pd
from production import *

st.set_page_config(layout='wide')
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


if 'logged_in' not in st.session_state:
    st.session_state['logged_in']=False

def sign_in(email,password):
    creds=st.secrets['email_password']
    return creds.get(email)==password

def main_app(email):
    st.write(f"Welcome {email}! This is the main app.")
    options=st.radio('Choose an option',('Daily Production','Production Report'))
    if options=='Daily Production':
        daily_production()
    elif options=='Production Report':
        production_report()

def login():
    with st.form(key='login_form'):
        email = st.text_input('Email ID', key='email')
        password = st.text_input('Password', type='password', key='password')
        if st.form_submit_button('Submit', key='submit'):
            if sign_in(email, password):
                st.session_state.user_email = email
                st.session_state.authenticated = True
                st.success("Logged in successfully!")
                st.rerun() 
            else:
                st.error("Invalid email or password.")

if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated and st.session_state.user_email:
    main_app(st.session_state.user_email)
else:
    login()