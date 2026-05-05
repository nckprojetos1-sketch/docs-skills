from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPO_ROOT / "skills" / "docs-pdf-context" / "scripts" / "extract_pdf_context.py"

spec = importlib.util.spec_from_file_location("extract_pdf_context", SCRIPT_PATH)
extract_pdf_context = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["extract_pdf_context"] = extract_pdf_context
spec.loader.exec_module(extract_pdf_context)


try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover
    fitz = None  # type: ignore


class ExtractPdfContextTests(unittest.TestCase):
    def test_fixture_generates_cross_referenced_package(self) -> None:
        fixture = REPO_ROOT / "requisitos_minimos_catalogo_produtos_api.pdf"
        if not fixture.exists():
            self.skipTest("fixture PDF not present")

        with tempfile.TemporaryDirectory() as temp_dir:
            pdf = extract_pdf_context.validate_pdf(str(fixture))
            doc = extract_pdf_context.extract_document(pdf)
            payload = extract_pdf_context.write_outputs(doc, Path(temp_dir))

            self.assertTrue(payload["valid"], payload["warnings"])
            self.assertEqual(payload["page_count"], 7)
            self.assertEqual(payload["tables_count"], 7)
            self.assertEqual(payload["callouts_count"], 5)

            readme = Path(payload["readme"]).read_text(encoding="utf-8")
            tables = json.loads(Path(payload["tables_json"]).read_text(encoding="utf-8"))

            for req_id in [f"RF-{index:02d}" for index in range(1, 11)]:
                self.assertIn(req_id, readme)
            for table in tables["tables"]:
                self.assertIn(table["table_id"], readme)
                self.assertIn("row_id", table["rows"][0])
            self.assertNotIn("_ _", readme)

    @unittest.skipIf(fitz is None, "PyMuPDF not available")
    def test_pdf_without_tables_writes_no_tables_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "plain.pdf"
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 72), "Objetivo do documento\nCriar sistema simples.\nRF-01 Deve listar clientes.\nCriterio de aceite: lista aparece.")
            doc.save(pdf_path)
            doc.close()

            extracted = extract_pdf_context.extract_document(pdf_path)
            payload = extract_pdf_context.write_outputs(extracted, Path(temp_dir) / "out")

            self.assertTrue(payload["valid"], payload["warnings"])
            self.assertIsNone(payload["tables_json"])
            self.assertTrue(Path(payload["readme"]).exists())

    @unittest.skipIf(fitz is None, "PyMuPDF not available")
    def test_blank_pdf_fails_without_inventing_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "blank.pdf"
            doc = fitz.open()
            doc.new_page()
            doc.save(pdf_path)
            doc.close()

            extracted = extract_pdf_context.extract_document(pdf_path)
            with self.assertRaises(extract_pdf_context.ExtractionError):
                extract_pdf_context.write_outputs(extracted, Path(temp_dir) / "out")


if __name__ == "__main__":
    unittest.main()
