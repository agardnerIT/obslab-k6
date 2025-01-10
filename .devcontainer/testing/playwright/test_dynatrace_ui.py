import re
from playwright.sync_api import Playwright, Page, expect, Locator, FrameLocator
import pytest
import os
from loguru import logger

TESTING_DYNATRACE_TENANT_ID = os.environ.get("TESTING_DYNATRACE_TENANT_ID", "")
TESTING_DYNATRACE_USER_EMAIL = os.environ.get("TESTING_DYNATRACE_USER_EMAIL", "")
TESTING_DYNATRACE_USER_PASSWORD = os.environ.get("TESTING_DYNATRACE_USER_PASSWORD", "")
TEST_TIMEOUT_SECONDS = os.environ.get("TESTING_TIMEOUT_SECONDS", 60)

if TESTING_DYNATRACE_TENANT_ID == "" or TESTING_DYNATRACE_USER_EMAIL == "" or TESTING_DYNATRACE_USER_PASSWORD == "":
    print("MISSING MANDATORY ENV VARS. EXITING.")
    exit()

def login(page: Page):
    # Navigate to dynatrace.com
    page.goto("https://dynatrace.com")
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Dynatrace"))

    # Click the get started link.
    page.get_by_role("link", name="Login").click()
    
    # Fill in user name and click next
    page.get_by_test_id("text-input").fill(TESTING_DYNATRACE_USER_EMAIL)
    page.wait_for_selector('[data-id="email_submit"]').click()

    # Fill in password and Sign in
    page.locator('[data-id="password_login"]').fill(TESTING_DYNATRACE_USER_PASSWORD)
    page.locator('[data-id="sign_in"]').click()

    # Expect a title to contain the tenant ID
    # Wait for all login related redirects to finish
    # Then assert on the page which should contain the tenant ID
    page.wait_for_url("**/ui/**")
    expect(page).to_have_title(re.compile(TESTING_DYNATRACE_TENANT_ID))

def open_search_menu(page: Page):
    page.get_by_test_id("dock-search").click()
    # Expect the Search modal to be visible
    expect(page.get_by_test_id("search-base-modal-content")).to_be_visible()

def search_for(page: Page, search_term: str):
    # Type in "notebooks"
    page.get_by_label("Search query").fill(search_term)

    # Wait for search results
    expect(page.get_by_label("Result list")).to_be_visible()

def open_app_from_search_modal(page: Page, app_name: str):
    page.locator(f"[id='apps:dynatrace.{app_name}']").click()
    page.wait_for_url(f"**/dynatrace.{app_name}/**")
    expect(page).to_have_title(re.compile(app_name, re.IGNORECASE))

def wait_for_app_frame_to_load(page: Page):
    frame = page.frame_locator('[data-testid="app-iframe"]')
    expect(frame.get_by_test_id("page-panel-main")).to_be_visible()
    return frame

def create_new_document(page: Page, app_frame: FrameLocator):
    app_frame.get_by_test_id("new-document-button").click()
    expect(app_frame.get_by_label("Add section").first).to_be_visible()

def add_document_section(app_frame: FrameLocator):
    add_section_element = app_frame.get_by_label("Add section").first
    add_section_element.wait_for(timeout=10000)
    add_section_element.click()
    expect(app_frame.get_by_text("Create new section")).to_be_visible()

def validate_document_section_has_data(app_frame: FrameLocator, search_term: str):
    # Validate the search results have multiple results
    #search_result_list = page.get_by_test_id("virtualized-list")
    parent_element = app_frame.get_by_test_id("virtualized-list")
    parent_element.wait_for()
    span_locators = parent_element.locator("span")
    spans = span_locators.all()

    if len(spans) < 1:
        pytest.fail(f"No search results for {search_term} found")

    first_search_result = spans[0]
    if search_term not in first_search_result.inner_html().lower():
        pytest.fail(f"Got a search result but first item in list did not contain {search_term}")
    
    # Click the first search result
    first_search_result.click()

    # Click the Run button
    app_frame.get_by_test_id("run-query-button").click()

    # wait for DQL to finish
    app_frame.get_by_test_id("result-container").wait_for()

    # Try to find the "no data" <h6>
    # Remember, NOT finding this is actually a good thing
    # Because then you DO have data
    no_data_heading = app_frame.locator("h6")
    # If the chart graphic does not appear
    # Then the data is not available in Dynatrace
    # and we should error and exit.
    if no_data_heading.is_visible() and no_data_heading.inner_html(timeout=1000) == "There are no records":
        pytest.fail("No data found!")

@pytest.mark.timeout(TEST_TIMEOUT_SECONDS)
def test_dynatrace_ui(page: Page):

    app_name = "notebooks"

    ################################################
    logger.info("STARTING TEST")

    ################################################
    logger.info("Logging in")
    login(page)

    ################################################
    logger.info("Opening search menu")
    open_search_menu(page)
    
    ################################################
    logger.info(f"Searching for {app_name}")
    search_for(page, app_name)

    ################################################
    logger.info(f"Opening {app_name} app")
    open_app_from_search_modal(page, app_name)

    ################################################
    logger.info(f"Waiting for {app_name} app to show")
    app_frame = wait_for_app_frame_to_load(page)
    logger.info(f"{app_name} app is now displayed")

    ################################################
    logger.info(f"Creating a new document: ({app_name})")
    create_new_document(page, app_frame)
    
    ################################################
    logger.info(f"Adding a new {app_name} section")
    add_document_section(app_frame)

    ################################################
    search_term = "cpu"
    logger.info(f"Selecting {search_term} from list")
    
    logger.info("Clicking `Metrics`")
    app_frame.get_by_text("Metrics", exact=True).click()
    logger.info("Clicking `Select metric` button")
    app_frame.get_by_label("Metric key").first.click()
    logger.info(f"Typing `{search_term}` into the box")
    app_frame.get_by_test_id("text-input").fill(search_term)

    
    ################################################
    validate_document_section_has_data(app_frame, search_term)