# FestivalOps · inicio

Empieza por [el contexto del alumnado](docs/CONTEXTO_ALUMNADO.md). Para preparar la explicación y el recorrido en pantalla, consulta [el guion de contexto docente](docs/GUIA_DOCENTE_CONTEXTO.md).

`python demo.py` o `python demo.py contexto` presenta el proyecto sin ejecutar incidencias. Cada caso explica su situación y su relación con la pantalla. La búsqueda por nombre de escenario reproduce D01 con la misma función que la demo; es independiente del selector del panel.

Estado: D01-D08 y P01-P04 pendientes. Copia preparada del proyecto educativo FestivalOps.
Python 3.10 o posterior. Núcleo, demos y tests: biblioteca estándar, sin instalación.

Desde esta carpeta:
```
python -m unittest tests.test_smoke -v
python demo.py D01
python -m unittest tests.test_casos.D01 -v
python -m unittest discover -v
```
La última orden falla mientras queden casos pendientes. demo.py es una observación,
no un veredicto automático. Trabaja en el caso encargado, conservando los tests y el SQL.

Vista opcional, ensayada con Python 3.14.2 y Streamlit 1.63.0:
```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
No necesitas la vista para los ejercicios. La preparación de paquetes se realiza antes de clase.
La base local se crea desde data/source/festival.sql; los tests usan bases efímeras.
Consulta el PDF del alumnado para síntomas y criterios. Abre esta carpeta como proyecto
en Codex y conserva otra copia sin editar para reiniciar tu trabajo si lo necesitas.
