"""Create GST invoice and bank-statement PDFs for for-ca testing."""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "samples" / "invoices"
BANK = ROOT / "samples" / "bank"
INV.mkdir(parents=True, exist_ok=True)
BANK.mkdir(parents=True, exist_ok=True)


def _header(c, title):
    c.setFont("Times-Bold", 16)
    c.drawString(20 * mm, 280 * mm, title)
    c.setFont("Times-Roman", 9)
    c.drawString(20 * mm, 274 * mm, "Test document — not a real tax invoice / statement")


def write_invoice(path, *, inv_no, date, vendor, vgstin, buyer, bgstin, rows, igst=False, vendor_state="Andhra Pradesh"):
    c = canvas.Canvas(str(path), pagesize=A4)
    _header(c, "TAX INVOICE")
    y = 262
    c.setFont("Times-Bold", 11)
    c.drawString(20 * mm, y * mm, vendor)
    c.setFont("Times-Roman", 10)
    y -= 6
    c.drawString(20 * mm, y * mm, f"GSTIN: {vgstin}")
    y -= 6
    c.drawString(20 * mm, y * mm, vendor_state)
    y -= 10
    c.setFont("Times-Bold", 10)
    c.drawString(20 * mm, y * mm, f"Invoice No: {inv_no}     Date: {date}")
    y -= 8
    c.setFont("Times-Roman", 10)
    c.drawString(20 * mm, y * mm, f"Bill to: {buyer}")
    y -= 6
    c.drawString(20 * mm, y * mm, f"Buyer GSTIN: {bgstin}")
    y -= 12
    c.setFont("Times-Bold", 9)
    c.drawString(20 * mm, y * mm, "HSN   Description            Qty    Rate     Taxable   CGST    SGST    IGST    Total")
    y -= 6
    c.setFont("Times-Roman", 9)
    tot_t = tot_c = tot_s = tot_i = tot = 0
    for row in rows:
        hsn, desc, qty, rate, taxable, cgst, sgst, ig, total = row
        tot_t += taxable
        tot_c += cgst
        tot_s += sgst
        tot_i += ig
        tot += total
        c.drawString(
            20 * mm,
            y * mm,
            f"{hsn}  {desc:<20} {qty:>4} {rate:>8.2f} {taxable:>9.2f} {cgst:>7.2f} {sgst:>7.2f} {ig:>7.2f} {total:>8.2f}",
        )
        y -= 6
    y -= 4
    c.setFont("Times-Bold", 10)
    tax_note = "IGST @ 18% (inter-state)" if igst else "CGST 9% + SGST 9%"
    c.drawString(20 * mm, y * mm, f"Taxable: {tot_t:.2f}   {tax_note}")
    y -= 6
    c.drawString(20 * mm, y * mm, f"CGST: {tot_c:.2f}   SGST: {tot_s:.2f}   IGST: {tot_i:.2f}   Invoice total: Rs.{tot:.2f}")
    y -= 10
    c.setFont("Times-Roman", 9)
    c.drawString(20 * mm, y * mm, "Amount in words: as per total above. E. & O.E.")
    y -= 6
    c.drawString(20 * mm, y * mm, "Place of supply: Andhra Pradesh. Reverse charge: No.")
    c.showPage()
    c.save()


def write_bank(path):
    c = canvas.Canvas(str(path), pagesize=A4)
    _header(c, "HDFC BANK  —  ACCOUNT STATEMENT")
    c.setFont("Times-Roman", 10)
    lines = [
        "Account name: Example Traders Pvt Ltd",
        "Account no: 50200011223344",
        "IFSC: HDFC0001234    Branch: Vijayawada",
        "Period: 01-Apr-2026 to 30-Apr-2026",
        "Opening balance: 2,45,320.50 Cr",
        "",
        "Date        Narration                              Debit       Credit      Balance",
        "01-04-2026  NEFT/SHARMA TRADERS/INV ST-1042                    11,800.00   2,57,120.50",
        "03-04-2026  UPI/RENT/APR26                         25,000.00               2,32,120.50",
        "05-04-2026  IMPS/RAVI KIRANA/INV RK-88                         5,900.00    2,38,020.50",
        "08-04-2026  CHQ 001221/CASH WITHDRAWAL              10,000.00               2,28,020.50",
        "10-04-2026  NEFT/ELECTRICITY/APEPDCL                 8,450.00               2,19,570.50",
        "12-04-2026  RTGS/SALES/KRISHNA AGENCIES                        84,960.00   3,04,530.50",
        "15-04-2026  EMI/HDFC/CC-TERM LOAN                   18,750.00               2,85,780.50",
        "18-04-2026  UPI/UNKNOWN/Q12345                       3,200.00               2,82,580.50",
        "21-04-2026  SALARY/APR26                            95,000.00               1,87,580.50",
        "24-04-2026  GST/PMT/GSTR3B/APR26                    12,420.00               1,75,160.50",
        "28-04-2026  INT/CREDIT INTEREST                                  612.40    1,75,772.90",
        "30-04-2026  CHARGES/SMS+ATM                            118.00               1,75,654.90",
        "",
        "Closing balance: 1,75,654.90 Cr",
        "Unmatched items for books: UPI/UNKNOWN/Q12345 Rs.3,200; CHQ 001221 cash Rs.10,000.",
    ]
    y = 262
    for line in lines:
        c.drawString(18 * mm, y * mm, line)
        y -= 6
    c.showPage()
    c.save()


def main():
    buyer = "Example Traders Pvt Ltd"
    bgstin = "37AACTE1234F1Z5"
    write_invoice(
        INV / "INV-ST-1042-Sharma-Traders.pdf",
        inv_no="ST/1042",
        date="05-Apr-2026",
        vendor="Sharma Traders",
        vgstin="37AABCS1234Z1Z5",
        buyer=buyer,
        bgstin=bgstin,
        rows=[
            ("9988", "Packing material", 10, 1000.00, 10000.00, 900.00, 900.00, 0.00, 11800.00),
        ],
    )
    write_invoice(
        INV / "INV-RK-88-Ravi-Kirana.pdf",
        inv_no="RK/88",
        date="06-Apr-2026",
        vendor="Ravi Kirana Stores",
        vgstin="29AABCR9876K1Z3",
        buyer=buyer,
        bgstin=bgstin,
        igst=True,
        vendor_state="Karnataka",
        rows=[
            ("1905", "Tea and grocery", 20, 250.00, 5000.00, 0.00, 0.00, 900.00, 5900.00),
        ],
    )
    write_invoice(
        INV / "INV-ST-1042-duplicate.pdf",
        inv_no="ST/1042",
        date="05-Apr-2026",
        vendor="Sharma Traders",
        vgstin="37AABCS1234Z1Z5",
        buyer=buyer,
        bgstin=bgstin,
        rows=[
            ("9988", "Packing material", 10, 1000.00, 10000.00, 900.00, 900.00, 0.00, 11800.00),
        ],
    )
    write_bank(BANK / "HDFC-50200011223344-Apr-2026.pdf")
    print("Wrote samples to", INV, "and", BANK)


if __name__ == "__main__":
    main()
