import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

def extract_siops(ano: int, bimestre: int, municipio: int, save_base_path: str = "data/raw") -> None:
    """
    Extrai tabelas do SIOPS e salva CSVs na pasta local.
    """
    # Mapeamento de bimestres SIOPS
    bimestres_map = {1: 12, 2: 14, 3: 1, 4: 18, 5: 20, 6: 2}
    bimestre_value = bimestres_map.get(bimestre)
    if bimestre_value is None:
        raise ValueError("Bimestre inválido! Digite um número de 1 a 6.")

    url = "http://siops.datasus.gov.br/rel_LRF.php"
    data = {
        "cmbAno": str(ano),
        "cmbUF": "35",
        "cmbPeriodo": str(bimestre_value),
        "cmbMunicipio[]": str(municipio),
        "BtConsultar": "Consultar"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "http://siops.datasus.gov.br/consleirespfiscal.php"
    }

    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 200:
        raise ConnectionError(f"Erro ao acessar SIOPS: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="tam2 tdExterno")

    if not tables:
        print("Nenhuma tabela encontrada.")
        return

    folder_path = os.path.join(save_base_path, str(ano), str(municipio))
    os.makedirs(folder_path, exist_ok=True)

    for i, table in enumerate(tables, start=1):
        df = pd.read_html(StringIO(str(table)), decimal=",", thousands=".")[0]

        # remove headers repetidos
        if df.shape[0] > 1:
            df = df[df.apply(lambda row: not all(row.astype(str).str.contains(
                "RECEITA|DESPESA|EXERCÍCIO|CONTROLE|TOTAL", case=False)), axis=1)]

        # renomeia colunas
        df.columns = [str(c) for c in df.columns]

        filename = os.path.join(folder_path, f"bim{bimestre}_tabela{i}.csv")
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"✅ CSV salvo em: {filename}")