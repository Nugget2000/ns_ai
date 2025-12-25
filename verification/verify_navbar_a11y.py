from playwright.sync_api import Page, expect, sync_playwright

def verify_navbar_a11y(page: Page):
    # 1. Arrange: Go to the home page
    page.goto("http://localhost:3000")

    # 2. Act: Set viewport to mobile to see the mobile menu button
    page.set_viewport_size({"width": 375, "height": 667})

    # 3. Assert: Check for the mobile menu button with specific ARIA label
    mobile_menu_button = page.get_by_role("button", name="Toggle navigation menu")
    expect(mobile_menu_button).to_be_visible()

    # Check initial state (aria-expanded="false")
    expect(mobile_menu_button).to_have_attribute("aria-expanded", "false")

    # Click it
    mobile_menu_button.click()

    # Check expanded state (aria-expanded="true")
    expect(mobile_menu_button).to_have_attribute("aria-expanded", "true")

    # 4. Screenshot
    page.screenshot(path="verification/navbar_a11y.png")
    print("Verification successful: ARIA label and expanded state confirmed.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_navbar_a11y(page)
        finally:
            browser.close()
