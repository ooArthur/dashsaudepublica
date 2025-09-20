import streamlit as st
import os
import pandas as pd

# Importa funções do seu pacote src
from src.extract import extract_siops  # futuramente adicione outras fontes
from src.transform.siops_cleaner import normalize_siops

st.set_page_config(page_title="Extração de Dados", layout="wide")
st.title("Extração de Dados das Fontes de Saúde")

# Menu lateral: escolha da fonte
fonte = st.sidebar.selectbox(
    "Escolha a fonte de dados:",
    ["SIOPS"]  # futuramente adicione outras: "DataSUS", etc.
)

# Base de dados
base_path = "data/raw"
processed_path = "data/processed"
municipio_default = 355645

if fonte == "SIOPS":
    st.header("Extração SIOPS")
    ano = st.number_input("Ano", min_value=2000, max_value=2030, value=2023)
    bimestre = st.selectbox("Bimestre", options=list(range(1, 7)))
    municipio = st.text_input("Código do Município", value=str(municipio_default))

    # Botão de extração
    if st.button("Extrair dados do SIOPS"):
        with st.spinner("Extraindo dados do SIOPS..."):
            extract_siops(
                ano=ano,
                bimestre=bimestre,
                municipio=int(municipio),
                save_base_path=base_path
            )
        st.success("Extração concluída!")

    # Exibição de DataFrame bruto (RAW)
    csv_folder = os.path.join(base_path, str(ano), municipio)
    if os.path.exists(csv_folder):
        st.subheader("Arquivos brutos extraídos (RAW)")
        for f in sorted(os.listdir(csv_folder)):
            if f.endswith(".csv"):
                file_path = os.path.join(csv_folder, f)
                df_raw = pd.read_csv(file_path, header=None)
                col1, col2 = st.columns([20, 1])
                with col1:
                    st.markdown(f"**{f}**")
                with col2:
                    if st.button("🗑️", key=f"del_raw_{f}"):
                        os.remove(file_path)
                        st.warning(f"Arquivo RAW {f} excluído.")
                        st.rerun()

                # dataframe abaixo do título + botão
                st.dataframe(df_raw, use_container_width=True)



        if st.button("Normalizar e salvar em PROCESSED"):
            with st.spinner("Normalizando e salvando..."):
                normalize_siops(
                    base_path=base_path,
                    municipio=municipio,
                    ano=str(ano),
                    bimestre=str(bimestre),
                    save=True
                )
            st.success("Normalização concluída e salva!")


    # Exibição de DataFrame limpo (PROCESSED)
    processed_folder = os.path.join(processed_path, municipio)
    if os.path.exists(processed_folder):
        st.subheader("Arquivos normalizados (PROCESSED)")
        for f in sorted(os.listdir(processed_folder)):
            if f.endswith(".csv"):
                file_path = os.path.join(processed_folder, f)
                df_norm = pd.read_csv(file_path)

                col1, col2 = st.columns([20, 1])
                with col1:
                    st.markdown(f"**{f}**")
                with col2:
                    if st.button("🗑️", key=f"del_norm_{f}"):
                        os.remove(file_path)
                        st.warning(f"Arquivo normalizado {f} excluído.")
                        st.rerun()

                # dataframe abaixo do título + botão
                st.dataframe(df_norm, use_container_width=True)
