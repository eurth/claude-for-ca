from pathlib import Path

from openpyxl import load_workbook

from app.runtime.catalog import CATALOG, get_feature
from app.runtime.loader import load_skill
from app.workbook import build_master_accounts, purchase_rows_table, write_rows_xlsx


def test_every_catalog_skill_loads():
    missing = []
    for item in CATALOG:
        try:
            text = load_skill(item["id"])
        except FileNotFoundError:
            missing.append(item["id"])
            continue
        assert len(text) > 80, item["id"]
        assert "${CLAUDE_PLUGIN_ROOT}" not in text
    assert not missing, missing
    assert len(CATALOG) >= 45


def test_master_accounts_workbook_has_eleven_sheets(tmp_path):
    purchase = [
        {
            "vendor": "Sharma Traders",
            "gstin": "37AABCS1234Z1Z5",
            "invoice_no": "ST/1042",
            "date": "05-Apr-2026",
            "taxable_value": 10000,
            "cgst": 900,
            "sgst": 900,
            "igst": 0,
            "total": 11800,
        }
    ]
    bank = [{"date": "01-04-2026", "narration": "NEFT", "debit": 0, "credit": 11800, "balance": 100, "category": "receipt"}]
    path = Path(tmp_path) / "master.xlsx"
    meta = build_master_accounts(
        path,
        company="Example Traders Pvt Ltd",
        period="2026-04",
        purchase=purchase,
        sales=[],
        bank=bank,
        opening=245320.5,
        closing=175654.9,
    )
    assert path.exists()
    wb = load_workbook(path)
    assert "SUMMARY" in wb.sheetnames
    assert "PURCHASE" in wb.sheetnames
    assert "BANK" in wb.sheetnames
    assert meta["purchase_rows"] == 1


def test_register_xlsx(tmp_path):
    headers, rows = purchase_rows_table(
        [{"vendor": "A", "gstin": "37AABCS1234Z1Z5", "invoice_no": "1", "taxable_value": 10, "cgst": 0, "sgst": 0, "igst": 0, "total": 10}]
    )
    path = Path(tmp_path) / "pr.xlsx"
    write_rows_xlsx(path, "PURCHASE", headers, rows)
    wb = load_workbook(path)
    assert wb.active["A2"].value == "A"


def test_get_feature_tally_is_hitl():
    feat = get_feature("tally-import-builder")
    assert feat["filing_class"] == "tally_write"
    assert feat["name"] == "Tally import file"
