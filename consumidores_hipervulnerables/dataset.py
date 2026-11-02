"""Carga y normalización del dataset de consumidores hipervulnerables.

El archivo crudo (data/raw) NO se modifica nunca: todas las correcciones se
aplican en memoria y, si hace falta, se guardan en data/interim.
"""
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw" / "consumidores-hipervulnerables.csv"
INTERIM = RAIZ / "data" / "interim" / "consumidores_normalizado.csv"
PROCESSED = RAIZ / "data" / "processed"

COLUMNAS = [
    "rubro", "motivo", "vulnerabilidad", "mes_anio_tratamiento",
    "edad", "genero", "provincia_consumidor", "provincia_id",
]
TEXTO = ["rubro", "motivo", "vulnerabilidad", "genero", "provincia_consumidor"]


def cargar_crudo(ruta=RAW):
    """Lee el CSV tal como viene (codificación latin-1, separador coma)."""
    return pd.read_csv(ruta, encoding="latin-1")


def normalizar(df):
    """Devuelve una copia con las correcciones de formato documentadas.

    - Renombra las columnas (el encabezado original trae ';;;' pegado a la última).
    - Quita el ';;;' sobrante de la columna provincia_id y la pasa a entero.
    - Elimina espacios sobrantes en los textos.
    - Unifica 'Adulto/a Mayor' con 'Adulto/a mayor'.
    No elimina filas.
    """
    out = df.copy()
    out.columns = COLUMNAS
    out["provincia_id"] = (
        out["provincia_id"].astype(str).str.replace(";", "", regex=False).astype(int)
    )
    for col in TEXTO:
        out[col] = out[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    out["vulnerabilidad"] = out["vulnerabilidad"].replace({"Adulto/a Mayor": "Adulto/a mayor"})
    out["mes"] = out["mes_anio_tratamiento"].str.strip().str[:3]
    out["anio"] = 2000 + out["mes_anio_tratamiento"].str.strip().str[-2:].astype(int)
    return out


def agrupar_rubros(rubro, umbral=100, etiqueta="Otros"):
    """Mantiene los rubros con al menos `umbral` casos y agrupa el resto."""
    frecuencia = rubro.value_counts()
    conservar = frecuencia[frecuencia >= umbral].index
    return rubro.where(rubro.isin(conservar), etiqueta)


def cramer_v(a, b):
    """V de Cramér entre dos variables categóricas (0 = sin asociación, 1 = total)."""
    from scipy.stats import chi2_contingency

    tabla = pd.crosstab(a, b)
    chi2 = chi2_contingency(tabla)[0]
    n = tabla.values.sum()
    return float(np.sqrt(chi2 / (n * (min(tabla.shape) - 1))))
