import { test, expect } from '@playwright/test';

test.describe('Authentication and Dashboard Flow', () => {
  test('User can log in and see their balance', async ({ page }) => {
    // 1. Go to the login page
    await page.goto('/login');

    // 2. Fill in the credentials for John Doe
    await page.fill('input[placeholder="john.doe@email.com"]', 'john.doe@email.com');
    await page.fill('input[placeholder="Challenge@123"]', 'Challenge@123');

    // 3. Click the Sign In button
    await page.click('button:has-text("Sign in")');

    // 4. Wait for the dashboard to load and verify the URL
    await expect(page).toHaveURL(/.*dashboard/);

    // 5. Verify the balance and total transactions are displayed correctly
    await expect(page.locator('text=$15,491.00')).toBeVisible();
    await expect(page.locator('text=Total Transactions')).toBeVisible();
    await expect(page.locator('text=5').first()).toBeVisible();

    // 6. Verify that the Hide Balance button works
    await page.click('button:has-text("Hide")');
    await expect(page.locator('text=••••••')).toBeVisible();

    // 7. Verify pagination (Next/Previous buttons)
    await expect(page.locator('button:has-text("Previous")')).toBeDisabled();
  });
});