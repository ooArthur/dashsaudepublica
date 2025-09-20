import os
import re
import pandas as pd

def _strip_cols(cols):
    return [re.sub(r"\s+", " ", str(c)).strip() for c in cols]

def limpar_df(df: pd.DataFrame) -> pd.DataFrame:
    # renomeia colunas
    df.columns = _strip_cols(df.columns)

    # remove colunas vazias ou Unnamed
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed", case=False)]
    df = df.dropna(axis=1, how='all')

    # remove segunda coluna se duplicada
    if df.shape[1] >= 2:
        c0 = df.iloc[:, 0].astype(str).str.strip().fillna("")
        c1 = df.iloc[:, 1].astype(str).str.strip().fillna("")
        if c0.equals(c1):
            df = df.drop(columns=df.columns[1])

    # identificar colunas numéricas
    num_part = df.iloc[:, 2:] if df.shape[1] > 2 else pd.DataFrame(index=df.index)
    if not num_part.empty:
        num_coerced = num_part.apply(pd.to_numeric, errors='coerce')
        keep = ~num_coerced.isna().all(axis=1)
        df = df.loc[keep].copy()

    df.reset_index(drop=True, inplace=True)
    return df


def normalize_siops(base_path: str, municipio: str, ano: str = None, bimestre: str = None, save: bool = False) -> dict:
    """
    Lê CSVs do SIOPS, limpa, normaliza e concatena por tabela.
    Se ano/bimestre forem informados, processa apenas essa pasta.
    Retorna um dict {tabelaX: DataFrame}.
    Se save=True, salva os arquivos normalizados em data/processed/{municipio}.
    """
    dataframes = {}
    schemas = {}

    anos = [ano] if ano else sorted([d for d in os.listdir(base_path) if d.isdigit()])

    for ano_item in anos:
        ano_path = os.path.join(base_path, ano_item, municipio)
        if not os.path.isdir(ano_path):
            continue

        for filename in sorted(os.listdir(ano_path)):
            if not filename.endswith(".csv"):
                continue

            # Se quiser filtrar por bimestre
            if bimestre and not filename.startswith(f"bim{bimestre}_"):
                continue

            m = re.match(r"bim(\d+)_tabela(\d+)\.csv", filename)
            if not m:
                continue
            bim, tabela = m.groups()
            tabela_key = f"tabela{tabela}"
            filepath = os.path.join(ano_path, filename)

            df_raw = pd.read_csv(filepath, header=1, dtype=str, keep_default_na=False, na_values=[""])
            df = limpar_df(df_raw)

            # esquema fixo por tabela
            if tabela_key not in schemas:
                schemas[tabela_key] = df.columns.tolist()
            else:
                df = df.reindex(columns=schemas[tabela_key])

            df["ano"] = int(ano_item)
            df["bimestre"] = int(bim)

            if tabela_key not in dataframes:
                dataframes[tabela_key] = df
            else:
                dataframes[tabela_key] = pd.concat([dataframes[tabela_key], df], ignore_index=True)

    # drop colunas duplicadas pós-concat
    for k, df in dataframes.items():
        df = df.loc[:, ~df.T.duplicated(keep='first')].reset_index(drop=True)
        dataframes[k] = df

        if save:
            processed_dir = os.path.join("data", "processed", municipio)
            os.makedirs(processed_dir, exist_ok=True)
            outpath = os.path.join(processed_dir, f"{k}.csv")
            df.to_csv(outpath, index=False, encoding="utf-8-sig")

    return dataframes