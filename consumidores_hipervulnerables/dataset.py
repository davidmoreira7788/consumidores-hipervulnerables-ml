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
MODELOS = RAIZ / "models"

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


def definir_clases(rubro_entrenamiento, proporcion_minima=0.015):
    """Rubros que se conservan como clase propia, calculados SOLO con el conjunto de entrenamiento.

    Se conserva todo rubro que represente al menos `proporcion_minima` de los reclamos de entrenamiento
    (1,5 % de 4.842 reclamos son unos 73). Devuelve la lista de rubros conservados.
    """
    frecuencia = rubro_entrenamiento.value_counts()
    return frecuencia[frecuencia >= proporcion_minima * len(rubro_entrenamiento)].index.tolist()


def aplicar_clases(rubro, conservar, etiqueta="Otros"):
    """Reemplaza por `etiqueta` todo rubro que no esté en la lista `conservar`.

    La lista sale del entrenamiento y se aplica igual a prueba: un rubro que no figura en ella (incluso uno que
    no aparece en el entrenamiento) pasa a `Otros`.
    """
    return rubro.where(rubro.isin(conservar), etiqueta)


def clave_fila(df):
    """Texto que identifica a una fila completa (las 8 columnas originales); sirve para detectar repeticiones."""
    return df[COLUMNAS].astype(str).agg("|".join, axis=1)


def etiqueta_estratificacion(rubro, minimo=4):
    """Etiqueta para estratificar la partición: los rubros con menos de `minimo` casos se juntan en '_raro'.

    Solo se usa para repartir los datos de forma pareja; no define las clases del modelo.
    """
    frecuencia = rubro.map(rubro.value_counts())
    return rubro.where(frecuencia >= minimo, "_raro")


def particion_entrenamiento_prueba(df, test_size=0.25, semilla=42):
    """Partición aleatoria estratificada por rubro (los rubros muy raros se juntan solo para estratificar)."""
    from sklearn.model_selection import train_test_split

    return train_test_split(
        df,
        test_size=test_size,
        stratify=etiqueta_estratificacion(df["rubro"]),
        random_state=semilla,
    )


def cramer_v(a, b):
    """V de Cramér entre dos variables categóricas (0 = sin asociación, 1 = total)."""
    from scipy.stats import chi2_contingency

    tabla = pd.crosstab(a, b)
    chi2 = chi2_contingency(tabla)[0]
    n = tabla.values.sum()
    return float(np.sqrt(chi2 / (n * (min(tabla.shape) - 1))))
