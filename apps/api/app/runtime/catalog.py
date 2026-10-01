"""Staff feature catalog. Every runnable SKILL.md except section `review` dashboards."""

from __future__ import annotations


def _f(
    id: str,
    name: str,
    section: str,
    source: str,
    *,
    effort: str = "medium",
    scope: str = "entity",
    filing_class: str | None = None,
    produces: list[str] | None = None,
    consumes: list[str] | None = None,
    description: str = "",
) -> dict:
    return {
        "id": id,
        "name": name,
        "section": section,
        "source": source,
        "effort": effort,
        "scope": scope,
        "filing_class": filing_class,
        "produces": produces or [],
        "consumes": consumes or [],
        "description": description,
    }


CATALOG = [
    _f("pdf-data-extractor", "Extract invoices", "Documents", "document-intake/skills/pdf-data-extractor/SKILL.md", scope="gstin", produces=["purchase_register", "sales_register", "exception_report"], description="Read invoice PDFs into a purchase or sales register and flag GST errors."),
    _f("bank-statement-processor", "Process bank statement", "Documents", "document-intake/skills/bank-statement-processor/SKILL.md", produces=["bank_ledger", "exception_report"], consumes=["purchase_register"], description="Extract bank transactions, suggest Tally ledgers, list unmatched items."),
    _f("email-invoice-fetch", "Fetch invoices from email", "Documents", "document-intake/skills/email-invoice-fetch/SKILL.md", produces=["purchase_register", "exception_report"], description="Upload invoice PDFs saved from email. Live Gmail fetch is v2."),
    _f("master-accounts-sheet", "Master accounts workbook", "Documents", "document-intake/skills/master-accounts-sheet/SKILL.md", effort="high", produces=["master_accounts"], consumes=["purchase_register", "sales_register", "bank_ledger"], description="Build the 11-sheet Master Accounts Excel from this client’s registers and bank ledger."),
    _f("tally-import-builder", "Tally import file", "Documents", "document-intake/skills/tally-import-builder/SKILL.md", filing_class="tally_write", produces=["tally_xml"], consumes=["purchase_register", "bank_ledger"], description="Build a Tally XML file for Gateway → Import Data. Partner approves before download."),
    _f("gstr1-review", "Review GSTR-1", "GST", "gst-compliance/skills/gstr1-review/SKILL.md", effort="high", scope="gstin", filing_class="gst_filing", produces=["gstr1_working", "exception_report"], consumes=["sales_register", "purchase_register"], description="GSTR-1 working from the sales register. Not filed from this app."),
    _f("gstr3b-review", "Review GSTR-3B", "GST", "gst-compliance/skills/gstr3b-review/SKILL.md", effort="high", scope="gstin", filing_class="gst_filing", produces=["gstr3b_working"], consumes=["purchase_register", "sales_register", "gstr2b_excel"], description="Monthly GSTR-3B working, ITC eligibility, cash vs credit. Not filed from this app."),
    _f("itc-reconcile", "Reconcile ITC (GSTR-2B)", "GST", "gst-compliance/skills/itc-recon/SKILL.md", effort="high", scope="gstin", produces=["itc_recon", "exception_report"], consumes=["purchase_register", "gstr2b_excel"], description="Match the purchase register to GSTR-2B. CA sign-off before ITC is claimed."),
    _f("notice-triage", "GST notice", "Notices", "gst-compliance/skills/notice-triage/SKILL.md", effort="high", filing_class="notice_send", produces=["draft_reply", "notice_summary"], consumes=["notice_pdf"], description="Explain a GST notice in plain language and draft a reply for Partner review."),
    _f("annual-return", "GSTR-9 / 9C", "GST", "gst-compliance/skills/annual-return/SKILL.md", effort="high", scope="gstin", filing_class="gst_filing", produces=["gstr9_working"], consumes=["purchase_register", "sales_register", "gstr3b_working"], description="Annual GST return working and 9C recon. Partner reviews certification."),
    _f("gst-audit", "GST audit (65/66)", "GST", "gst-compliance/skills/gst-audit/SKILL.md", effort="high", scope="gstin", filing_class="gst_filing", produces=["gst_audit_working", "draft_reply"], description="Scrutiny checklist and representation draft. Partner reviews before sending."),
    _f("itr-review", "Review ITR", "Income tax", "income-tax/skills/itr-review/SKILL.md", effort="high", filing_class="itr_filing", produces=["itr_working", "exception_report"], consumes=["form26as"], description="ITR mismatch report and tax computation. Partner must approve before e-filing."),
    _f("notice-analysis", "Income-tax notice", "Notices", "income-tax/skills/notice-analysis/SKILL.md", effort="high", filing_class="notice_send", produces=["notice_summary", "draft_reply"], consumes=["notice_pdf"], description="Plain-language IT notice summary and reply draft. Partner before sending."),
    _f("advance-tax", "Advance tax", "Income tax", "income-tax/skills/advance-tax/SKILL.md", produces=["advance_tax_schedule"], description="Instalment schedule with 234B/234C. Confirm estimates with Partner."),
    _f("capital-gains", "Capital gains", "Income tax", "income-tax/skills/capital-gains/SKILL.md", effort="high", produces=["capital_gains_schedule"], description="Per-asset capital gains schedule and set-off. CA before filing."),
    _f("tax-audit-3cd", "Tax audit 3CD", "Income tax", "income-tax/skills/tax-audit-3cd/SKILL.md", effort="high", filing_class="itr_filing", produces=["form_3cd_working"], description="44-clause 3CD disclosures. Never certify unread."),
    _f("search-survey", "Search / survey", "Income tax", "income-tax/skills/search-survey/SKILL.md", effort="high", produces=["search_survey_note"], description="Rights guidance and preservation checklist. Escalate to specialist/advocate."),
    _f("default-check", "TDS default check", "TDS", "tds-compliance/skills/default-check/SKILL.md", produces=["tds_default_report"], description="Defaults and 201(1A) interest from payment ledger and challans."),
    _f("26as-recon", "Reconcile 26AS", "TDS", "tds-compliance/skills/26as-recon/SKILL.md", produces=["form26as_recon", "exception_report"], consumes=["form26as"], description="Match 26AS/AIS to books. Credit ITR only per 26AS."),
    _f("form-16-generator", "Form 16 / 16A data", "TDS", "tds-compliance/skills/form-16-generator/SKILL.md", produces=["form16_working"], description="Part B draft from salary register. Verify before issue."),
    _f("quarterly-return", "TDS quarterly return", "TDS", "tds-compliance/skills/quarterly-return/SKILL.md", effort="high", filing_class="tds_filing", produces=["tds_return_working"], description="234E and pre-filing checklist. Partner before filing on TRACES."),
    _f("caro-review", "CARO 2020", "Audit", "audit/skills/caro-review/SKILL.md", effort="high", produces=["caro_working"], description="21 clause drafts. Evidence-backed only."),
    _f("risk-matrix", "Audit risk matrix", "Audit", "audit/skills/risk-matrix/SKILL.md", produces=["audit_risk_matrix"], description="Materiality and SA-315 risk matrix."),
    _f("workpaper-draft", "Workpapers", "Audit", "audit/skills/workpaper-draft/SKILL.md", effort="high", produces=["workpapers"], description="Lead schedules, representation letter, completion checklist."),
    _f("bank-audit-lfar", "Bank audit / LFAR", "Audit", "audit/skills/bank-audit-lfar/SKILL.md", effort="high", produces=["lfar_working"], description="NPA review and LFAR responses."),
    _f("internal-audit", "Internal audit", "Audit", "audit/skills/internal-audit/SKILL.md", effort="high", produces=["internal_audit_report"], description="Plan and internal audit report."),
    _f("filing-tracker", "ROC filing tracker", "MCA", "mca-secretarial/skills/filing-tracker/SKILL.md", filing_class="mca_filing", produces=["roc_tracker"], description="ROC status board and late fees. Filing stays outside this app."),
    _f("resolution", "Board resolution", "MCA", "mca-secretarial/skills/resolution/SKILL.md", produces=["board_resolution"], description="Resolution text and MGT-14 checklist."),
    _f("annual-compliance", "Annual company compliance", "MCA", "mca-secretarial/skills/annual-compliance/SKILL.md", effort="high", filing_class="mca_filing", produces=["annual_compliance_pack"], description="AGM notice and directors’ report checklist."),
    _f("charge-registry", "Charge registry", "MCA", "mca-secretarial/skills/charge-registry/SKILL.md", filing_class="mca_filing", produces=["charge_pack"], description="CHG-1/4 pack and late-fee guidance."),
    _f("form-3ceb", "Form 3CEB", "Transfer pricing", "transfer-pricing/skills/form-3ceb/SKILL.md", effort="high", filing_class="itr_filing", produces=["form_3ceb_working"], description="Para-wise 3CEB drafts. CA signature required."),
    _f("tp-documentation", "TP documentation", "Transfer pricing", "transfer-pricing/skills/tp-documentation/SKILL.md", effort="high", produces=["tp_study"], description="Rule 10D study. Watch 271AA."),
    _f("fdi-compliance", "FDI (FC-GPR / FC-TRS)", "FEMA", "fema-compliance/skills/fdi-compliance/SKILL.md", effort="high", produces=["fdi_checklist"], description="FC-GPR / FC-TRS checklists and pricing-norm notes."),
    _f("odi-compliance", "ODI / APR", "FEMA", "fema-compliance/skills/odi-compliance/SKILL.md", effort="high", produces=["odi_checklist"], description="ODI and APR checklists for overseas JV/WOS."),
    _f("pf-recon", "PF / ECR", "Payroll", "payroll-compliance/skills/pf-recon/SKILL.md", produces=["pf_register"], description="PF register and ECR checklist from the salary register."),
    _f("esic-recon", "ESIC", "Payroll", "payroll-compliance/skills/esic-recon/SKILL.md", produces=["esic_register"], description="ESIC register for wages within the ceiling."),
    _f("professional-tax", "Professional tax", "Payroll", "payroll-compliance/skills/professional-tax/SKILL.md", produces=["pt_working"], description="PT table and deposit authority by state."),
    _f("tax-planning", "Tax planning", "Advisory", "advisory-ca/skills/tax-planning/SKILL.md", effort="high", produces=["tax_plan"], description="Old vs new regime and year-end checklist. GAAR caution."),
    _f("msme-advisory", "MSME / Udyam", "Advisory", "advisory-ca/skills/msme-advisory/SKILL.md", produces=["msme_note"], description="Udyam guidance and 43B(h) analysis."),
    _f("kyc-checklist", "KYC checklist", "Clients", "client-onboarding/skills/kyc-checklist/SKILL.md", produces=["kyc_checklist"], description="Entity-type document checklist and PMLA log."),
    _f("engagement-letter", "Engagement letter", "Clients", "client-onboarding/skills/engagement-letter/SKILL.md", produces=["engagement_letter"], description="SA-210 draft. Sign before statutory work."),
    _f("fee-tracker", "Fee tracker", "Practice", "firm-management/skills/fee-tracker/SKILL.md", produces=["fee_register"], description="Billing, WIP and reminder drafts."),
    _f("articleship-log", "Articleship diary", "Articles", "ca-student/skills/articleship-log/SKILL.md", produces=["articleship_log"], description="Diary vs ICAI minima."),
    _f("exam-prep", "Exam prep", "Articles", "ca-student/skills/exam-prep/SKILL.md", produces=["study_plan"], description="Notes and study plan by paper."),
    _f("onboard-firm", "Set up this firm", "Practice", "cold-start/skills/onboard-firm/SKILL.md", effort="high", produces=["firm_setup"], description="Firm profile working and calendar seed. Does not file."),
    _f("add-client", "Add client pack", "Clients", "cold-start/skills/add-client/SKILL.md", produces=["client_onboarding_pack"], description="Client facts checklist and calendar tasks to open the file."),
    _f("discover", "What do I need?", "Help", "ca-builder-hub/skills/discover/SKILL.md", effort="low", scope="none", produces=["router_suggestion"], description="Describe the task; the app points you to the right feature."),
]


def get_feature(feature_id: str) -> dict:
    for item in CATALOG:
        if item["id"] == feature_id:
            return item
    raise KeyError(feature_id)
