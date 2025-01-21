import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# Google Sheets API
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Google Sheets API credentials
credentials = Credentials.from_service_account_file("credentials.json", scopes=scope)
gc = gspread.authorize(credentials)

# Google Sheets URL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1UV9zQJo2vTgk2RT-Q6aX9ZvGTmA6d58xeEec1u9yrU0"
sh = gc.open_by_url(spreadsheet_url)

# Google Sheets worksheet
worksheet = sh.sheet1

# Get all values from the worksheet
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Form inputs
st.write('Input Data Google Sheets')
with st.form('input_form'):
    tanggal = st.date_input('Tanggal')
    kelas = st.selectbox('Kelas', 'Kelas-1A Kelas-1B Kelas-1C Kelas-1D'.split())
    jumlah = st.select_slider('Jumlah Sepatu yang Tertata Rapi', options=range(1, 28))
    submit_button = st.form_submit_button(label='Submit Data')

# Submit data to Google Sheets
if submit_button:
    if kelas and jumlah:
        # convert tanggal to string
        tanggal_str = tanggal.strftime('%Y-%m-%d')

        # append data to Google Sheets
        worksheet.append_row([tanggal_str, kelas, jumlah])
        st.success('Data berhasil ditambahkan ke Google Sheets')
    else:
        st.error('Data tidak boleh kosong')

# Display the data
st.write('Data from Google Sheets')
st.dataframe(df)