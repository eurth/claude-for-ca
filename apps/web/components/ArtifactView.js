"use client";

const LABELS = {
  purchase_register: "Purchase register",
  sales_register: "Sales register",
  bank_ledger: "Bank ledger",
  exception_report: "Exceptions",
  master_accounts: "Master accounts",
  master_accounts_xlsx: "Master Accounts workbook",
  workbook: "Excel file",
  itc_recon: "ITC recon",
  gstr1_working: "GSTR-1 working",
  gstr3b_working: "GSTR-3B working",
  notice_summary: "Notice summary",
  draft_reply: "Draft reply",
  router_suggestion: "Suggested job",
  reused_context: "Reused from this client",
  tally_xml: "Tally import",
  purchase_invoice: "Invoice PDF",
  bank_pdf: "Bank PDF",
  upload: "Uploaded file",
};

function label(type) {
  return LABELS[type] || type.replaceAll("_", " ");
}

function pick(row, keys) {
  for (const key of keys) {
    if (row?.[key] !== undefined && row?.[key] !== null && row[key] !== "") return row[key];
  }
  return "";
}

function money(value) {
  if (value === "" || value === undefined || value === null) return "";
  const n = Number(value);
  if (Number.isNaN(n)) return String(value);
  return n.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function RegisterTable({ rows }) {
  if (!rows?.length) return <p className="muted">No invoice rows yet. Upload PDFs, then Run.</p>;
  return (
    <table className="register">
      <thead>
        <tr>
          <th>Vendor</th>
          <th>GSTIN</th>
          <th>Invoice</th>
          <th>Date</th>
          <th className="num">Taxable</th>
          <th className="num">CGST</th>
          <th className="num">SGST</th>
          <th className="num">IGST</th>
          <th className="num">Total</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i}>
            <td>{pick(row, ["vendor", "vendor_name"])}</td>
            <td>{pick(row, ["gstin", "vendor_gstin"])}</td>
            <td>{pick(row, ["invoice_no", "invoice_number"])}</td>
            <td>{pick(row, ["date", "invoice_date"])}</td>
            <td className="num">{money(pick(row, ["taxable_value", "taxable"]))}</td>
            <td className="num">{money(pick(row, ["cgst", "cgst_amount"]))}</td>
            <td className="num">{money(pick(row, ["sgst", "sgst_amount"]))}</td>
            <td className="num">{money(pick(row, ["igst", "igst_amount"]))}</td>
            <td className="num">{money(pick(row, ["total"]))}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function BankTable({ data }) {
  const rows = data?.rows || [];
  return (
    <>
      <p className="muted">
        Opening {money(data?.opening)} · Closing {money(data?.closing)}
      </p>
      {!rows.length ? (
        <p className="muted">No bank rows yet. Upload the statement PDF, then Run.</p>
      ) : (
        <table className="register">
          <thead>
            <tr>
              <th>Date</th>
              <th>Narration</th>
              <th className="num">Debit</th>
              <th className="num">Credit</th>
              <th className="num">Balance</th>
              <th>Category</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i}>
                <td>{row.date}</td>
                <td>{row.narration}</td>
                <td className="num">{money(row.debit)}</td>
                <td className="num">{money(row.credit)}</td>
                <td className="num">{money(row.balance)}</td>
                <td>{row.category}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}

function ExceptionList({ data }) {
  const items = data?.items || data?.flags || [];
  if (!items.length) return <p className="muted">No exceptions.</p>;
  return (
    <ul className="exceptions">
      {items.map((item, i) => (
        <li key={i}>{typeof item === "string" ? item : JSON.stringify(item)}</li>
      ))}
    </ul>
  );
}

export default function ArtifactView({ artifact, pack, onDownload, onExcel }) {
  const data = artifact.json || {};
  const rows = data.rows;
  const canExcel = Boolean(onExcel) && (rows?.length || artifact.has_file);
  return (
    <div className="card" style={{ marginBottom: "0.85rem" }}>
      <div className="row" style={{ justifyContent: "space-between" }}>
        <h3>
          {label(artifact.type)} {artifact.is_input ? "(uploaded)" : ""}
        </h3>
        <div className="row">
          {canExcel && artifact.type !== "tally_xml" ? (
            <button className="btn secondary" type="button" onClick={() => onExcel(artifact)}>
              Download Excel
            </button>
          ) : null}
          {artifact.has_file && (artifact.type !== "tally_xml" || pack.status === "approved") ? (
            <button className="btn secondary" type="button" onClick={() => onDownload(artifact)}>
              {artifact.type === "tally_xml" ? "Download for Tally" : "Download"}
            </button>
          ) : null}
          {artifact.type === "tally_xml" && pack.status !== "approved" ? (
            <span className="muted">Waiting for Partner approval</span>
          ) : null}
        </div>
      </div>
      {artifact.title && artifact.title !== label(artifact.type) ? (
        <p className="muted">{artifact.title}</p>
      ) : null}
      {artifact.type === "purchase_register" || artifact.type === "sales_register" || artifact.type === "itc_recon" ? (
        <RegisterTable rows={rows} />
      ) : artifact.type === "bank_ledger" ? (
        <BankTable data={data} />
      ) : artifact.type === "exception_report" ? (
        <ExceptionList data={data} />
      ) : artifact.type === "reused_context" ? (
        <p className="muted">{(data.titles || data.types || []).join(", ") || "Earlier working for this client and period."}</p>
      ) : artifact.type === "draft_reply" ? (
        <pre>{data.body || JSON.stringify(data, null, 2)}</pre>
      ) : artifact.json && !artifact.is_input ? (
        <pre>{JSON.stringify(data, null, 2).slice(0, 2000)}</pre>
      ) : null}
    </div>
  );
}
