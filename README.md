# Clasificación del rubro de reclamos de consumidores hipervulnerables

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Proyecto de **Aprendizaje Automático** – Centro Politécnico Superior Malvinas Argentinas (2026).
Autor: David Moreira.

## Objetivo

**Pregunta de investigación:** ¿es posible clasificar el rubro de un reclamo de consumidores a partir de
variables sociodemográficas y territoriales, comparando Regresión Logística, K-NN y Árbol de Decisión?
Se probarán esos tres modelos y se presentará en detalle el que se elija como modelo final.

**Tipo de problema:** clasificación **multiclase** (multinomial).

**Momento de la predicción (supuesto):** al ingresar un reclamo, con el perfil de la persona y antes de conocer su
rubro.

> Los resultados se interpretan solo como **asociaciones dentro de los reclamos registrados** en el período
> cubierto por el dataset. No permiten afirmar qué grupos están más expuestos al problema, porque no hay
> información de quienes no reclamaron ni de cuántas personas de cada grupo consumen cada servicio.

## Datos

**Qué representa cada fila:** un reclamo de un consumidor registrado por el programa. El dataset no trae
identificador de reclamo ni de persona.

- **Fuente:** Datos Argentina, Ministerio de Desarrollo Productivo. Programa Consumidores Hipervulnerables.
- **Ficha del dataset en Datos Argentina:** https://datos.gob.ar/dataset/produccion-programa-consumidores-hipervulnerables
- **Portal de origen del Ministerio:** https://datos.produccion.gob.ar/dataset/programa-consumidores-hipervulnerables
- **Enlace de descarga directa del CSV:** https://datos.produccion.gob.ar/dataset/f6f32192-8b0c-4a3a-a40f-0e782b4eea46/resource/b84b8029-1026-4710-8bde-ec9d28aff1aa/download/consumidores-hipervulnerables.csv
- **Fecha de descarga:** 15/10/2026
- **Organismo publicador:** Ministerio de Desarrollo Productivo, Dirección Nacional de Defensa del Consumidor y Arbitraje
  del Consumo. Datos de las denuncias de consumidores en la Ventanilla Única Federal de Consumo; el organismo
  detecta qué consumidores son hipervulnerables (Resolución 139/2020).
- **Licencia:** Creative Commons Attribution 4.0 (CC BY 4.0), según la ficha del dataset.
- **Última actualización de los datos (según la ficha):** 7 de febrero de 2023.
- **Archivo en este repositorio:** `data/raw/consumidores-hipervulnerables.csv` (sin modificaciones).
- **Contenido:** 6.457 reclamos y 8 columnas, sin valores faltantes. Reclamos tratados entre enero de 2021 y
  diciembre de 2022.

Marco normativo: Resolución 139/2020 de la Secretaría de Comercio Interior (atención prioritaria de reclamos de
consumidores hipervulnerables).

### Variable objetivo

`rubro_agrupado`: rubro del bien o servicio reclamado. Los rubros con al menos 100 reclamos son una clase propia y
el resto se agrupa en `Otros`. Valores posibles (11):

| Valor | Reclamos |
|---|---|
| Servicios financieros y seguros | 1.788 |
| Servicios de comunicaciones | 1.390 |
| Otros (37 rubros con menos de 100 reclamos cada uno) | 775 |
| Servicios de Salud | 740 |
| Servicios públicos domiciliarios | 621 |
| Electrodomésticos y artefactos para el hogar | 308 |
| Servicios turísticos | 245 |
| Rodados automotores y embarcaciones | 192 |
| Servicio de administración de pagos | 147 |
| Servicios de transporte aéreo | 141 |
| Equipos de telefonía | 110 |

### Variables

| Variable | Tipo | Descripción (inferida; la ficha solo trae nombres y tipos) | Rol |
|---|---|---|---|
| `rubro` | categórica | Rubro del bien o servicio reclamado | Variable a predecir (agrupada) |
| `vulnerabilidad` | categórica | Tipo de vulnerabilidad registrada | Predictora |
| `edad` | numérica | Edad de la persona | Predictora |
| `genero` | categórica | Género registrado | Predictora |
| `provincia_consumidor` | categórica | Provincia del consumidor | Predictora |
| `motivo` | categórica | Motivo del reclamo | No se usa: puede revelar el rubro |
| `mes_anio_tratamiento` | texto | Mes y año de tratamiento del reclamo | No se usa en el escenario principal |
| `provincia_id` | código | Código de la provincia | No se usa: duplica a `provincia_consumidor` |

### Preprocesamiento (resumen)

Normalización de formato, agrupación de rubros, partición estratificada 75/25, codificación one-hot y escalado de
`edad`. Los datos listos para modelar quedan en `data/processed/` (39 columnas predictoras; 4.842 filas de
entrenamiento y 1.615 de prueba). El detalle está en el notebook de preprocesamiento y en `docs/`.

## Documentación

- [`docs/01_descripcion_dataset.md`](docs/01_descripcion_dataset.md): descripción y origen del dataset.
- [`docs/02_decisiones_metodologicas.md`](docs/02_decisiones_metodologicas.md): decisiones de diseño y de
  preprocesamiento, con su justificación.
- [`notebooks/1.0-dm-eda-y-preprocesamiento.ipynb`](notebooks/1.0-dm-eda-y-preprocesamiento.ipynb): carga,
  exploración (EDA) y preprocesamiento.

## Estado del proyecto

Completados: descripción del dataset, exploración y preprocesamiento. Pendiente: entrenamiento y evaluación de
modelos, modelo de referencia, métricas por clase y conclusiones.

## Organización del repositorio

Basada en la plantilla [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/).

```
├── Makefile           <- Comandos de conveniencia (plantilla)
├── README.md
├── data
│   ├── external       <- Datos de terceros
│   ├── interim        <- Dataset normalizado (generado por el notebook)
│   ├── processed      <- Conjuntos de entrenamiento y prueba ya preprocesados
│   └── raw            <- Dataset original, sin modificar
├── docs               <- Descripción del dataset y decisiones metodológicas (Markdown)
├── models             <- Modelos entrenados (etapa de modelado)
├── notebooks          <- 1.0-dm-eda-y-preprocesamiento.ipynb
├── pyproject.toml
├── references         <- Materiales de referencia
├── reports
│   └── figures        <- Gráficos generados por el notebook
├── requirements.txt
└── consumidores_hipervulnerables   <- Código fuente
    ├── __init__.py
    ├── config.py      <- Rutas y configuración (plantilla)
    ├── dataset.py     <- Carga, normalización y agrupación de rubros
    ├── features.py    <- (plantilla, sin uso por ahora)
    ├── plots.py       <- (plantilla, sin uso por ahora)
    └── modeling
        ├── predict.py <- (plantilla, etapa de modelado)
        └── train.py   <- (plantilla, etapa de modelado)
```

## Cómo reproducir

```bash
pip install -r requirements.txt
cd notebooks
jupyter nbconvert --to notebook --execute 1.0-dm-eda-y-preprocesamiento.ipynb
```

El notebook se ejecutó de principio a fin con Python 3, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1,
matplotlib 3.11.2 y scikit-learn 1.9.1. Con otras versiones los resultados descriptivos deberían ser iguales.

La plantilla original indicaba `requires-python = "~=3.10.0"`; se cambió a `>=3.10` para poder instalar el
paquete con versiones más nuevas de Python.
