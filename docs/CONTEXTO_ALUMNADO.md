# Entender FestivalOps antes de investigar

Recibes una aplicación en desarrollo para consultar un festival imaginario. Tu encargo es entender cómo trabaja, reproducir un comportamiento incorrecto, pedir ayuda a la IA y comprobar una corrección pequeña. Los defectos son deliberados: no debes resolverlos todos de una vez.

## Qué puedes hacer

Consultar actuaciones, escenarios, entradas vendidas, ingresos, ocupación calculada e incidencias; seleccionar escenarios, buscar por nombre y descargar actuaciones en CSV. No puedes vender entradas, registrar artistas ni editar incidencias desde la pantalla. La ocupación se calcula con entradas vendidas y aforo; no mide personas presentes en tiempo real. La etiqueta próxima actuación usa la primera fila recibida, no una comparación con el reloj actual.

## De dónde sale la información

SQLite guarda tablas relacionadas en un archivo local; no requiere un servidor. `data/source/festival.sql` contiene la estructura y los datos sintéticos: 3 escenarios, 8 artistas, 8 actuaciones, 10 lotes de ventas y 5 incidencias. Una actuación pertenece a un escenario y un artista, y puede tener varias ventas e incidencias. Una incidencia no añade ingresos.

La aplicación crea la base local a partir del SQL si hace falta. Las pruebas y algunas demos usan bases temporales en memoria. Conserva el SQL original para poder reconstruir los datos.

## Mapa de archivos

| Archivo | Responsabilidad |
| --- | --- |
| `app.py` | Presenta la pantalla y llama a funciones. |
| `src/festivalops/database.py` | Abre o prepara SQLite. |
| `src/festivalops/metrics.py` | Consultas, ingresos, aforo y recuentos. |
| `src/festivalops/filters.py` | Prepara nombres y busca actuaciones. |
| `src/festivalops/schedule.py` | Ordena fechas en el ejercicio aislado. |
| `src/festivalops/exports.py` | Produce el CSV descargable. |
| `demo.py` | Prepara entradas pequeñas y muestra lo observado. |
| `tests/test_casos.py` | Comprueba requisitos de D01–D08 y P01–P04. |

## Primer recorrido

Con el entorno Python preparado, desde la raíz del proyecto:

```powershell
python demo.py contexto
python -m unittest tests.test_smoke -v
python -m streamlit run app.py
```

La prueba de humo comprueba la base, no que toda la interfaz funcione correctamente. Para la vista necesitas las dependencias de `requirements.txt`, instaladas antes del taller.

En la búsqueda superior escribe `Escenario Principal` y después ` Escenario Principal `, con un espacio a cada lado. Deberían encontrarse las mismas actuaciones. Esta búsqueda es independiente del selector inferior: ambos controles tienen recorridos distintos y sus resultados están separados.

Antes de investigar, anota entrada, resultado y resultado esperado. Después ejecuta:

```powershell
python demo.py D01
python -m unittest tests.test_casos.D01 -v
```

La pantalla utiliza los datos completos. D01 usa dos actuaciones pequeñas para llamar a la misma función `filter_by_stage`, que a su vez llama a `normalize_stage`. Por eso las cantidades difieren entre pantalla y demo, pero la equivalencia que esperamos es la misma.

## Cómo leer una demo

`python` ejecuta el archivo; `demo.py` prepara el experimento; `D01` selecciona el caso. Sin argumento se muestra el contexto. `resumen` ejecuta todos los casos: resérvalo para después del recorrido inicial.

Observado se calcula con el código actual. Esperado es un requisito escrito por quien preparó el ejemplo: debe discutirse, no tomarse como una medición. La demo imprime información; las pruebas comparan resultados. Una demo puede mostrar una excepción y terminar normalmente porque la captura para poder explicarla. Su código de salida no demuestra que el caso esté resuelto.

D01–D08 son demostraciones guiadas; P01–P04 son práctica; P05 consiste en crear una actividad para tus alumnos y no tiene comando en demo.py. No todas las funciones están conectadas a la pantalla: cada demo indica su alcance.

Investiga un caso, formula una hipótesis, comprueba una predicción, revisa un cambio acotado y repite la misma prueba. Una prueba puede detenerse en su primera comparación fallida; no significa que haya comprobado todas las líneas posteriores. Un caso verde tampoco convierte en verde el proyecto entero.
