import pandas as pd

def importar_csv(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)
    return df