import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd
from vega_datasets import data

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

st.title('Selamat Datang di Dashboard Sepatu Rapi :chart_with_upwards_trend:')
st.write('Laporan Jumlah Sepatu yang Tertata Rapi')
tabChart, tabInput, tabData, tabDelete = st.tabs(['Chart 📊','Input Data ✍️', 'Edit Data 📝', 'Delete Data 🗑️'])

if df.empty:
    st.warning('Data Masih kosong ⛔')
else:

    # Display the chart
    source = df
    tabChart.subheader('Chart Jumlah Sepatu yang Tertata Rapi')
    tabChart.bar_chart(source, x='Tanggal', y='Jumlah Sepatu Rapi', color='Kelas', stack=False)
    
    # Display the data
    tabData.subheader('Edit Data Jumlah Sepatu yang Tertata Rapi')
    edited_df = tabData.data_editor(df)
    if tabData.button('Save Changes'):
        for i, row in edited_df.iterrows():
            target_value = row['Jumlah Sepatu Rapi'] / row['Jumlah Siswa']
            worksheet.update(f'A{i+2}', [[row['Tanggal'], row['Kelas'], row['Jumlah Sepatu Rapi'], row['Jumlah Siswa'], target_value]])
        st.toast('Data berhasil disimpan ke Google Sheets', icon='📝') 
    
    # Display Delete functionality
    tabDelete.subheader('Delete Data Jumlah Sepatu yang Tertata Rapi')
    tabDelete.table(df)
    selected_rows = tabDelete.multiselect('Select rows to delete', edited_df.index)
    if tabDelete.button('Delete Selected Rows'):
        if selected_rows:
            edited_df.drop(selected_rows, inplace=True)
            # Update Google Sheets after deletion
            worksheet.clear()  # Clear the existing data
            worksheet.update([df.columns.values.tolist()] + edited_df.values.tolist())  # Update with new data
        st.toast('Selected rows deleted and changes saved to Google Sheets', icon='🗑️')


# Display the input form
tabInput.subheader('Masukkan data jumlah sepatu yang tertata rapi')
form = tabInput.form('input_form')
with form:
    tanggal = st.date_input('Tanggal')
    kelas = st.selectbox('Kelas', 'Kelas-1A Kelas-1B Kelas-1C Kelas-1D'.split())
    jumlah_rapi = st.select_slider('Jumlah Sepatu yang Tertata Rapi', options=range(1, 28))
    submit_button = st.form_submit_button(label='Submit Data')

    # Submit data to Google Sheets
    if submit_button:
        if kelas and jumlah_rapi:
            # convert tanggal to string
            tanggal_str = tanggal.strftime('%Y-%m-%d')

            if kelas == 'Kelas-1A':
                jumlah_siswa = 27
            elif kelas == 'Kelas-1B':
                jumlah_siswa = 28
            elif kelas == 'Kelas-1C':
                jumlah_siswa = 29
            elif kelas == 'Kelas-1D':
                jumlah_siswa = 30

            target = jumlah_rapi / jumlah_siswa

            # append data to Google Sheets
            worksheet.append_row([tanggal_str, kelas, jumlah_rapi, jumlah_siswa, target])
            st.toast('Data berhasil ditambahkan ke Google Sheets', icon='🚀')
        else:
            st.error('Data tidak boleh kosong')

st.sidebar.title('About')
st.sidebar.info(
    '''
    This app is created to demonstrate the integration of Streamlit with Google Sheets API.
    '''
)