import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
from datetime import datetime
import time
from typing import Union,cast,Sequence
from zoneinfo import ZoneInfo
# from production import *

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

def connect_to_gsheet(sheet,sheet_name='Sheet1'):
    scope = ["https://spreadsheets.google.com/feeds", 
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", 
             "https://www.googleapis.com/auth/drive"]
    creds_dict=st.secrets['account']
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(credentials) # type: ignore
    spreadsheet = client.open(sheet).worksheet(sheet_name)  
    return spreadsheet 


def daily_production():
    column=['Supervisor Name','Operators Name','Reactor Number','Product Batch Number','Grade',
            'Date','Process Start Time','Reaction Start Time','Cooling Start Time',
            'Filter Start Time','Process Completed at Time']
    st.header('Daily Production Report')
    if 'daily_production_list' not in st.session_state:
        st.session_state.daily_production_list=pd.DataFrame([['']*len(column)],columns=column)
    sheet=connect_to_gsheet(sheet='Production',sheet_name='Daily Production')
    if 'step' not in st.session_state:
        st.session_state.step=0
    for i in range(len(column)):
        if st.session_state.step==i and i<4:
            input=st.text_input(column[i],value=st.session_state.daily_production_list.at[0,column[i]])
            if st.button(f'Add {column[i]}',key=f'TN_dp_{i}'):
                st.session_state.daily_production_list.at[0,column[i]]=input
                st.session_state.step+=1
        if st.session_state.step==i and i==4:
            grade_name=st.selectbox('Please select the Grade',('KK-117','ABK-99','ABK-399','ABK-TP (6%)','KK-405'),placeholder='-',key=f'grade_name_{i}')
            if st.button(f'Add {column[i]}',key=f'TN1_{i}'):
                st.session_state.daily_production_list.at[0,column[i]]=grade_name
                st.session_state.step+=1
        
        if st.session_state.step==i and i==5:
            val = st.session_state.daily_production_list.at[0, column[i]]
            if isinstance(val, str) or pd.isna(val) or val == "":
                val = datetime.now(ZoneInfo("Asia/Kolkata")).date()
            user_input = st.date_input(column[i], value=val, key=f"input_{i}")
            if st.button(f"Add {column[i]}", key=f"TN_dp_{i}"):
                st.session_state.daily_production_list.at[0, column[i]] = user_input.isoformat()
                st.session_state.step += 1
        if st.session_state.step==i and i>5:
            input=datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
            if st.button(f'Add {column[i]}',key=f'TN_dp_{i}'):
                st.session_state.daily_production_list.at[0,column[i]]=input
                st.session_state.step+=1
    if st.session_state.step>=len(column):
        if st.button('Submit',key='submit_daily_production'):
            sheet.append_row(st.session_state.daily_production_list.values.tolist()[0])
            time.sleep(2)
            st.success('Data Updated Successfully')
    st.dataframe(st.session_state.daily_production_list)

def product_elements(grade_name):
    kk_117={
        'DM':302.79,
        'E-01':4.85,
        'M-03':1063,
        'M-05':21.400,
        'DM':720,
        'E-01':1.0,
        'ADD DM E-01':1.0,
        'E-02':1.0,
        'ADD DM E-02':1.0,
        'S-02':0.570,
        'ADD DM S-02':10,
        'C-01':5,
        'ADD DM C-01':30,
        'An-01':12.500,
        'Add DM An-01':16.67,
        'E-03':7,
        'ADD HOT DM E-03':18,
        'T-01':0.400,
        'ADD DM T-01':3.330,
        'R-01':0.700,
        'ADD DM R-01':10,
        'F-02': 3,
        'ADD DM F-02':5,
        'F-01':0.120,
        'ADD DM F-01':1.67,
        'Total in kgs':2000
    }
    abk_tp6={
        'DM':570,
        'S-01':3.195,
        'ADD DM S-01':12,
        'M-03': 565.25,
        'M-01': 790,
        'M-05':21.28,
        'DM M-05':659,
        'S-01':3.195,
        'ADD DM S-01':12,
        'A-03':2.130,
        'ADD DM A-03':11.5,
        'S-02':4.79,
        'ADD DM S-02':35,
        'C-03':5.586,
        'ADD DM C-03':35,
        'T-01':0.798,
        'ADD DM T-01':24,
        'A-02':0.187,
        'ADD DM A-02':14.7, 
        'AN-01':16.130,
        'ADD DM AN-01':5.8,
        'F-03':2.66,
        'ADD DM F-03':5.8,
        'Total in kgs':2000
    }
    abk_99={
        'DM':800,
        'E-01':5.700,
        'ADD DM E-01':12,
        'E-02':5.700,
        'ADD DM E-02':12,
        'M-02': 1008,
        'M-01': 233,
        'M-04': 62,
        'M-03': 62,
        'M-06': 69.200,
        'DM M-06': 600,
        'E-01':1.450,
        'ADD DM E-01':6,
        'E-02':1.450,
        'DM E-02':6,
        'C-01':8,
        'ADD DM C-01':94.13,
        'C02':8,
        'ADD DM C02':94.13,
        'An-01':3.88,
        'ADD DM An-01':5,
        'F-01':0.360,
        'DM F-01':2,
        'Total':3100
        }
    abk_399={
        'DM':454.19,
        'E-01':7.275,
        'M-03':1594.5,
        'M-05':32.100,
        'DM M-05':720,
        'E-01':1.5,
        'ADD DM E-01':1.5,
        'E-02':1.5,
        'ADD DM E-02':1.5,
        'S-02':0.855,
        'ADD DM S-02':15,
        'C-01':7.5,
        'ADD DM C-01':45,
        'An-01':18.75,
        'ADD DM An-01':25,
        'E-03':10.500,
        'ADD HOT DM E-03':27,
        'T-01':0.600,
        'ADD DM T-01':5,
        'R-01':1.050,
        'ADD DM R-01':15,
        'F-02':4.5,
        'ADD DM F-02':7.5,
        'F-01':0.180,
        'ADD DM F-01':2.50,
        'Total':3000
        }
    kk_405={
        'DM':327,
        'E-01':2.45,
        'ADD DM E-01':8,
        'A-01':27.65,
        'M-11':1001.5,
        'M-01':134,
        'DM M-01':347,
        'E-01': 0.280,
        'ADD DM E-01':8,
        'A-02':0.280,
        'ADD DM A-02':8,
        'C-01':4.36,
        'ADD DM C-01':66,
        'C-01':0.390,
        'ADD DM C-01':23,
        'C-01': 0.485,
        'ADD DM C-01':15,
        'LC 40 PART-1':93,
        'T-01': 0.410,
        'ADD DM T-01':6.5, 
        'R-01':0.360,
        'ADD DM R-01':6.5,
        'F-02':5.4,
        'ADD DM F-02':6.5,
        'AN-01':3.15,
        'ADD DM AN-01':4.6,
        'Total':2100
        }
    grades={
        'KK-117':kk_117,
        'ABK-99':abk_99,
        'ABK-399':abk_399,
        'ABK-TP (6%)':abk_tp6,
        'KK-405':kk_405
    }
    return grades[grade_name]


def production_report():
    st.header('Production Report (In Kgs)')
    sheet=connect_to_gsheet(sheet='Production',sheet_name='Production Report Summary')
    column=['Date','Grade Name']
    if 'production_report_df' not in st.session_state:
        st.session_state.production_report_df=pd.DataFrame([['']*len(column)],columns=column)
    if 'step_2' not in st.session_state:
        st.session_state.step_2=0
    if st.session_state.step_2==0:
        val = st.session_state.production_report_df.at[0, column[0]]
        if isinstance(val, str) or pd.isna(val) or val == "":
            val = datetime.now(ZoneInfo("Asia/Kolkata")).date()
            user_input = st.date_input(column[0], value=val, key=f"input_pr_{0}")
            if st.button(f"Add {column[0]}", key=f"TN0_{0}"):
                st.session_state.production_report_df.at[0, column[0]] = user_input.isoformat()
                st.session_state.step_2+=1
    grade_name=st.selectbox('Please select the Grade',('KK-117','ABK-99','ABK-399','ABK-TP (6%)','KK-405'),placeholder='-',key=f'grade_name_{1}')
    if st.session_state.step_2==1:
        if st.button(f'Add {column[1]}',key=f'TN1_{1}'):
            st.session_state.production_report_df.at[0,column[1]]=grade_name
            st.session_state.step_2+=1
    grade=product_elements(grade_name)
    if 'grade_df ' not in st.session_state:
        st.session_state.grade_df = pd.DataFrame(list(grade.items()), columns=["Element", "Weight"])
        st.session_state.grade_df['Batch Number']=''
        st.session_state.grade_df['Date']=st.session_state.production_report_df['Date'].iloc[0]
        st.session_state.grade_df['Grade']=st.session_state.production_report_df['Grade Name'].iloc[0]
    if grade:
        editor=st.data_editor(
            st.session_state.grade_df,
            num_rows='dynamic',
            use_container_width=True,
            width='stretch',
            key='data_editor_grade'
        )
        st.session_state.grade_df=editor
    if st.button('submit',key='submit_production_report'):
        try:
            sheet.append_rows(st.session_state.grade_df.values.tolist())
            time.sleep(2)
            st.success('Data has been updated successfully')
        except:
            st.write('Error Observed')




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
