import re
from playwright.sync_api import Playwright, Page, expect, FrameLocator, Locator
import pytest
import os
from loguru import logger
import time

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
    expect(frame.get_by_test_id("page-panel-main")).to_be_visible(timeout=10000)
    return frame

def create_new_document(page: Page, app_frame: FrameLocator):
    app_frame.get_by_test_id("new-document-button").click()
    expect(app_frame.get_by_label("Add section").first).to_be_visible(timeout=15000)
    app_frame.get_by_label("Add section").first.wait_for(timeout=15000)

def add_document_section(page, app_frame: FrameLocator, section_type_text):

    # Wait for stuff to load
    expect(app_frame.get_by_label("Add section").first.or_(app_frame.get_by_label("Add section at the start of the notebook")).first).to_be_visible(timeout=15000)

    #add_section_element = app_frame.get_by_label("Add section").first
    #add_section_element.wait_for(timeout=10000)
    #add_section_element.click()
    # Annoyingly an empty document "Add section +" button is "add-section-menu-label"
    # But a document with an existing section has two buttons:
    # - "Add section at the start of the notebook"
    # - "Add section at the end of the notebook"
    # Key combinations like Shift+D automatically
    # add new sections to the end of the document
    # We should always check .last for data
    # Special treatment for section types with key combo shortcuts:
    # DQL: Shift+D
    # Code: Shift+C
    # Markdown: Shift+M
    if section_type_text == "DQL":
        logger.info("Using key combination Shift+D for DQL tile")
        page.keyboard.press("Shift+D")
    elif section_type_text == "Code":
        logger.info("Using key combination Shift+C for Code tile")
        page.keyboard.press("Shift+C")
    elif section_type_text == "Markdown":
        logger.info("Using key combination Shift+M for Markdown tile")
        page.keyboard.press("Shift+M")
    else:
        page.keyboard.press("ControlOrMeta+Shift+Enter")
        expect(app_frame.get_by_text("Create new section")).to_be_visible(timeout=10000)
        logger.info(f"Clicking {section_type_text}")
        app_frame.get_by_text(section_type_text, exact=False).first.click(timeout=10000)

def enter_dql_query(app_frame, dql_query):
    app_frame.get_by_label("Enter a DQL query").type(dql_query)

def validate_document_section_has_data(app_frame: FrameLocator, section_index):
    
    section = app_frame.locator(f"[data-testid-section-index=\"{section_index}\"]")

    # Click the Run button
    section.get_by_test_id("run-query-button").click()

    # wait for DQL to finish
    # if this times out, either query took too long
    # of the query was invalid
    try:
        section.get_by_test_id("result-container").wait_for(timeout=30000)
    except:
        pytest.fail("Either query timed out or an invalid query was provided.")


    # If we get here
    # query executed and now let's
    # see if there valid data returned

    # Try to find the "no data" <h6>
    # Remember, NOT finding this is actually a good thing
    # Because then you DO have data
    no_data_heading = app_frame.locator("h6")
    # If the chart graphic does not appear
    # Then the data is not available in Dynatrace
    # and we should error and exit.
    if no_data_heading.is_visible(timeout=5000) and no_data_heading.inner_html(timeout=5000) == "There are no records":
        pytest.fail(f"No data found in section_index={section_index}")
    else:
        logger.debug(f"[DEBUG] Data found in section_index={section_index}")

# Specific function to add a metric to a metric type chart
# Note: This does NOT click the "Run query" button
# For data validation, use the valudate_document_section_has_data function
def add_metric(app_frame, search_term, metric_text):
    app_frame.get_by_label("Select metric").first.click()
    logger.info(f"Selecting {search_term} from list")    
    # logger.info("Clicking `Select metric` button")
    # app_frame.get_by_label("Select metric").first.click()
    logger.info(f"Typing `{search_term}` into the box")
    app_frame.get_by_test_id("text-input").fill(search_term)
    # Add the metric to the metric chart
    app_frame.get_by_label(metric_text).last.click()
    
@pytest.mark.timeout(TEST_TIMEOUT_SECONDS)
def test_dynatrace_ui(page: Page):

    app_name = "notebooks"

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
    search_term = "k6"
    metric_text = "k6.vus"
    logger.info(f"Adding a new {app_name} section")
    add_document_section(page=page, app_frame=app_frame, section_type_text="Metrics")
    add_metric(app_frame=app_frame, search_term=search_term, metric_text=metric_text)

    ################################################
    validate_document_section_has_data(app_frame=app_frame, section_index="0")

    add_document_section(page=page, app_frame=app_frame, section_type_text="DQL")
    enter_dql_query(app_frame, dql_query='fetch events\n| filter event.kind == "SDLC_EVENT"\n| filter event.provider == "k6"')
    validate_document_section_has_data(app_frame=app_frame, section_index="1")