from pathlib import Path

from pypdf import PdfReader

from app.runtime.invoice_parse import parse_invoice_text, parse_invoice_uploads


def test_parse_sharma_and_ravi_pdfs():
    root = Path(__file__).resolve().parents[3] / "Test" / "samples" / "invoices"
    sharma = "\n".join(
        (p.extract_text() or "")
        for p in PdfReader(str(root / "INV-ST-1042-Sharma-Traders.pdf")).pages
    )
    ravi = "\n".join((p.extract_text() or "") for p in PdfReader(str(root / "INV-RK-88-Ravi-Kirana.pdf")).pages)
    s = parse_invoice_text(sharma)
    r = parse_invoice_text(ravi)
    assert s["rows"][0]["vendor"] == "Sharma Traders"
    assert s["rows"][0]["invoice_no"] == "ST/1042"
    assert s["rows"][0]["total"] == 11800.0
    assert r["rows"][0]["vendor"] == "Ravi Kirana Stores"
    assert r["rows"][0]["igst"] == 900.0


def test_duplicate_and_matching_buyer_gstin():
    root = Path(__file__).resolve().parents[3] / "Test" / "samples" / "invoices"
    uploads = []
    for name in (
        "INV-ST-1042-Sharma-Traders.pdf",
        "INV-RK-88-Ravi-Kirana.pdf",
        "INV-ST-1042-duplicate.pdf",
    ):
        text = "\n".join((p.extract_text() or "") for p in PdfReader(str(root / name)).pages)
        uploads.append({"filename": name, "text_excerpt": text})
    data = parse_invoice_uploads(uploads, job_gstin="37AACTE1234F1Z5")
    assert len(data["rows"]) == 3
    assert any("Duplicate invoice number ST/1042" in item for item in data["items"])
    assert not any("buyer GSTIN" in item for item in data["items"])
    assert not any("inter-state supply should use IGST" in item for item in data["items"])
