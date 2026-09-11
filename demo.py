"""Observa un caso real. La verificación se ejecuta aparte con unittest."""
import csv,io,sys,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
from festivalops.database import memory_database
from festivalops.filters import normalize_stage
from festivalops.exports import export_csv
from festivalops.metrics import (parse_price,collect_open_incidents,revenue_by_stage,
    next_event_label,summarize_prices,capacity_status,occupancy_ratio,
    revenue_for_selection,incident_counts)
from festivalops.schedule import sort_for_show
from tests.test_casos import tiny_revenue

def show(case):
    print('\nCASO',case)
    if case=='D01':
        print('Entrada:',repr(' Escenario Principal '))
        print('Observado:',repr(normalize_stage(' Escenario Principal ')))
        print('Esperado:',repr('escenario-principal'))
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
    requested=sys.argv[1] if len(sys.argv)>1 else 'resumen'
    if requested not in ids+['resumen']:raise SystemExit('Usa D01-D08, P01-P04 o resumen')
    for case in ids if requested=='resumen' else [requested]:
        try:show(case)
        except Exception:
            traceback.print_exc()
            print('La excepción anterior es la observación del caso; ejecuta unittest para verificarlo.')
