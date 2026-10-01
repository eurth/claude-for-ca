GSTR3B = """GSTR-3B — PARTNER APPROVAL REQUIRED

This pack is a draft working only. It is not filed.

Before marking ready:
  [ ] GSTR-1 is filed for this period
  [ ] ITC reconciled with GSTR-2B
  [ ] Rule 42/43 reversals considered
  [ ] Cash/credit ledger is sufficient
  [ ] Client has authorised filing

Approve = intern may give the working to the filer
Deny = stop — review manually
"""

TALLY = """TALLY IMPORT FILE — PARTNER APPROVAL REQUIRED
This file can change accounting data once imported in Tally.

  [ ] Voucher amounts are correct
  [ ] Ledger heads are correctly mapped
  [ ] No duplicate entries
  [ ] GST ledgers (CGST/SGST/IGST) mapped

Approve = download XML for Gateway → Import Data
Deny = do not import
"""

NOTICE = """NOTICE REPLY — PARTNER APPROVAL REQUIRED

This is a draft. Do not send or upload to any portal until signed.

  [ ] Facts match the notice and books
  [ ] Deadline is diary'd
  [ ] CA / advocate has reviewed the legal basis
  [ ] Client has authorised sending

Approve = ready to send outside this app
Deny = revise
"""

ITR = """ITR PACK — PARTNER APPROVAL REQUIRED
  [ ] 26AS / AIS reconciled
  [ ] Computations reviewed
  [ ] Client has authorised filing
"""

TDS = """TDS RETURN PACK — PARTNER APPROVAL REQUIRED
  [ ] Challans matched
  [ ] Deductee PANs verified
  [ ] Late fee / interest computed if any
"""

MCA = """MCA / ROC PACK — PARTNER APPROVAL REQUIRED
  [ ] CIN and form type correct
  [ ] Board approval on file
  [ ] DSC holder identified
"""


def template_for(kind: str) -> str:
    return {
        "gst_filing": GSTR3B,
        "tally_write": TALLY,
        "notice_send": NOTICE,
        "itr_filing": ITR,
        "tds_filing": TDS,
        "mca_filing": MCA,
    }.get(kind, NOTICE)
