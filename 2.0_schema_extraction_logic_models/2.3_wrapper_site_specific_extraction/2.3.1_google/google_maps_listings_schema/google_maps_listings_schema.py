"""
Google Maps Listings Schema Extractor

Execution Model: 1.2_dynamic_browser_javascript_render_model
Requires: Selenium or Playwright with browser driver

Follows Intent Tensor Theory Coding Principles:
- Ghostless Coding: Semantically complete identifiers
- Writables Doctrine: Single-stream data pipeline
- PRE-X MetaMapping: Schema defines decisions before runtime
"""

import json
import re
import time
import logging
from typing import Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Load selectors from JSON schema
SELECTORS_PATH = Path(__file__).parent / "selectors.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google_maps_listings_schema")


@dataclass
class GoogleMapsListingDataModel:
    """Data model for a single Google Maps listing - Ghostless field naming"""
    business_name: str = ""
    address_full: str = ""
    address_street: str = ""
    address_city: str = ""
    address_state: str = ""
    address_zip: str = ""
    phone_number: str = ""
    website_url: str = ""
    rating_stars: Optional[float] = None
    review_count: Optional[int] = None
    category: str = ""
    hours_status: str = ""
    hours_json: Optional[dict] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_id: str = ""
    maps_url: str = ""
    price_level: str = ""
    plus_code: str = ""


class GoogleMapsListingsExtractor:
    """
    Extractor for Google Maps business listings.

    Usage:
        extractor = GoogleMapsListingsExtractor(driver)
        writables = extractor.extract_listings_by_query_and_location("plumbers", "miami fl")
    """

    def __init__(self, selenium_webdriver=None, playwright_page=None):
        """
        Initialize with either Selenium WebDriver or Playwright Page.

        Args:
            selenium_webdriver: Selenium WebDriver instance
            playwright_page: Playwright Page instance
        """
        self.driver = selenium_webdriver
        self.page = playwright_page
        self.selectors = self._load_selectors_from_json()

        if not self.driver and not self.page:
            logger.warning("No browser driver provided. Call set_driver() before extraction.")

    def _load_selectors_from_json(self) -> dict:
        """Load selector definitions from JSON schema file"""
        try:
            with open(SELECTORS_PATH, 'r') as selectors_file:
                return json.load(selectors_file)
        except FileNotFoundError:
            logger.error(f"Selectors file not found: {SELECTORS_PATH}")
            return {}

    def set_selenium_driver(self, driver) -> None:
        """Set Selenium WebDriver after initialization"""
        self.driver = driver
        self.page = None

    def set_playwright_page(self, page) -> None:
        """Set Playwright Page after initialization"""
        self.page = page
        self.driver = None

    # =========================================================================
    # WRITABLES DOCTRINE: Single-stream data pipeline
    # Each method receives writables, processes, and returns writables
    # =========================================================================

    def extract_listings_by_query_and_location(
        self,
        search_query: str,
        location: str,
        max_results: int = 20
    ) -> list[dict]:
        """
        Main extraction entry point.

        Writables Flow:
            writables = navigate_to_search()
            writables = wait_for_listings_to_load(writables)
            writables = scroll_to_load_more_listings(writables)
            writables = extract_all_listing_data(writables)
            writables = parse_address_components(writables)
            return writables
        """
        search_url = self._build_search_url_from_query_and_location(search_query, location)

        # Writables pipeline starts
        writables = []

        writables = self._navigate_to_search_url(search_url)
        writables = self._wait_for_listings_feed_to_load(writables)
        writables = self._scroll_feed_to_load_more_listings(writables, max_results)
        writables = self._extract_all_visible_listing_data(writables)
        writables = self._parse_address_components_for_all_listings(writables)
        writables = self._extract_coordinates_from_urls(writables)

        logger.info(f"Extracted {len(writables)} listings for '{search_query}' in '{location}'")
        return writables

    def _build_search_url_from_query_and_location(self, query: str, location: str) -> str:
        """Build Google Maps search URL from query and location"""
        search_term = f"{query}+{location}".replace(" ", "+")
        return f"https://www.google.com/maps/search/{search_term}"

    def _navigate_to_search_url(self, url: str) -> list:
        """Navigate browser to search URL"""
        writables = []

        if self.driver:
            self.driver.get(url)
        elif self.page:
            self.page.goto(url)

        logger.info(f"Navigated to: {url}")
        time.sleep(2)  # Initial page load delay
        return writables

    def _wait_for_listings_feed_to_load(self, writables: list) -> list:
        """Wait for the listings feed container to be present"""
        wait_config = self.selectors.get("wait_conditions", {}).get("listings_loaded", {})
        timeout = wait_config.get("timeout_seconds", 10)

        if self.driver:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_config.get("css", "div[role='feed']")))
                )
                logger.info("Listings feed loaded successfully")
            except Exception as wait_error:
                logger.warning(f"Timeout waiting for listings feed: {wait_error}")

        elif self.page:
            try:
                self.page.wait_for_selector(wait_config.get("css", "div[role='feed']"), timeout=timeout * 1000)
                logger.info("Listings feed loaded successfully")
            except Exception as wait_error:
                logger.warning(f"Timeout waiting for listings feed: {wait_error}")

        return writables

    def _scroll_feed_to_load_more_listings(self, writables: list, max_results: int) -> list:
        """Scroll the feed to load more listings via infinite scroll"""
        scroll_config = self.selectors.get("scroll_config", {})
        scroll_container_selector = scroll_config.get("scroll_container", "div[role='feed']")
        max_scrolls = scroll_config.get("max_scrolls", 20)
        scroll_delay_ms = scroll_config.get("scroll_delay_ms", 1000)

        scroll_count = 0
        previous_listing_count = 0

        while scroll_count < max_scrolls:
            if self.driver:
                # Selenium scroll
                feed_element = self.driver.find_elements("css selector", scroll_container_selector)
                if feed_element:
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight",
                        feed_element[0]
                    )
            elif self.page:
                # Playwright scroll
                self.page.evaluate(f"""
                    const feed = document.querySelector('{scroll_container_selector}');
                    if (feed) feed.scrollTop = feed.scrollHeight;
                """)

            time.sleep(scroll_delay_ms / 1000)
            scroll_count += 1

            # Check current listing count
            current_count = self._get_current_listing_count()

            if current_count >= max_results:
                logger.info(f"Reached max_results ({max_results}), stopping scroll")
                break

            if current_count == previous_listing_count:
                logger.info("No new listings loaded, stopping scroll")
                break

            previous_listing_count = current_count
            logger.info(f"Scroll {scroll_count}: {current_count} listings loaded")

        return writables

    def _get_current_listing_count(self) -> int:
        """Get count of currently loaded listings"""
        listing_selector = self.selectors.get("selectors", {}).get("listing_container", {}).get("css", "div.Nv2PK")

        if self.driver:
            elements = self.driver.find_elements("css selector", listing_selector)
            return len(elements)
        elif self.page:
            elements = self.page.query_selector_all(listing_selector)
            return len(elements)
        return 0

    def _extract_all_visible_listing_data(self, writables: list) -> list:
        """Extract data from all visible listings in the feed"""
        selectors = self.selectors.get("selectors", {})
        listing_container_css = selectors.get("listing_container", {}).get("css", "div.Nv2PK")

        if self.driver:
            listing_elements = self.driver.find_elements("css selector", listing_container_css)
        elif self.page:
            listing_elements = self.page.query_selector_all(listing_container_css)
        else:
            return writables

        for listing_element in listing_elements:
            listing_data = self._extract_single_listing_data(listing_element, selectors)
            writables.append(asdict(listing_data))

        return writables

    def _extract_single_listing_data(self, element, selectors: dict) -> GoogleMapsListingDataModel:
        """Extract data from a single listing element"""
        listing = GoogleMapsListingDataModel()

        # Business Name
        listing.business_name = self._safe_extract_text_from_element(
            element,
            selectors.get("business_name", {}).get("css", "")
        )

        # Rating Stars
        rating_text = self._safe_extract_text_from_element(
            element,
            selectors.get("rating_stars", {}).get("css", "")
        )
        if rating_text:
            try:
                listing.rating_stars = float(rating_text)
            except ValueError:
                pass

        # Review Count
        review_text = self._safe_extract_text_from_element(
            element,
            selectors.get("review_count", {}).get("css", "")
        )
        if review_text:
            numbers = re.findall(r'[\d,]+', review_text)
            if numbers:
                listing.review_count = int(numbers[0].replace(",", ""))

        # Category
        listing.category = self._safe_extract_text_from_element(
            element,
            selectors.get("category", {}).get("css", "")
        )

        # Address
        listing.address_full = self._safe_extract_text_from_element(
            element,
            selectors.get("address_full", {}).get("css", "")
        )

        # Phone Number
        listing.phone_number = self._safe_extract_text_from_element(
            element,
            selectors.get("phone_number", {}).get("css", "")
        )

        # Hours Status
        listing.hours_status = self._safe_extract_text_from_element(
            element,
            selectors.get("hours_status", {}).get("css", "")
        )

        # Listing URL (for place_id and coordinates)
        listing.maps_url = self._safe_extract_attribute_from_element(
            element,
            selectors.get("listing_link", {}).get("css", ""),
            "href"
        )

        return listing

    def _safe_extract_text_from_element(self, parent_element, css_selector: str) -> str:
        """Safely extract text from child element using CSS selector"""
        if not css_selector:
            return ""

        try:
            if self.driver:
                child = parent_element.find_elements("css selector", css_selector)
                if child:
                    return child[0].text.strip()
            elif self.page:
                child = parent_element.query_selector(css_selector)
                if child:
                    return child.inner_text().strip()
        except Exception as extraction_error:
            logger.debug(f"Failed to extract text with selector '{css_selector}': {extraction_error}")

        return ""

    def _safe_extract_attribute_from_element(self, parent_element, css_selector: str, attribute: str) -> str:
        """Safely extract attribute from child element using CSS selector"""
        if not css_selector:
            return ""

        try:
            if self.driver:
                child = parent_element.find_elements("css selector", css_selector)
                if child:
                    return child[0].get_attribute(attribute) or ""
            elif self.page:
                child = parent_element.query_selector(css_selector)
                if child:
                    return child.get_attribute(attribute) or ""
        except Exception as extraction_error:
            logger.debug(f"Failed to extract attribute '{attribute}' with selector '{css_selector}': {extraction_error}")

        return ""

    def _parse_address_components_for_all_listings(self, writables: list) -> list:
        """Parse address string into components for all listings"""
        for listing in writables:
            address_full = listing.get("address_full", "")
            if address_full:
                components = self._parse_address_string_to_components(address_full)
                listing["address_street"] = components.get("street", "")
                listing["address_city"] = components.get("city", "")
                listing["address_state"] = components.get("state", "")
                listing["address_zip"] = components.get("zip", "")

        return writables

    def _parse_address_string_to_components(self, address: str) -> dict:
        """Parse address string into street, city, state, zip components"""
        components = {"street": "", "city": "", "state": "", "zip": ""}

        # Pattern: "123 Main St, Miami, FL 33101"
        pattern = r'^(.+?),\s*([^,]+),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?)?$'
        match = re.match(pattern, address.strip())

        if match:
            components["street"] = match.group(1).strip()
            components["city"] = match.group(2).strip()
            components["state"] = match.group(3).strip()
            components["zip"] = match.group(4).strip() if match.group(4) else ""
        else:
            # Fallback: just store as street
            components["street"] = address

        return components

    def _extract_coordinates_from_urls(self, writables: list) -> list:
        """Extract latitude/longitude from Google Maps URLs"""
        for listing in writables:
            maps_url = listing.get("maps_url", "")
            if maps_url:
                # Pattern: @lat,lng,zoom
                coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', maps_url)
                if coord_match:
                    listing["latitude"] = float(coord_match.group(1))
                    listing["longitude"] = float(coord_match.group(2))

                # Extract place_id from URL
                place_match = re.search(r'/place/[^/]+/data=!3m1!4b1!4m[^!]+!3m[^!]+!1s(0x[a-f0-9]+:[a-f0-9x]+)', maps_url)
                if place_match:
                    listing["place_id"] = place_match.group(1)

        return writables

    def export_writables_to_json_file(self, writables: list, output_filepath: str) -> None:
        """Export extracted data to JSON file"""
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            json.dump(writables, output_file, indent=2, ensure_ascii=False)
        logger.info(f"Exported {len(writables)} listings to {output_filepath}")

    def export_writables_to_csv_file(self, writables: list, output_filepath: str) -> None:
        """Export extracted data to CSV file"""
        import csv

        if not writables:
            logger.warning("No data to export")
            return

        fieldnames = writables[0].keys()

        with open(output_filepath, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(writables)

        logger.info(f"Exported {len(writables)} listings to {output_filepath}")


# =============================================================================
# Standalone execution example
# =============================================================================

if __name__ == "__main__":
    print("Google Maps Listings Schema Extractor")
    print("=" * 50)
    print("\nUsage with Selenium:")
    print("""
    from selenium import webdriver
    from google_maps_listings_schema import GoogleMapsListingsExtractor

    driver = webdriver.Chrome()
    extractor = GoogleMapsListingsExtractor(selenium_webdriver=driver)

    writables = extractor.extract_listings_by_query_and_location(
        search_query="plumbers",
        location="miami fl",
        max_results=20
    )

    extractor.export_writables_to_json_file(writables, "output.json")
    driver.quit()
    """)

    print("\nUsage with Playwright:")
    print("""
    from playwright.sync_api import sync_playwright
    from google_maps_listings_schema import GoogleMapsListingsExtractor

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        extractor = GoogleMapsListingsExtractor(playwright_page=page)

        writables = extractor.extract_listings_by_query_and_location(
            search_query="restaurants",
            location="new york ny",
            max_results=50
        )

        extractor.export_writables_to_json_file(writables, "restaurants.json")
        browser.close()
    """)
