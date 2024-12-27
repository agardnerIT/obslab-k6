import re
from playwright.sync_api import Page, expect

def test_log_in_to_dynatrace(page: Page):
    page.goto("https://dynatrace.com")
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Dynatrace"))

    # Click the get started link.
    page.get_by_role("link", name="Login").click()
    
    # Fill in user name and click next
    page.get_by_test_id("text-input").fill("someuser@example.com")
    page.get_by_role("button", name="Next").click()

