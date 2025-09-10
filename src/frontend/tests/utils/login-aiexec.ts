import type { Page } from "playwright/test";

export const loginAiexec = async (page: Page) => {
  await page.goto("/");
  await page.getByPlaceholder("Username").fill("aiexec");
  await page.getByPlaceholder("Password").fill("aiexec");
  await page.getByRole("button", { name: "Sign In" }).click();
};
