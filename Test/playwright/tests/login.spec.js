const { test, expect } = require("@playwright/test");

test("partner can sign in", async ({ page }) => {
  await page.goto("/login");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByText("Gorantla Associates")).toBeVisible();
});
