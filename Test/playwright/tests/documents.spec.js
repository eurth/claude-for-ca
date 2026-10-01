const path = require("path");
const { test, expect } = require("@playwright/test");

const invoice = path.resolve(__dirname, "../../samples/invoices/INV-ST-1042-Sharma-Traders.pdf");
const bank = path.resolve(__dirname, "../../samples/bank/HDFC-50200011223344-Apr-2026.pdf");

async function signIn(page) {
  await page.goto("/login");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByText("Gorantla Associates")).toBeVisible();
}

test("extract invoice PDF produces a purchase output", async ({ page }) => {
  await signIn(page);
  await page.goto("/features");
  await page.getByRole("button", { name: /Extract invoices/ }).click();
  await expect(page).toHaveURL(/\/workpacks\//, { timeout: 30000 });
  await page.locator('input[type="file"]').setInputFiles(invoice);
  await page.getByRole("button", { name: /Run/ }).click();
  await expect(page.getByRole("heading", { name: "Summary" })).toBeVisible({ timeout: 150000 });
  await expect(page.getByText(/Sharma Traders|ST\/1042|packing material/i).first()).toBeVisible();
});

test("bank statement PDF produces a ledger or summary", async ({ page }) => {
  await signIn(page);
  await page.goto("/features");
  await page.getByRole("button", { name: /Process bank statement/ }).click();
  await expect(page).toHaveURL(/\/workpacks\//, { timeout: 30000 });
  await page.locator('input[type="file"]').setInputFiles(bank);
  await page.getByRole("button", { name: /Run/ }).click();
  await expect(page.getByRole("heading", { name: "Summary" })).toBeVisible({ timeout: 150000 });
  await expect(page.getByText(/Extracted 12 bank rows/i)).toBeVisible();
  await expect(page.getByRole("cell", { name: /HDFC-50200011223344/ })).toBeVisible();
});
