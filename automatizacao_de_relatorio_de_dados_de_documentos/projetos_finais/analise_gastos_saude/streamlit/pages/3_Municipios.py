import streamlit as st
import pandas as pd
import pickle


st.set_page_config(page_title="Municípios", page_icon="🏥", layout="wide")

st.title('_Municípios_')
st.markdown("---")

figura1 = ''
figura2 = ''

arquivo1 = './fig2.pkl'
arquivo2 = './fig.pkl'

col1, col2 = st.columns(2)

with col1:
    with open(arquivo1, 'rb') as pickle_file:
        figura1 = pickle.load(pickle_file)
    st.write("## Gastos Hospitalares - UF")
    st.plotly_chart(figura1)

with col2:
    with open(arquivo1, 'rb') as pickle_file:
        figura2 = pickle.load(pickle_file)
    st.write("## Gastos Hospitalares per capita - UF")
    st.plotly_chart(figura2)
