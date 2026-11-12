"""Métricas de evaluación para clasificación multiclase con clases desbalanceadas."""
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    precision_recall_fscore_support,
)


def resumen(y_real, y_pred):
    """Métricas globales: exactitud, exactitud balanceada, F1 macro y F1 ponderado."""
    return {
        "exactitud": accuracy_score(y_real, y_pred),
        "exactitud balanceada": balanced_accuracy_score(y_real, y_pred),
        "F1 macro": f1_score(y_real, y_pred, average="macro", zero_division=0),
        "F1 ponderado": f1_score(y_real, y_pred, average="weighted", zero_division=0),
    }


def por_clase(y_real, y_pred, clases):
    """Precisión, recall, F1 y cantidad de casos reales de cada clase."""
    p, r, f, n = precision_recall_fscore_support(y_real, y_pred, labels=clases, zero_division=0)
    return pd.DataFrame({"precisión": p, "recall": r, "F1": f, "casos": n}, index=clases)


def intervalo_bootstrap(y_real, y_pred, metrica, repeticiones=1000, semilla=42, nivel=0.95):
    """Intervalo aproximado para una métrica, remuestreando con reposición los casos de prueba.

    Refleja solo la variabilidad por el tamaño de la prueba (no la variabilidad de entrenar con otros datos).
    """
    rng = np.random.default_rng(semilla)
    y_real = np.asarray(y_real)
    y_pred = np.asarray(y_pred)
    valores = []
    for _ in range(repeticiones):
        idx = rng.integers(0, len(y_real), len(y_real))
        valores.append(metrica(y_real[idx], y_pred[idx]))
    bajo = (1 - nivel) / 2
    return float(np.quantile(valores, bajo)), float(np.quantile(valores, 1 - bajo))


def diferencia_bootstrap(y_real, pred_a, pred_b, metrica, repeticiones=1000, semilla=42, nivel=0.95):
    """Intervalo para la diferencia de una métrica entre dos modelos (a - b) evaluados sobre los mismos casos.

    Se remuestrean los mismos índices para ambos modelos (diferencia apareada). Si el intervalo incluye el 0, con este
    tamaño de prueba no se puede afirmar que uno sea mejor que el otro.
    """
    rng = np.random.default_rng(semilla)
    y_real, pred_a, pred_b = np.asarray(y_real), np.asarray(pred_a), np.asarray(pred_b)
    valores = []
    for _ in range(repeticiones):
        idx = rng.integers(0, len(y_real), len(y_real))
        valores.append(metrica(y_real[idx], pred_a[idx]) - metrica(y_real[idx], pred_b[idx]))
    bajo = (1 - nivel) / 2
    return float(np.quantile(valores, bajo)), float(np.quantile(valores, 1 - bajo))
