# Descripción del dataset – Consumidores hipervulnerables

Los números de este documento salen del notebook
[`notebooks/1.0-dm-eda-y-preprocesamiento.ipynb`](../notebooks/1.0-dm-eda-y-preprocesamiento.ipynb)
y se pueden reproducir con él.

## 1. Origen

| Dato | Valor |
|---|---|
| Fuente | Datos Argentina, Ministerio de Desarrollo Productivo. Programa Consumidores Hipervulnerables |
| Ficha del dataset | https://datos.gob.ar/dataset/produccion-programa-consumidores-hipervulnerables |
| Portal de origen | https://datos.produccion.gob.ar/dataset/programa-consumidores-hipervulnerables |
| Enlace de descarga directa | https://datos.produccion.gob.ar/dataset/f6f32192-8b0c-4a3a-a40f-0e782b4eea46/resource/b84b8029-1026-4710-8bde-ec9d28aff1aa/download/consumidores-hipervulnerables.csv |
| Fecha de descarga | 15/10/2026 |
| Licencia | Creative Commons Attribution 4.0 (CC BY 4.0), según la ficha del dataset |
| Última actualización de los datos | 7 de febrero de 2023 (según la ficha) |
| Archivo | `data/raw/consumidores-hipervulnerables.csv` (sin modificaciones) |
| Organismo publicador | Ministerio de Desarrollo Productivo. Secretaría de Comercio Interior. Subsecretaría de Acciones para la Defensa de las y los Consumidores. Dirección Nacional de Defensa del Consumidor y Arbitraje del Consumo |
| Contacto del organismo | dnmejoradelagestion@produccion.gob.ar |
| Fecha de publicación | 9 de mayo de 2021 |
| Frecuencia de actualización declarada | Mensual (el recurso figura modificado por última vez el 7 de febrero de 2023 y los datos llegan hasta diciembre de 2022) |

### Proceso de recopilación (según la ficha)

La ficha describe los datos como «correspondientes a las denuncias que realizan las y los consumidores en la
Ventanilla Única Federal de Consumo y que la Dirección Nacional de Defensa del Consumidor y Arbitraje del
Consumo detecta como consumidores hipervulnerables debido a su condición, de acuerdo a lo dispuesto por la
Resolución N° 139/2020». Es decir: los datos provienen de denuncias presentadas por consumidores y la condición
de hipervulnerabilidad es **detectada por el organismo**, no declarada por quien denuncia. La ficha no detalla
cómo se carga cada denuncia, quién asigna el rubro y el motivo, ni con qué criterio se asigna la vulnerabilidad.
En este trabajo se usa «reclamo» como equivalente de «denuncia».

### Proceso de adquisición (por el autor)

El archivo CSV se descargó desde la ficha del dataset en Datos Argentina el 15/10/2026.

**Contexto normativo.** La Resolución 139/2020 de la Secretaría de Comercio Interior establece una atención
prioritaria y especializada para los reclamos de consumidores hipervulnerables presentados ante el COPREC, el
SNAC y la Ventanilla Federal Única de Reclamos de Defensa del Consumidor. Define como hipervulnerables a
personas que, por su edad, género, estado físico o mental, o por circunstancias sociales, económicas, étnicas o
culturales, tienen dificultades especiales para ejercer sus derechos como consumidoras.

**Verificación.** Los datos de licencia, organismo, fechas y descripción se tomaron de la ficha del dataset. La
descripción de la ficha menciona también el «proveedor denunciado», pero el archivo descargado no incluye esa
columna (solo tiene las 8 columnas descritas abajo).

## 2. Descripción general

- **Instancias:** 6.457 (cada fila es un reclamo registrado).
- **Características:** 8 columnas originales. Al normalizar se agregan `mes` y `anio` (derivadas de
  `mes_anio_tratamiento`) y, para el análisis, `rubro_agrupado`.
- **Formato:** CSV, codificación latin-1, separador coma.
- **Período:** reclamos tratados entre enero de 2021 y diciembre de 2022 (24 meses).
- **Valores faltantes:** ninguno en ninguna columna.
- **Diccionario de datos:** la ficha del dataset incluye uno mínimo, con el nombre y el tipo de cada columna (`text` o
  `numeric`) pero sin descripciones; los significados de abajo se infieren del nombre y del contenido. La ficha
  muestra además una columna `_id` (número de fila de la tabla en el portal) que no viene en el CSV descargado.

## Unidad de observación y variable objetivo

- **Cada fila es un reclamo** de un consumidor registrado por el programa, con el rubro reclamado, el motivo, el
  perfil de la persona (vulnerabilidad, edad, género, provincia) y el mes de tratamiento. No hay identificador de
  reclamo ni de persona, por lo que no se puede saber si dos filas iguales son el mismo reclamo.
- **Tipo de problema:** clasificación multiclase (multinomial).
- **Variable objetivo:** `rubro_agrupado`, derivada de `rubro`. Indica el rubro del bien o servicio reclamado.
  Valores posibles (11): Servicios financieros y seguros; Servicios de comunicaciones; Servicios de Salud;
  Servicios públicos domiciliarios; Electrodomésticos y artefactos para el hogar; Servicios turísticos; Rodados
  automotores y embarcaciones; Servicio de administración de pagos; Servicios de transporte aéreo; Equipos de
  telefonía; y `Otros` (los 37 rubros restantes, cada uno con menos del 1,5 % del entrenamiento).
- **Columnas que no son predictoras:** `rubro` (es lo que se predice), `motivo`, `mes_anio_tratamiento` (con `mes` y
  `anio`) y `provincia_id`. Los motivos de cada exclusión están en `02_decisiones_metodologicas.md`.

## 3. Diccionario de datos

| Variable | Tipo | Valores | Descripción (inferida) |
|---|---|---|---|
| `rubro` | categórica | 47 categorías (48 antes de normalizar) | Rubro del bien o servicio reclamado. Candidata a variable objetivo. |
| `motivo` | categórica | 49 categorías | Motivo del reclamo. |
| `vulnerabilidad` | categórica | 13 categorías (14 antes de normalizar) | Tipo de vulnerabilidad registrada. |
| `mes_año_tratamiento` | texto | 24 valores (ene-21 a dic-22) | Mes y año en que se trató el reclamo. |
| `edad` | numérica entera | 14 a 103; media 60,0; mediana 65 | Edad de la persona. Qué persona (quien reclama o la afectada) no está documentado. |
| `genero` | categórica | Femenino (3.910), Masculino (2.544), No Binario (3) | Género registrado. |
| `provincia_consumidor` | categórica | 24 jurisdicciones | Provincia del consumidor. |
| `provincia_id` | entera (código) | códigos de provincia | Código asociado a la provincia. |

## 4. Distribuciones principales

- **Rubro (47 categorías):** «Servicios financieros y seguros» es el más frecuente (1.788; 27,7 %); los cuatro
  principales suman 70,3 %. 27 rubros tienen menos de 30 casos y 15 tienen menos de 10.
- **Vulnerabilidad:** «Adulto/a mayor» 52,8 % (3.410), «Socio-económica» 19,2 %, «Discapacidad» 10,0 %,
  «Salud» 8,8 %, «NNyA» 4,5 %; el resto son categorías con muy pocos casos (por ejemplo, «Ex-combatiente»: 2;
  «Pueblos originarios»: 5).
- **Provincia:** CABA (3.496) y Buenos Aires (1.386) concentran el 75,6 % de los registros. Córdoba tiene 400.
- **Mes de tratamiento:** entre 105 y 426 reclamos por mes.

## 5. Calidad de los datos

| Problema | Detalle | Tratamiento |
|---|---|---|
| Restos de separador | El encabezado de la última columna es `provincia_id;;;` y cada valor termina en `;;;` | Se limpia al normalizar. El archivo crudo no se toca |
| Espacios sobrantes | «Equipos de telefonía» aparecía como dos categorías (por un espacio) | Se normaliza: 48 → 47 rubros |
| Categorías duplicadas | «Adulto/a Mayor» y «Adulto/a mayor» | Se unifican: 14 → 13 categorías |
| Registros repetidos | 173 filas idénticas a otra; 336 filas involucradas; 163 grupos distintos | **No se eliminan**: no hay identificador de reclamo |
| Edad y vulnerabilidad | 252 de 291 registros «NNyA» tienen edad ≥ 18; 412 de 3.410 «Adulto/a mayor» tienen edad < 60; 50 registros tienen edad < 18 | Se informa; no se corrige. Una hipótesis es que `edad` sea la de quien reclama, pero no se puede confirmar |
| Categorías con muy pocos casos | 15 rubros con menos de 10 casos | Agrupación documentada en `02_decisiones_metodologicas.md` |
| Columna redundante | `provincia_id` equivale uno a uno a `provincia_consumidor` | Se descarta como predictora |

## 6. Dataset procesado para el modelado

El notebook de preprocesamiento deja en `data/processed/` los conjuntos de entrenamiento (4.842 reclamos) y prueba
(1.615) ya transformados, para dos escenarios de variables predictoras: **A** (41 columnas: `vulnerabilidad`, `genero`
y `provincia_consumidor` codificadas en 0/1 y `edad` estandarizada) y **B** (28 columnas: igual, sin
`vulnerabilidad`). La variable a predecir es `rubro_agrupado` (10 rubros que representan al menos 1,5 % del
entrenamiento + `Otros`). Los preprocesadores ajustados están en `models/`. El detalle y la justificación están en
`02_decisiones_metodologicas.md`.

## 7. Alcance y limitaciones de interpretación

- Los datos son **reclamos registrados** de consumidores incluidos en el programa, entre 2021 y 2022. No
  representan a toda la población ni al período actual.
- No hay información de quienes no reclamaron ni de cuántas personas de cada grupo consumen cada servicio. Los
  análisis muestran **asociaciones dentro de los reclamos observados**; no miden exposición ni «grupos más
  afectados».
- Hay una fuerte concentración geográfica (CABA y Buenos Aires), por lo que las diferencias por provincia se apoyan
  en pocos casos en la mayoría de las jurisdicciones.
- Varias categorías de vulnerabilidad tienen muy pocos casos y no permiten conclusiones propias.

## 8. Preguntas abiertas para confirmar con la fuente

1. ¿`edad` corresponde a la persona que reclama o a la persona afectada?
2. ¿`mes_año_tratamiento` es la fecha de ingreso del reclamo o la fecha en que se trató? (define si se puede usar
   para clasificar un reclamo al ingresarlo).
3. ¿El motivo se elige después de asignar el rubro? (define si revela la respuesta).
4. La ficha indica que el organismo detecta la vulnerabilidad: ¿con qué criterio concreto? ¿Un reclamo puede tener más de una?

Estas preguntas se consultan al contacto del organismo esperando una pronta respuesta.