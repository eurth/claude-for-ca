CATALOG = [
    {
        "id": "pdf-data-extractor",
        "name": "Extract invoices",
        "section": "Documents",
        "effort": "medium",
        "scope": "gstin",
        "filing_class": None,
        "produces": ["purchase_register", "sales_register", "exception_report"],
        "consumes": [],
        "description": "Read invoice PDFs into a purchase or sales register and flag GST errors.",
    },
    {
        "id": "bank-statement-processor",
        "name": "Process bank statement",
        "section": "Documents",
        "effort": "medium",
        "scope": "entity",
        "filing_class": None,
        "produces": ["bank_ledger", "exception_report"],
        "consumes": ["purchase_register"],
        "description": "Extract bank transactions, suggest Tally ledgers, list unmatched items.",
    },
    {
        "id": "tally-import-builder",
        "name": "Tally import file",
        "section": "Documents",
        "effort": "medium",
        "scope": "entity",
        "filing_class": "tally_write",
        "produces": ["tally_xml"],
        "consumes": ["purchase_register", "bank_ledger"],
        "description": "Build a Tally XML file for Gateway → Import Data. Partner approves before download.",
    },
    {
        "id": "gstr3b-review",
        "name": "Review GSTR-3B",
        "section": "GST",
        "effort": "high",
        "scope": "gstin",
        "filing_class": "gst_filing",
        "produces": ["gstr3b_working"],
        "consumes": ["purchase_register", "sales_register", "gstr2b_excel"],
        "description": "Monthly GSTR-3B working, ITC eligibility, cash vs credit. Not filed from this app.",
    },
    {
        "id": "notice-triage",
        "name": "Notice (GST or income tax)",
        "section": "Notices",
        "effort": "high",
        "scope": "entity",
        "filing_class": "notice_send",
        "produces": ["draft_reply", "notice_summary"],
        "consumes": ["notice_pdf"],
        "description": "Explain a notice in plain language and draft a reply for Partner review.",
    },
    {
        "id": "discover",
        "name": "What do I need?",
        "section": "Help",
        "effort": "low",
        "scope": "none",
        "filing_class": None,
        "produces": ["router_suggestion"],
        "consumes": [],
        "description": "Describe the task; the app points you to the right feature.",
    },
]


def get_feature(feature_id: str) -> dict:
    for item in CATALOG:
        if item["id"] == feature_id:
            return item
    raise KeyError(feature_id)
