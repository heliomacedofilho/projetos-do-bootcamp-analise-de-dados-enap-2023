import streamlit as st
import pandas as pd

# st.set_page_config(page_title="Municípios", page_icon="🏥", layout="wide")

st.title('_Análise Descritiva:_ Mapas')
st.markdown("---")

st.write("## A ideia é trazer mapas com dados dos municípios")

@st.cache_data
def gerar_df():
    df = pd.read_excel('./data/variaveis_uf_ano.xlsx',
                       engine='openpyxl',
                       usecols='A:F',
                       nrows=244)
    return df

df = gerar_df()
df