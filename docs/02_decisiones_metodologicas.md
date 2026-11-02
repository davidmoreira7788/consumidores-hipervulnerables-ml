# Decisiones metodológicas y de preprocesamiento

Decisiones de diseño y de preprocesamiento, con su justificación, la evidencia del dataset y dónde verla. Los
números salen del notebook
[`1.0-dm-eda-y-preprocesamiento.ipynb`](../notebooks/1.0-dm-eda-y-preprocesamiento.ipynb). Hasta acá **no se
entrena ningún modelo**: lo que se justifica es la preparación de los datos.

## 1. Concentración de reclamos ≠ exposición al problema

**Decisión.** Los resultados se formulan como **asociaciones dentro de los reclamos registrados** entre enero de
2021 y diciembre de 2022. No se afirma que un grupo esté «más expuesto» o «más afectado».

**Por qué.** El dataset solo contiene personas que reclamaron. No hay información de quienes no reclamaron ni de
cuántas personas de cada grupo consumen cada servicio.

**Hipótesis.** Cuando se observa un patrón (por ejemplo, que entre los reclamos de «Salud»
predomina el rubro Servicios de Salud), las explicaciones posibles se plantean como hipótesis a confirmar con
información adicional, no como hechos. Esto se aplica a todo el trabajo.

Notebook: sección 9.

## 2. Alcance de la predicción y variables disponibles

**Decisión.** El escenario principal clasifica un reclamo **al momento de ingresarlo** con: `vulnerabilidad`,
`edad`, `genero` y `provincia_consumidor`. **No** usa mes ni año de tratamiento, ni el motivo.

**Por qué.**
- La fecha del dataset es de *tratamiento*; no se sabe si está disponible al ingresar el reclamo.
- La asociación de `mes` y de `anio` con el rubro es baja (V de Cramér 0,071 y 0,109), menor que la de
  `vulnerabilidad` (0,290).
- Se descarta también `provincia_id`, porque equivale uno a uno a `provincia_consumidor`.

**Qué queda para la etapa de modelado.** Comprobar con un modelo si agregar mes y año mejora los resultados, como análisis
de sensibilidad presentado por separado y aclarando que responde a otra pregunta. Hasta entonces la decisión se
apoya en la disponibilidad dudosa y en la asociación baja, no en un resultado de modelo.

Notebook: secciones 9, 10 y 13.

### Momento de la predicción

El modelo se piensa para usarse **cuando se ingresa un reclamo**, con el perfil de la persona y antes de conocer
su rubro. Es un **supuesto**: el diccionario de la ficha no describe las columnas y no se pudo confirmar que esas variables estén
disponibles en ese momento ni cómo se asigna el rubro. Una **hipótesis** sobre su utilidad es que anticipar el
rubro podría ayudar a orientar o derivar el reclamo; con estos datos no se puede comprobar.

Para evaluar el modelo contra la realidad habría que comparar sus predicciones con el rubro finalmente registrado
en reclamos nuevos; este dataset histórico no lo permite, por lo que la evaluación se hará con un conjunto de
prueba separado de los mismos datos.

### ¿El dataset permite responder la pregunta?

Solo en parte. `vulnerabilidad` tiene una asociación moderada con el rubro (V de Cramér 0,290); `genero`,
`provincia_consumidor` y las variables temporales tienen asociaciones más bajas (sección 9 del notebook). Con
solo perfil y territorio es esperable que quede una parte importante sin explicar, porque el rubro depende de lo
que se consumió y no del perfil. Es una limitación que se informa; se verá con el modelo cuánto se puede anticipar.

## 3. Agrupación de rubros

**Criterio (fijado antes de entrenar):** clase propia para todo rubro con **al menos 100 reclamos**; el resto se
agrupa en `Otros`. Usa solo la frecuencia de la etiqueta, no las variables predictoras.

| Umbral | Clases propias | Registros en «Otros» | % en «Otros» | Clase propia más chica |
|---|---|---|---|---|
| 30 | 20 | 258 | 4,0 | 33 |
| 50 | 15 | 451 | 7,0 | 54 |
| **100** | **10 (+ Otros = 11 clases)** | **775** | **12,0** | **110** |
| 150 | 7 | 1.173 | 18,2 | 192 |
| 200 | 6 | 1.365 | 21,1 | 245 |

**Comprobación de casos por clase** (partición estratificada 75/25, semilla 42): mínimo de 82 casos en
entrenamiento y 28 en prueba («Equipos de telefonía»). La estratificación conserva las proporciones pero no
agrega ejemplos: las clases chicas tendrán métricas inestables y se reportan por clase con esa advertencia.

**Agrupar cambia el problema.** Con `Otros` ya no se clasifica entre todos los rubros, sino entre los 10 más
frecuentes y «cualquier otro». El umbral de 100 es una regla práctica de tamaño mínimo de muestra, **fijada antes
de entrenar** y no elegida para mejorar métricas; no proviene de una fuente oficial, y por eso se verifica con
otros umbrales. Toda decisión de este tipo debe quedar justificada con los datos o con una fuente, no con el
resultado del modelo.

**Qué se pierde.** `Otros` reúne 37 rubros distintos y es heterogénea; su resultado no se interpreta como un rubro
concreto. En la etapa de modelado se comparará con los umbrales 50 y 200 como análisis de sensibilidad.

Notebook: secciones 5, 6 y 7.

## 4. Modelo de referencia con la clasificación definitiva

**Decisión.** El 28 % que se mencionó al plantear el proyecto corresponde a los rubros sin agrupar. Con la clasificación
definitiva, el modelo de referencia se define así y **se calculará en la etapa de modelado**:
1. Elegir la clase mayoritaria **con el conjunto de entrenamiento** (hoy: «Servicios financieros y seguros»).
2. Predecir esa clase para todo el conjunto de prueba.
3. Calcular las **mismas métricas** que para los otros modelos (exactitud, exactitud balanceada, F1 macro y
   métricas por clase).

**Dato descriptivo disponible hoy** (no es un modelo): esa clase representa 27,7 % del conjunto de prueba.

Superar la exactitud del modelo de referencia no basta: un modelo puede acertar más en total sin identificar mejor
las clases minoritarias. Por eso se evaluará principalmente con F1 macro, exactitud balanceada y métricas por clase.

Notebook: sección 7.

## 5. Ponderación del desbalance: `class_weight` vs `weights` en K-NN

- **Regresión Logística y Árbol de Decisión:** admiten `class_weight` (por ejemplo, `"balanced"`) para ponderar
  clases.
- **K-NN (`KNeighborsClassifier`):** no tiene `class_weight`. Su parámetro `weights` (`"uniform"` o
  `"distance"`) solo pondera el **voto de los vecinos** (por ejemplo, según su distancia) y **no equivale** a
  ponderar clases.
- **Implementación prevista:** K-NN se evalúa sin ponderación de clases y se reporta su comportamiento en las
  clases minoritarias. Si se prueba un remuestreo para compensar el desbalance, se aplicará **solo al
  conjunto de entrenamiento** (nunca a la prueba) y se describirá aparte. `weights` se presentará como un
  hiperparámetro distinto.
- Verificar la sintaxis y los parámetros en la documentación vigente de scikit-learn antes de implementar.

## 6. El motivo del reclamo

**Evidencia.** En el dataset, 25 de los 49 motivos aparecen siempre con un único rubro (cubren 14,1 % de los
reclamos); por ejemplo, «Cancelación o supresión de vuelos» (solo transporte aéreo) o «Baja de efectores y/o
profesionales de la cartilla de prestaciones médicas» (solo Servicios de Salud). Otros son genéricos: «Prácticas
Abusivas» o «Problemas de fraude o estafa» aparecen en 26 rubros distintos cada uno. La pureza ponderada es 0,495:
en promedio, conociendo el motivo se acierta el rubro más frecuente de ese motivo en cerca de la mitad de los
reclamos. Notebook: sección 11.

**Decisión.** El análisis principal **no usa el motivo**. Si se incluye, será un escenario complementario que
responde a otra pregunta (clasificar el rubro a partir del motivo y el perfil) y se presentará con esta
limitación. Queda pendiente confirmar con la fuente cómo se registra (ver pregunta abierta 3 en el documento 01).

## 7. Preprocesamiento para el modelado

Todo lo que sigue está en la sección 13 del notebook, con comentarios en cada paso.

| Paso | Qué se hace | Por qué |
|---|---|---|
| Partición | 75 % entrenamiento / 25 % prueba, estratificada por rubro agrupado, semilla 42 | Evaluar con datos que el modelo no vio y conservar la proporción de cada clase |
| Codificación | One-hot de `vulnerabilidad`, `genero` y `provincia_consumidor`; categorías con menos de 5 casos en entrenamiento se agrupan como «infrecuente» | Los modelos necesitan números; evita columnas casi vacías |
| Escalado | Estandarización de `edad` (media 0, desvío 1 en entrenamiento) | Poner la edad en una escala comparable con las columnas 0/1; importa para modelos basados en distancias, como K-NN |
| Ajuste | Las transformaciones se ajustan solo con el entrenamiento y se aplican a la prueba | Evitar que la prueba influya en el preprocesamiento |

**Por qué la partición es aleatoria.** El modelo no predice períodos futuros (no usa variables temporales), por lo
que no hace falta una partición cronológica. Se asume que los reclamos son observaciones independientes; no se
puede verificar (no hay identificador de persona ni de reclamo) y, si una misma persona figura más de una vez o hay
filas repetidas entre entrenamiento y prueba, el resultado podría verse algo mejor de lo real. Además, los datos
cubren solo 2021-2022 y no se evalúa con períodos posteriores.

**Aclaración conceptual.** Escalar variables sirve para llevarlas a una escala común; **no** sirve para eliminar
redundancia ni correlación entre variables predictoras. La posible redundancia entre `edad` y `vulnerabilidad`
(por ejemplo, «Adulto/a mayor») se señala como limitación, no se resuelve con el escalado.

**Resultado.** 4.842 filas de entrenamiento y 1.615 de prueba con 39 columnas predictoras, guardadas en
`data/processed/` (`X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`). Sin valores faltantes.

## 8. Registros repetidos

No se eliminan (no hay identificador de reclamo). Se informa cuántos son (173 filas idénticas a otra) y se
interpreta como limitación.


## 9. Próximos pasos

- Entrenar los modelos en un notebook aparte (el de preprocesamiento no incluye modelos) y calcular el modelo de
  referencia con el procedimiento descrito.
- Presentar **un modelo final elegido** y explicar cómo resuelve el problema. Los otros modelos probados
  (Regresión Logística, K-NN, Árbol de Decisión, distintos hiperparámetros) pueden quedar en una sección
  «modelos probados» del notebook, con un comentario sobre por qué se eligió el final.
- Reportar métricas por clase con la advertencia sobre el tamaño de las clases chicas.
- Mostrar una predicción de ejemplo con un reclamo hipotético para ilustrar cómo se usa el modelo.
- Análisis de sensibilidad (umbrales 50 y 200; escenario con información temporal; escenario con motivo).
- Interpretar siempre dentro de la población y el período representados en los datos, y plantear las explicaciones
  como hipótesis.
