"""Comprueba el material sin reparar los defectos del laboratorio."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DemoContext(unittest.TestCase):
    def run_demo(self, *arguments):
        return subprocess.run(
            [sys.executable, str(ROOT / 'demo.py'), *arguments],
            cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
            env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'},
        )

    def test_default_is_context_not_incidents(self):
        result = self.run_demo()
        self.assertEqual(result.returncode, 0)
        self.assertIn('laboratorio', result.stdout)
        self.assertNotIn('CASO D01:', result.stdout)

    def test_d01_calls_filter_for_both_inputs(self):
        result = self.run_demo('D01')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.count('Actuaciones encontradas:'), 2)
        self.assertIn('Luz de Barrio', result.stdout)
        self.assertIn('tests.test_casos.D01', result.stdout)

    def test_summary_continues_after_expected_exceptions(self):
        result = self.run_demo('resumen')
        self.assertEqual(result.returncode, 0)
        self.assertIn('CASO P04:', result.stdout)
        self.assertEqual(result.stdout.count('Comprobación independiente:'), 12)
