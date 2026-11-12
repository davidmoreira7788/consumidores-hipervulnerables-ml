"""Preprocesamiento de las variables predictoras (codificación y escalado)."""
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Escenarios de variables predictoras. A incluye `vulnerabilidad`, condicionado al supuesto de que esté disponible
# al ingresar el reclamo (no confirmado). B no la incluye.
ESCENARIOS = {
    "A": {"cat": ["vulnerabilidad", "genero", "provincia_consumidor"], "num": ["edad"]},
    "B": {"cat": ["genero", "provincia_consumidor"], "num": ["edad"]},
}


def construir_preprocesador(cat, num, min_frequency=5):
    """Devuelve un ColumnTransformer SIN ajustar.

    - `cat`: columnas categóricas -> one-hot (una columna 0/1 por categoría). Las categorías con menos de
      `min_frequency` casos se agrupan en una categoría «infrecuente»; las categorías desconocidas en prueba se ignoran.
    - `num`: columnas numéricas -> estandarización (media 0, desvío 1), para llevarlas a una escala comparable con las
      columnas 0/1. Importa para los modelos basados en distancias, como K-NN.

    Se devuelve sin ajustar para poder incluirlo dentro de un Pipeline: así, en cada partición de la validación
    cruzada se ajusta solo con los datos de entrenamiento de esa partición.
    """
    return ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=min_frequency, sparse_output=False), cat),
            ("num", StandardScaler(), num),
        ]
    )
