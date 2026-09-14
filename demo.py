"""Observa un caso real. La verificación se ejecuta aparte con unittest."""
import csv,io,sys,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
from festivalops.database import memory_database
from festivalops.filters import normalize_stage, filter_by_stage
from festivalops.exports import export_csv
from festivalops.metrics import (parse_price,collect_open_incidents,revenue_by_stage,
    next_event_label,summarize_prices,capacity_status,occupancy_ratio,
    revenue_for_selection,incident_counts)
from festivalops.schedule import sort_for_show
from tests.test_casos import tiny_revenue

# Contexto del experimento, sin anticipar la reparación.
CASES = {
    'D01': ('Buscar actuaciones por nombre', 'Comparamos dos formas de escribir el mismo escenario.', 'filters.py: filter_by_stage -> normalize_stage. Misma búsqueda por texto que la pantalla; el selector inferior es independiente.'),
    'D02': ('Interpretar un precio', 'Una entrada cuesta 19,90 euros. Queremos obtener un número.', 'metrics.py: parse_price. Ejemplo aislado; las consultas SQL convierten precios por su cuenta.'),
    'D03': ('Consultar incidencias abiertas', 'Repetimos la consulta con los mismos datos: esperamos la misma respuesta.', 'metrics.py: collect_open_incidents. Ejemplo aislado, no es el contador de la pantalla.'),
    'D04': ('Revisar ingresos', 'Dos entradas de 10 euros y dos incidencias operativas. Las incidencias no son ventas.', 'metrics.py: revenue_by_stage. Base SQLite mínima en memoria; cálculo usado indirectamente por la pantalla.'),
    'D05': ('Compartir actuaciones', 'Exportamos un artista con coma y volvemos a leer el CSV.', 'exports.py: export_csv. Misma función que el botón de descarga.'),
    'D06': ('Consultar una selección vacía', 'No hay actuaciones seleccionadas. Es un estado permitido.', 'metrics.py: next_event_label. La pantalla también debe manejar tablas y gráfico vacíos.'),
    'D07': ('Informar de precios desconocidos', 'Conocemos 10 y 20 euros; N/A indica un dato pendiente, no cero.', 'metrics.py: summarize_prices. Función aislada, no conectada a la pantalla.'),
    'D08': ('Comprobar el aforo', 'Con 80 plazas, observamos 79, 80 y 81 entradas vendidas.', 'metrics.py: capacity_status. Misma función que la tabla de ocupación.'),
    'P01': ('Ordenar la programación', 'El festival continúa después de medianoche: importa también la fecha.', 'schedule.py: sort_for_show. Ejemplo aislado; la pantalla recibe filas ordenadas por SQL.'),
    'P02': ('Calcular ocupación conjunta', 'Hay 100 entradas vendidas entre 1100 plazas en dos actuaciones.', 'metrics.py: occupancy_ratio. Misma función que el indicador de la pantalla.'),
    'P03': ('Consultar ingresos seleccionados', 'Seleccionamos solo Escenario Río: el informe debe respetar esa selección.', 'metrics.py: revenue_for_selection. Copia del festival en memoria; misma función que la pantalla.'),
    'P04': ('Contar incidencias con menos consultas', 'Consultamos tres actuaciones y contamos las consultas SQL, no el tiempo.', 'metrics.py: incident_counts. Copia del festival en memoria; misma función que la pantalla.'),
}

def introduction():
    print('FestivalOps: laboratorio de investigación de una aplicación de festival.')
    print('La pantalla consulta actuaciones, entradas, ingresos e incidencias y exporta CSV.')
    print('No vende entradas ni registra artistas. Los datos son sintéticos y los fallos deliberados.')
    print('app.py = pantalla; src/festivalops = funciones; data/source/festival.sql = datos.')
    print('demo.py prepara entradas y muestra resultados; tests comprueba los requisitos.')
    print('Observado se calcula al ejecutar. Esperado es el requisito escrito, no una validación.')
    print('D01-D08: demostraciones guiadas. P01-P04: práctica. P05 es una actividad docente sin comando.')
    print('Elige un caso: python demo.py D01. Todos los casos: python demo.py resumen.')
    for case, (title, _, _) in CASES.items():
        print(f'  {case}: {title}')

def show(case):
    title, situation, route = CASES[case]
    print(f'\nCASO {case}: {title}')
    print('Situación:', situation)
    print('Dónde se ejecuta:', route)
    print('Antes de continuar: predice el resultado y decide qué sería correcto.')
    if case=='D01':
        rows = [{'stage': 'Escenario Principal', 'artist': 'Luz de Barrio'},
                {'stage': 'Escenario Río', 'artist': 'Mar Abierto'}]
        print('Datos del ejemplo:', rows)
        for requested in ('Escenario Principal', ' Escenario Principal '):
            print('Entrada:', repr(requested))
            print('Clave observada:', repr(normalize_stage(requested)))
            print('Actuaciones encontradas:', filter_by_stage(rows, requested))
        print('Esperado: ambas búsquedas devuelven solo Luz de Barrio; clave escenario-principal.')
    elif case=='D02':
        print("Entrada: '19,90'. Esperado: 19.9")
        print('Observado:',parse_price('19,90'))
    elif case=='D03':
        for item in collect_open_incidents.__defaults__ or ():
            if isinstance(item,list):item.clear()
        rows=[{'id':1,'status':'abierta'}]
        first=list(collect_open_incidents(rows));second=list(collect_open_incidents(rows))
        print('Observado primera/segunda:',len(first),len(second),'Esperado: 1 1')
    elif case=='D04':
        with tiny_revenue() as con:
            print('Una venta 2 x 10, dos incidencias.')
            print('Observado:',revenue_by_stage(con),'Esperado ingreso: 20')
    elif case=='D05':
        row=dict(event_id=1,stage='Río',artist='The Cats, Live',starts_at='2026-07-10T23:30:00',sold=2,revenue=20)
        payload=export_csv([row]);print('CSV:',payload)
        parsed=list(csv.DictReader(io.StringIO(payload)))
        print('Leído:',parsed,'Esperado artist: The Cats, Live, seis columnas')
    elif case=='D06':
        print('Entrada: []. Esperado: Sin actuaciones. Comprobar también vista vacía.')
        print('Observado:',next_event_label([]))
    elif case=='D07':
        print('Observado:',summarize_prices(['10','20','N/A']))
        print('Esperado: subtotal 30.0, pending 1, total None')
    elif case=='D08':
        print('Ocupación 79,80,81; aforo80. Observado:',[capacity_status(x,80) for x in (79,80,81)])
        print('Esperado: casi completo, completo, completo')
    elif case=='P01':
        rows=[dict(artist='Antes',starts_at='2026-07-10T23:30:00'),dict(artist='Después',starts_at='2026-07-11T00:30:00')]
        print('Observado:',[r['artist'] for r in sort_for_show(rows)],'Esperado: Antes, Después')
    elif case=='P02':
        print('90/100 y 10/1000. Observado:',occupancy_ratio([dict(sold=90,capacity=100),dict(sold=10,capacity=1000)]))
        print('Esperado: 9.090909... %')
    elif case=='P03':
        with memory_database() as con:
            print('Selección: Escenario Río. Observado:',revenue_for_selection(con,['Escenario Río']))
            print('Esperado: solo Escenario Río con ingreso 27625.0')
    elif case=='P04':
        with memory_database() as con:
            queries=[];con.set_trace_callback(queries.append)
            result=incident_counts(con,[101,102,103]);con.set_trace_callback(None)
            print('Recuentos:',result)
            print('SELECT:',sum(q.lstrip().upper().startswith('SELECT') for q in queries),'Objetivo:1, mismos recuentos')
    else:raise ValueError('ID no válido')

if __name__=='__main__':
    ids=[f'D{i:02}' for i in range(1,9)]+[f'P{i:02}' for i in range(1,5)]
    requested=sys.argv[1] if len(sys.argv)>1 else 'contexto'
    if requested == 'contexto':
        introduction()
        raise SystemExit(0)
    if requested not in ids+['resumen']:raise SystemExit('Usa contexto, D01-D08, P01-P04 o resumen')
    for case in ids if requested=='resumen' else [requested]:
        try:show(case)
        except Exception:
            traceback.print_exc(file=sys.stdout)
            print('La excepción anterior es la observación del caso; ejecuta unittest para verificarlo.')
        finally:
            print('Comprobación independiente: python -m unittest tests.test_casos.' + case + ' -v')
            print('Describe lo observado antes de explicar la causa. Esta demo no certifica un arreglo.')
