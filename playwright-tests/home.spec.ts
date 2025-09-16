import { test, expect } from '@playwright/test';

// Test that page title is correct

test('home page title', async ({ page }) => {
  // Navigate to the homepage. Base URL defined in playwright.config.ts
  await page.goto('/');
  await expect(page).toHaveTitle(/GuardPilot React UI/);
});
