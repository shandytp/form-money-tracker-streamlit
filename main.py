import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("Form Money Tracker")
st.markdown("Masukkan anda khilaf apa hari ini")

@st.cache_resource
def connect_gsheets():
    conn = st.connection("gsheets",
                         type=GSheetsConnection)
    
    return conn

conn = connect_gsheets()

existing_data = conn.read(worksheet="test-dev", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

KATEGORI_KHILAF = [
    "Jajan",
    "Ops",
    "Khilaf"
]

SOURCE_MONEY = [
    "E-wallet",
    "Cash",
    "Transfer",
    "QRIS",
    "Debit"
]

with st.form(key="form_money_tracker", clear_on_submit=True):
    tanggal_kegiatan = st.date_input(label="Tanggal Kegiatan Khilaf")
    nama_kegiatan = st.text_input(label="Nama Kegiatan Khilaf")
    kategori = st.selectbox("Kategori Khilaf", KATEGORI_KHILAF)
    pengeluaran_pemasukan = st.selectbox("Pengeluaran / Pemasukan",
                                         ("Pengeluaran", "Pemasukan"))
    source = st.selectbox("Source Money", SOURCE_MONEY)
    jumlah = st.number_input(label="Berapa bwang luwh keluarin duitnya?",
                             min_value=0)

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        money_tracker_data = pd.DataFrame(
            [
                {
                    "Tanggal Kegiatan": tanggal_kegiatan.strftime("%Y-%m-%d"),
                    "Nama Kegiatan": nama_kegiatan,
                    "Kategori": kategori,
                    "Pengeluaran / Pemasukan": pengeluaran_pemasukan,
                    "Source": source,
                    "Jumlah": jumlah
                }
            ]
        )

        updated_df = pd.concat([existing_data, money_tracker_data], ignore_index=True)

        conn.update(worksheet="test-dev", data=updated_df)

        st.success("Mantap bwanggg")