# Decisiones metodológicas y de preprocesamiento

Decisiones de diseño del problema y de preparación de los datos, con su justificación y la evidencia del dataset.
Los números salen del notebook
[`1.0-dm-eda-y-preprocesamiento.ipynb`](../notebooks/1.0-dm-eda-y-preprocesamiento.ipynb) (las secciones se indican
entre paréntesis). Los resultados de los modelos están en [`03_modelado_y_resultados.md`](03_modelado_y_resultados.md).

## 1. Qué se puede afirmar con estos datos

**Decisión.** Los resultados se formulan como **asociaciones dentro de los reclamos registrados** entre enero de 2021
y diciembre de 2022. No se afirma que un grupo esté «más expuesto» o «más afectado», ni se atribuyen causas.

**Por qué.** El dataset solo contiene personas que reclamaron. No hay información de quienes no reclamaron ni de
cuántas personas de cada grupo consumen cada servicio.

**Hipótesis** Cuando se observa un patrón (por ejemplo, que entre los reclamos de «Salud»
predomina el rubro Servicios de Salud), las explicaciones posibles se plantean como hipótesis a confirmar con
información adicional, no como hechos. Esto se aplica a todo el trabajo (sección 9).

## 2. Uso previsto y momento de la predicción

**Uso previsto (supuesto):** clasificar un reclamo **cuando se ingresa**, con el perfil de la persona y antes de
conocer su rubro. El supuesto no está confirmado: el diccionario de la ficha solo da nombre y tipo de cada columna y
no explica cuándo ni cómo se registra cada dato. Una **hipótesis** sobre la utilidad del modelo es que anticipar el
rubro podría ayudar a orientar o derivar el reclamo; con estos datos no se puede comprobar.

**Qué variables se pueden usar** depende de si estarán disponibles en ese momento (sección 12):

| Variable | Decisión | Motivo |
|---|---|---|
| `edad`, `genero`, `provincia_consumidor` | Se usan | Datos de la persona; se supone que están al ingresar el reclamo |
| `vulnerabilidad` | **Dos escenarios** (A con ella, B sin ella) | Disponibilidad **no confirmada** (ver 2.1) |
| `motivo` | No se usa | Puede no estar disponible o revelar el rubro |
| `mes_anio_tratamiento` | No se usa como predictora | Es fecha de *tratamiento*, no necesariamente de ingreso |
| `provincia_id` | No se usa | Equivale uno a uno a `provincia_consumidor` |

Las exclusiones son **por disponibilidad o por redundancia exacta**. Ninguna variable se excluye por tener una
asociación baja con el rubro: una asociación individual baja no demuestra que la variable sea inútil combinada con
otras. Si hubiera que decidir por capacidad predictiva, se hace **dentro del entrenamiento** (validación cruzada), no
con el conjunto completo.

### 2.1 La vulnerabilidad

La ficha del dataset indica que el organismo **detecta** la condición de vulnerabilidad, sin aclarar cuándo ni cómo.
Categorías como «Salud» o «Turista» podrían asignarse a partir de la situación que originó el reclamo. Si la
vulnerabilidad se determina **después** de analizar o clasificar el reclamo, usarla como predictora introduciría
información que no existiría en el momento de la predicción.

Que la vulnerabilidad esté asociada con el rubro **no demuestra** que haya fuga de información; lo que falta es
confirmar cuándo se registra. Mientras tanto:
- **Escenario A** (con vulnerabilidad): se presenta como **condicionado** a que esté disponible al ingresar el reclamo.
- **Escenario B** (sin vulnerabilidad): no depende de ese supuesto y se presenta como comparación.
- Se informan los dos, sin elegir uno por su rendimiento. Para confirmar el momento de registro hay que consultar al
  organismo (contacto en [`01_descripcion_dataset.md`](01_descripcion_dataset.md)).

## 3. Partición entrenamiento / prueba

**Decisión.** Partición **aleatoria estratificada por rubro**, 75 % entrenamiento (4.842 reclamos) y 25 % prueba
(1.615), semilla 42 (sección 6).

**Qué evalúa.** Una partición aleatoria sirve para evaluar el modelo con reclamos de una distribución parecida a la de
la muestra histórica. **No comprueba** que el modelo generalice a reclamos de períodos posteriores: un modelo puede
aplicarse a reclamos futuros aunque no incluya el tiempo entre sus predictoras.

**Evaluación temporal complementaria.** Se entrena con los reclamos de 2021 y se evalúa con los de 2022. Tiene una
limitación propia: la fecha del dataset es la de *tratamiento* y no necesariamente la de ingreso, por lo que es una
aproximación a la generalización hacia el futuro.

**Dependencia entre reclamos.** Se asume que los reclamos son observaciones independientes, algo que no se puede
verificar (no hay identificador de persona ni de reclamo). Ver el punto 5.

## 4. Definición de las clases de rubro

**Decisión.** La lista de rubros que se conservan como clase propia se calcula **solo con el conjunto de
entrenamiento** y se mantiene fija al evaluar. Se conserva todo rubro que represente al menos el **1,5 %** de los
reclamos de entrenamiento (unos 73); el resto se agrupa en `Otros`. Un rubro de prueba que no esté en la lista pasa a
`Otros` (sección 7).

**Por qué este cambio.** Calcular la lista con todo el dataset hacía intervenir las etiquetas de prueba en la
definición del problema, aunque se hubiera fijado «antes de entrenar».

**Resultado.** 10 clases propias más `Otros` (11 clases): Servicios financieros y seguros, Servicios de
comunicaciones, Servicios de Salud, Servicios públicos domiciliarios, Electrodomésticos y artefactos para el hogar,
Servicios turísticos, Rodados automotores y embarcaciones, Servicio de administración de pagos, Servicios de
transporte aéreo y Equipos de telefonía. La clase propia más chica tiene 82 casos de entrenamiento y 28 de prueba.
En entrenamiento, `Otros` reúne 12,0 % de los reclamos.

**Agrupar cambia el problema.** Con `Otros` ya no se clasifica entre todos los rubros, sino entre los más frecuentes
y «cualquier otro». El 1,5 % es una regla práctica de tamaño mínimo de muestra (con validación cruzada de 5
particiones, una clase de ese tamaño deja unos 15 casos para validar en cada una), no una fuente oficial.

**Otros umbrales.** Comparar 1 %, 1,5 % y 2 % **modifica las clases**: con más clases propias la tarea es más difícil
y con menos se simplifica. Una mejora de métricas entre umbrales no significa que el modelo haya mejorado. Por eso cada
variante se compara con **su propio modelo de referencia** y se informa la ganancia sobre esa referencia.

**Qué se pierde.** `Otros` es heterogénea (37 rubros con pocos casos cada uno); su resultado no se interpreta como un
rubro concreto.

## 5. Repeticiones de filas

**Hecho.** 173 filas son idénticas a otra (336 filas en grupos repetidos). Podrían ser reclamos distintos con el mismo
perfil, así que **no se eliminan** automáticamente (sección 4).

**Alcance entre conjuntos.** Con la partición aleatoria, **64 reclamos de prueba (4,0 %)** tienen una fila completa
idéntica en entrenamiento, repartidas en 61 grupos (sección 6). El modelo podría «reconocerlas» y el resultado verse
algo mejor de lo real.

**Análisis de sensibilidad.** Se repite la evaluación manteniendo juntas las filas idénticas al separar. Esto **no
identifica personas** ni resuelve toda posible dependencia, y no se asume que dos reclamos con el mismo perfil
pertenezcan a la misma persona.

## 6. El motivo del reclamo

**Evidencia** (solo entrenamiento, sección 11): 24 de los 47 motivos aparecen siempre con un único rubro (cubren
16,9 % de los reclamos); por ejemplo, «Cancelación o supresión de vuelos» (solo transporte aéreo). Otros son
genéricos y aparecen en muchos rubros. La pureza ponderada es 0,498: conociendo el motivo, el rubro más frecuente de
ese motivo acierta en cerca de la mitad de los reclamos.

**Decisión.** El análisis principal **no usa el motivo**, por disponibilidad y posible fuga de información. Si se
incluyera, sería un escenario complementario que responde a otra pregunta (clasificar el rubro a partir del motivo y el
perfil).

## 7. Preprocesamiento

Todo está en la sección 13 del notebook 1.0, con comentarios en cada paso. El código reutilizable está en
`consumidores_hipervulnerables/features.py`.

| Paso | Qué se hace | Por qué |
|---|---|---|
| Codificación | One-hot de `vulnerabilidad` (solo escenario A), `genero` y `provincia_consumidor`; categorías con menos de 5 casos se agrupan como «infrecuente» | Los modelos necesitan números; evita columnas casi vacías |
| Escalado | Estandarización de `edad` | Poner la edad en una escala comparable con las columnas 0/1; importa para K-NN |
| Ajuste | Se ajusta solo con el entrenamiento y se aplica a la prueba | Evitar que la prueba influya en el preprocesamiento |

**El escalado no sirve para eliminar redundancia ni correlación entre variables**; solo lleva las variables a una escala
común.

**Cómo se conserva el procedimiento.**
- El **preprocesador ajustado** se guarda con `joblib` en `models/` (`preprocesador_escenario_A.joblib` y
  `preprocesador_escenario_B.joblib`) para transformar reclamos nuevos de la misma manera.
- Para la validación cruzada, el preprocesador va **dentro de un `Pipeline`**: en cada partición se vuelve a ajustar solo
  con los datos de entrenamiento de esa partición. Usar una matriz ya transformada con todo el entrenamiento haría que
  las categorías y el escalado conocieran los datos de validación.
- Los CSV de `data/processed/` (`X_train_A/B`, `X_test_A/B`, `y_train`, `y_test`) sirven para inspeccionar el resultado
  de la transformación, pero **no se usan para validar**.
- Los archivos `.joblib` dependen de la versión de scikit-learn (1.9.1 en este trabajo).

Resultado: escenario A, 41 columnas; escenario B, 28 columnas; sin valores faltantes.

## 8. Modelo de referencia y desbalance

**Modelo de referencia.** Predecir siempre la clase mayoritaria **del entrenamiento** («Servicios financieros y
seguros») y evaluarla en la prueba con **las mismas métricas** que los modelos. Superar la exactitud no basta: un
modelo puede acertar más en total sin identificar mejor las clases minoritarias, por eso se evalúa con F1 macro,
exactitud balanceada y métricas por clase.

**`class_weight` y K-NN.**
- Regresión Logística y Árbol de Decisión admiten `class_weight` (por ejemplo, `"balanced"`).
- `KNeighborsClassifier` no tiene `class_weight`. Su parámetro `weights` (`"uniform"` o `"distance"`) solo pondera el
  voto de los vecinos y **no equivale** a ponderar clases. K-NN se evalúa sin ponderación de clases.

## 9. Otros límites conocidos

- Hay una fuerte concentración geográfica (CABA y Buenos Aires: 75,6 % de los reclamos); en la mayoría de las
  provincias hay pocos casos.
- `edad` puede corresponder a quien reclama y no a la persona afectada (hipótesis; no se puede confirmar).
- Los datos cubren solo 2021-2022.
