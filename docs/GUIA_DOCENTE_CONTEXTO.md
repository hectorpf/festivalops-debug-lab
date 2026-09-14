# Preparar y explicar el inicio de FestivalOps

Este guion acompaña la guía de ejercicios y añade el contexto previo. Ensaya desde el clon actualizado, con las dependencias instaladas. Conserva una copia inicial y trabaja en una rama de ensayo para poder revisar tus cambios. Este repositorio es el estado inicio: no contiene las copias practica y solucion del kit docente.

## Apertura de clase sugerida de 15 a 20 minutos

1. **Encargo, 2 minutos.** Di: «Recibimos una aplicación de consulta de un festival. Vamos a entender qué hace y comprobar cambios concretos con ayuda de IA. Los datos son inventados y los errores están preparados para el taller». Pregunta qué necesitaría consultar la organización.
2. **Producto, 4 minutos.** Abre Streamlit y recorre actuaciones, ventas, ingresos, ocupación e incidencias. Explica que no hay venta ni edición de datos. La ocupación usa entradas vendidas, no acceso real. Distingue la búsqueda superior del selector inferior; no vacíes todavía este último, porque activa D06.
3. **Datos y mapa, 4 minutos.** Abre el SQL y muestra una actuación enlazada con escenario, artista y ventas. Enseña app.py, src/festivalops, demo.py y tests. Di: «Pantalla, funciones, datos y comprobaciones son piezas distintas del mismo trabajo». No leas todas las funciones ni anticipes las soluciones.
4. **Herramientas de observación, 3 minutos.** Ejecuta `python demo.py contexto` y la prueba de humo. Explica observado frente a esperado y demo frente a prueba. El humo comprueba SQLite; no certifica la pantalla.
5. **Primera incidencia, 3–7 minutos.** Sigue el recorrido D01 siguiente. Deja que el grupo formule la expectativa antes del prompt.

## D01 desde la pantalla hasta el código

Di: «Queremos buscar las actuaciones del Escenario Principal por su nombre. ¿Un espacio accidental al copiarlo debería cambiar lo que encontramos?».

En la búsqueda superior introduce `Escenario Principal`: en el estado inicial aparecen tres actuaciones. Introduce ` Escenario Principal `: aparecen cero. La pantalla informa que no encontró actuaciones; el panel inferior mantiene su selección porque es independiente. Conserva ambos resultados antes de abrir el código.

Di: «Ahora reproducimos la misma comparación con dos actuaciones pequeñas. Reducimos los datos para seguir el recorrido». Ejecuta `python demo.py D01`. Debe encontrar Luz de Barrio con el nombre sin espacios y ninguna actuación con los espacios. El ejemplo no consulta SQLite: la pantalla sí lo hace. Ambas llaman a filter_by_stage y después a normalize_stage.

El grupo debe explicar qué entrada cambió y qué salida esperaba. Solo entonces utiliza este prompt:

```text
En la búsqueda por nombre de la pantalla, 'Escenario Principal' devuelve tres actuaciones y ' Escenario Principal ' devuelve cero. Esperamos las mismas actuaciones. Ejecuta python demo.py D01 y sigue el recorrido desde app.py por filter_by_stage y normalize_stage. Explica por qué la demo usa menos datos que la pantalla. No edites aún: distingue resultados ejecutados de hipótesis y propón una comprobación que permita contrastarlas.
```

Ejecuta `python -m unittest tests.test_casos.D01 -v`. Explica que el primer fallo detiene ese método; sus otras comprobaciones aún no han pasado. Antes de reparar acuerda espacios exteriores y mayúsculas equivalentes, otros escenarios distintos y conservación de la lista.

Cuando corresponda la reparación, solicita únicamente D01, conserva datos y pruebas, revisa el diff y repite la demo y el test. Repite también ambas búsquedas en la pantalla: deben devolver las mismas tres actuaciones. No aceptes como prueba visual solo el test de la función. No añadas equivalencias de acentos o búsquedas aproximadas sin otro requisito.

## Qué demos están conectadas a la pantalla

| Caso | Relación real |
| --- | --- |
| D01 | Búsqueda superior → filter_by_stage → normalize_stage. |
| D02 | parse_price aislada; SQL convierte los precios por otro recorrido. |
| D03 | collect_open_incidents aislada; no es el contador de la pantalla. |
| D04 | revenue_by_stage es usada por revenue_for_selection; la demo usa una base mínima. |
| D05 | Misma export_csv que la descarga. |
| D06 | next_event_label y además tratamiento de tabla y gráfico vacíos en app.py. |
| D07 | summarize_prices aislada; no alimenta un indicador visual. |
| D08 | capacity_status alimenta la tabla de ocupación. |
| P01 | sort_for_show aislada; las filas de la pantalla vienen ordenadas por SQL. |
| P02 | occupancy_ratio alimenta el indicador de ocupación. |
| P03 | revenue_for_selection alimenta el informe por escenarios. |
| P04 | incident_counts alimenta los recuentos; contar consultas no mide velocidad. |

## Preparación y límites

Ejecuta la suite antes del ensayo y registra los fallos pendientes. El estado inicial conserva defectos intencionados. Las mejoras del material no deben repararlos por accidente. Tras cada reparación exige evidencia acotada; algunos casos tienen varias pruebas.

Para práctica autónoma usa el estado practica del kit, con las D resueltas, o una copia de trabajo donde hayas comprobado esas correcciones. No entregues solucion como punto de partida. Este guion se guarda junto al código y es visible a quien tenga el repositorio: no es documentación privada ni incluye los parches de solución.

Si una demo muestra una excepción, explica la traza y ejecuta el test específico; demo.py la captura y no ofrece un veredicto de éxito. D03 limpia el acumulador inicial únicamente para aislar el experimento; las dos llamadas observadas comparten proceso. D04 reutiliza tiny_revenue de las pruebas para mantener los mismos datos pequeños. Estos son apoyos de taller, no funcionalidades del producto.
