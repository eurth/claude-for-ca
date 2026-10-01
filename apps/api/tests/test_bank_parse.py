from pathlib import Path

from pypdf import PdfReader

from app.runtime.bank_parse import parse_bank_statement

SAMPLE = """
Opening balance: 2,45,320.50 Cr
01-04-2026  NEFT/SHARMA TRADERS/INV ST-1042                    11,800.00   2,57,120.50
03-04-2026  UPI/RENT/APR26                         25,000.00               2,32,120.50
Closing balance: 1,75,654.90 Cr
"""


def test_parse_plain_statement_text():
    data = parse_bank_statement(SAMPLE)
    assert data["opening"] == 245320.50
    assert data["closing"] == 175654.90
    assert len(data["rows"]) == 2
    assert data["rows"][0]["credit"] == 11800.00
    assert data["rows"][1]["debit"] == 25000.00


def test_parse_sample_bank_pdf():
    pdf = (
        Path(__file__).resolve().parents[3]
        / "Test"
        / "samples"
        / "bank"
        / "HDFC-50200011223344-Apr-2026.pdf"
    )
    text = "\n".join((page.extract_text() or "") for page in PdfReader(str(pdf)).pages)
    data = parse_bank_statement(text)
    assert data["opening"] == 245320.50
    assert data["closing"] == 175654.90
    assert len(data["rows"]) >= 10
    narrations = " ".join(r["narration"] for r in data["rows"])
    assert "SHARMA" in narrations.upper()
    assert "GST" in narrations.upper() or any(r["category"] == "GST" for r in data["rows"])
