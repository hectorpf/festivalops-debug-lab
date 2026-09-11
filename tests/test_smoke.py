import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from festivalops.database import memory_database, integrity_report
class Smoke(unittest.TestCase):
    def test_database(self):
        with memory_database() as con:
            report=integrity_report(con)
            self.assertEqual(report["integrity"], "ok")
            self.assertEqual(report["foreign_key_errors"], [])
            self.assertEqual(report["events"], 8)
