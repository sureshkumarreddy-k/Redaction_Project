import time

from playwright.sync_api import sync_playwright

from excel_utils import get_test_data

def test_ui_page_load():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        # Open application
        page.goto("http://127.0.0.1:8000")

        page.wait_for_timeout(3000)

        # Validate page title
        assert "Stored Messages" in page.title()

        # Validate textbox visible
        assert page.locator(
            'input[name="message"]'
        ).is_visible()

        # Validate button visible
        assert page.get_by_role(
            "button",
            name="Redact"
        ).is_visible()

        browser.close()


def test_delete_message():

    unique_email = f"test{int(time.time())}@gmail.com"

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        page = browser.new_page()

        # Open application
        page.goto("http://127.0.0.1:8000")

        # Enter message
        page.fill(
            'input[name="message"]',
            unique_email
        )

        # Click redact button
        page.get_by_role(
            "button",
            name="Redact"
        ).click()

        page.wait_for_timeout(3000)

        # Count rows before delete
        rows_before = page.locator(
            "table tr"
        ).count()

        # Delete last row
        page.locator(
            ".delete-btn"
        ).last.click()

        page.wait_for_timeout(3000)

        # Count rows after delete
        rows_after = page.locator(
            "table tr"
        ).count()

        # Validate row deleted
        assert rows_after == rows_before - 1

        browser.close()

def test_empty_input():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        page = browser.new_page()

        # Open application
        page.goto("http://127.0.0.1:8000")

        # Enter only spaces
        page.fill(
            'input[name="message"]',
            "     "
        )

        # Click redact
        page.get_by_role(
            "button",
            name="Redact"
        ).click()

        page.wait_for_timeout(3000)

        content = page.content()

        # Validate empty message validation
        assert "Message cannot be empty" in content

        browser.close()

def test_redaction_from_excel():

    test_data = get_test_data()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        page = browser.new_page()

        for message, expected in test_data:

            # Open application
            page.goto("http://127.0.0.1:8000")

            page.wait_for_timeout(2000)

            # Enter message from excel
            page.fill(
                'input[name="message"]',
                message
            )

            # Click redact button
            page.get_by_role(
                "button",
                name="Redact"
            ).click()

            page.wait_for_timeout(3000)

            content = page.content()

            # Validate expected output
            expected_values = expected.split(",")

            for value in expected_values:
                assert value.strip() in content

            print(f"Validated: {message}")

        browser.close()