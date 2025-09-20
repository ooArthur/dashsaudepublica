import streamlit as st
import os
import pandas as pd
from src.transform.siops_cleaner import normalize_siops

st.set_page_config(page_title="Dashboard Saúde - Vargem Grande", layout="wide")
st.title("Dashboard Saúde - Vargem Grande")

# Base de dados
municipio = "355645"
base_path = "data/raw"

# Resumo das extrações
st.header("Resumo das Extrações")
overview = []


df_overview = pd.DataFrame(overview)
st.dataframe(df_overview)

# Evolução de gastos
st.header("Evolução de Gastos - SIOPS")
# dfs = normalize_siops(base_path=base_path, municipio=municipio)

st.markdown("---")
st.info("Use o menu lateral para ir às páginas de Extração ou Dashboards detalhados.")