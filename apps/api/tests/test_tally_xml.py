from app.tally_xml import purchase_register_to_xml


def test_purchase_xml_contains_company_and_totals():
    xml = purchase_register_to_xml(
        [
            {
                "vendor": "Sharma Traders",
                "gstin": "37AABCS1234Z1Z5",
                "invoice_no": "ST/1",
                "date": "20260401",
                "taxable_value": 1000,
                "cgst": 90,
                "sgst": 90,
                "igst": 0,
                "total": 1180,
            }
        ],
        "Example Traders Pvt Ltd",
    )
    assert "Example Traders Pvt Ltd" in xml
    assert "Sharma Traders" in xml
    assert "CGST Input" in xml
    assert "1180.00" in xml
