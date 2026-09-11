"""Plantilla compartida de pruebas de aceptación; copiada a cada repositorio."""
import csv, io, sys, unittest, sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from festivalops.database import memory_database
from festivalops.filters import normalize_stage, filter_by_stage
from festivalops.exports import export_csv, FIELDS
from festivalops.metrics import (parse_price, collect_open_incidents, revenue_by_stage,
    next_event_label, summarize_prices, capacity_status, occupancy_ratio,
    revenue_for_selection, incident_counts)
from festivalops.schedule import sort_for_show

def tiny_revenue():
    con=sqlite3.connect(':memory:');con.row_factory=sqlite3.Row
    con.executescript('''CREATE TABLE stages(stage_id, name);
    CREATE TABLE events(event_id, stage_id);
    CREATE TABLE ticket_sales(event_id, quantity, unit_price);
    CREATE TABLE incidents(event_id);
    INSERT INTO stages VALUES(1,'Principal'); INSERT INTO events VALUES(1,1);
    INSERT INTO ticket_sales VALUES(1,2,'10');
    INSERT INTO incidents VALUES(1),(1);''')
    return con

class D01(unittest.TestCase):
    def test_equivalence(self):
        self.assertEqual(normalize_stage(' Escenario Principal '),'escenario-principal')
        self.assertEqual(normalize_stage('ESCENARIO PRINCIPAL'),'escenario-principal')
        rows=[{'stage':'Escenario Principal'},{'stage':'Escenario Río'}];before=list(rows)
        self.assertEqual(filter_by_stage(rows,' Escenario Principal '),[rows[0]])
        self.assertEqual(rows,before)

class D02(unittest.TestCase):
    def test_formats(self):
        for v in ('19,90','19.90',19.9):self.assertAlmostEqual(parse_price(v),19.9)
    def test_invalid(self):
        with self.assertRaises(ValueError):parse_price('gratis')

class D03(unittest.TestCase):
    def setUp(self):
        # Aísla el caso en la suite; las dos llamadas del test siguen compartiendo proceso.
        for item in collect_open_incidents.__defaults__ or ():
            if isinstance(item,list):item.clear()
    def test_repeated(self):
        rows=[{'id':1,'status':'abierta'},{'id':2,'status':'cerrada'}]
        first=collect_open_incidents(rows);snapshot=list(first)
        second=collect_open_incidents(rows)
        self.assertEqual(snapshot,[rows[0]]);self.assertEqual(second,[rows[0]])
        self.assertIsNot(first,second)
    def test_explicit_accumulator(self):
        accumulator=[];row={'status':'abierta'}
        result=collect_open_incidents([row],accumulator)
        self.assertIs(result,accumulator);self.assertEqual(result,[row])

class D04(unittest.TestCase):
    def test_join(self):
        with tiny_revenue() as con:
            self.assertEqual(revenue_by_stage(con)[0]['revenue'],20)
    def test_equal_sales_are_real(self):
        with tiny_revenue() as con:
            con.execute("INSERT INTO ticket_sales VALUES(1,2,'10')")
            self.assertEqual(revenue_by_stage(con)[0]['revenue'],40)
    def test_no_incidents(self):
        with tiny_revenue() as con:
            con.execute('DELETE FROM incidents')
            self.assertEqual(revenue_by_stage(con)[0]['revenue'],20)

class D05(unittest.TestCase):
    def test_roundtrip(self):
        rows=[dict(event_id=1,stage='Río',artist=artist,starts_at='2026-07-10T23:30:00',sold=2,revenue=20)
              for artist in ['The Cats, Live','A"B','Primera\nSegunda']]
        parsed=list(csv.DictReader(io.StringIO(export_csv(rows))))
        self.assertEqual(len(parsed),3)
        for original,result in zip(rows,parsed):
            self.assertEqual(list(result),list(FIELDS))
            self.assertEqual(result,{f:str(original[f]) for f in FIELDS})
    def test_empty(self):
        reader=csv.DictReader(io.StringIO(export_csv([])))
        self.assertEqual(reader.fieldnames,list(FIELDS));self.assertEqual(list(reader),[])

class D06(unittest.TestCase):
    def test_empty(self):self.assertEqual(next_event_label([]),'Sin actuaciones')
    def test_nonempty(self):self.assertEqual(next_event_label([{'artist':'Luz'}]),'Luz')

class D07(unittest.TestCase):
    def test_pending(self):self.assertEqual(summarize_prices(['10','20','N/A']),dict(subtotal=30.0,pending=1,total=None))
    def test_valid(self):self.assertEqual(summarize_prices(['10','20']),dict(subtotal=30.0,pending=0,total=30.0))
    def test_empty(self):self.assertEqual(summarize_prices([]),dict(subtotal=0.0,pending=0,total=0.0))

class D08(unittest.TestCase):
    def test_boundary(self):
        self.assertEqual([capacity_status(x,80) for x in (79,80,81)],['casi completo','completo','completo'])
    def test_threshold(self):
        self.assertEqual([capacity_status(x,100) for x in (79,80,99)],['disponible','casi completo','casi completo'])

class P01(unittest.TestCase):
    def test_midnight(self):
        rows=[dict(artist='Antes',starts_at='2026-07-10T23:30:00'),dict(artist='Después',starts_at='2026-07-11T00:30:00')]
        before=[dict(r) for r in rows]
        self.assertEqual([r['artist'] for r in sort_for_show(rows)],['Antes','Después'])
        self.assertEqual(rows,before)
    def test_empty_tie(self):
        self.assertEqual(sort_for_show([]),[])
        rows=[dict(id=2,starts_at='2026-07-10T23:30:00'),dict(id=1,starts_at='2026-07-10T23:30:00')]
        self.assertEqual(sort_for_show(rows),rows)

class P02(unittest.TestCase):
    def test_weighted(self):self.assertAlmostEqual(occupancy_ratio([dict(sold=90,capacity=100),dict(sold=10,capacity=1000)]),100/1100*100)
    def test_common(self):self.assertAlmostEqual(occupancy_ratio([dict(sold=50,capacity=100),dict(sold=100,capacity=200)]),50)
    def test_zero(self):
        self.assertIsNone(occupancy_ratio([]));self.assertIsNone(occupancy_ratio([dict(sold=0,capacity=0)]))
        self.assertAlmostEqual(occupancy_ratio([dict(sold=0,capacity=0),dict(sold=50,capacity=100)]),50)

class P03(unittest.TestCase):
    def test_one(self):
        with memory_database() as con:
            rows=revenue_for_selection(con,['Escenario Río'])
            self.assertEqual([r['stage'] for r in rows],['Escenario Río'])
            self.assertAlmostEqual(rows[0]['revenue'],27625)
    def test_all(self):
        with memory_database() as con:
            names=[r[0] for r in con.execute('SELECT name FROM stages')]
            self.assertEqual(revenue_for_selection(con,names),revenue_by_stage(con))
    def test_empty_unknown(self):
        with memory_database() as con:
            self.assertEqual(revenue_for_selection(con,[]),[])
            self.assertEqual(revenue_for_selection(con,['No existe']),[])

class P04(unittest.TestCase):
    def test_equivalence_and_queries(self):
        with memory_database() as con:
            ids=[101,102,103]
            expected={i:con.execute('SELECT COUNT(*) FROM incidents WHERE event_id=?',(i,)).fetchone()[0] for i in ids}
            queries=[];con.set_trace_callback(queries.append)
            result=incident_counts(con,ids+[101]);con.set_trace_callback(None)
            self.assertEqual(result,expected)
            self.assertEqual(sum(q.lstrip().upper().startswith('SELECT') for q in queries),1)
    def test_empty(self):
        with memory_database() as con:
            queries=[];con.set_trace_callback(queries.append)
            self.assertEqual(incident_counts(con,[]),{})
            self.assertEqual(queries,[])
    def test_zero(self):
        with memory_database() as con:
            con.execute('DELETE FROM incidents WHERE event_id=101')
            self.assertEqual(incident_counts(con,[101]),{101:0})
