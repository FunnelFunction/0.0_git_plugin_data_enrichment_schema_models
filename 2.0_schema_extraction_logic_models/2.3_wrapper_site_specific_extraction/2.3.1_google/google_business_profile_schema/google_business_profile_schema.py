"""
Google Business Profile Schema Extractor

Extraction schema for individual Google Business Profile detail pages.
Extracts comprehensive data from a single business listing.

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
from dataclasses import dataclass, field, asdict
from pathlib import Path

SELECTORS_PATH = Path(__file__).parent / "selectors.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google_business_profile_schema")


@dataclass
class GoogleBusinessProfileDataModel:
    """Data model for a Google Business Profile - Ghostless field naming"""
    business_name: str = ""
    address_full: str = ""
    address_street: str = ""
    address_city: str = ""
    address_state: str = ""
    address_zip: str = ""
    address_country: str = ""
    phone_number: str = ""
    website_url: str = ""
    website_display: str = ""
    rating_stars: Optional[float] = None
    review_count: Optional[int] = None
    price_level: str = ""
    category_primary: str = ""
    categories_all: list = field(default_factory=list)
    hours_status: str = ""
    hours_structured: dict = field(default_factory=dict)
    hours_special: list = field(default_factory=list)
    attributes: dict = field(default_factory=dict)
    photos_count: Optional[int] = None
    menu_url: str = ""
    reservation_url: str = ""
    order_url: str = ""
    owner_verified: bool = False
    place_id: str = ""
    plus_code: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    maps_url: str = ""
    extraction_timestamp: str = ""


class GoogleBusinessProfileExtractor:
    """
    Extractor for Google Business Profile detail pages.

    Usage:
        extractor = GoogleBusinessProfileExtractor(driver)
        writables = extractor.extract_profile_from_url(maps_url)
    """

    def __init__(self, selenium_webdriver=None, playwright_page=None):
        """
        Initialize with either Selenium WebDriver or Playwright Page.
        """
        self.driver = selenium_webdriver
        self.page = playwright_page
        self.selectors = self._load_selectors_from_json()

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
    # =========================================================================

    def extract_profile_from_url(self, maps_url: str) -> dict:
        """
        Main extraction entry point for a single business profile.

        Writables Flow:
            writables = navigate_to_profile_url()
            writables = wait_for_profile_to_load(writables)
            writables = extract_basic_info(writables)
            writables = extract_contact_info(writables)
            writables = extract_hours_info(writables)
            writables = extract_attributes(writables)
            writables = extract_action_links(writables)
            writables = extract_coordinates_from_url(writables)
            return writables
        """
        from datetime import datetime

        # Initialize writables as profile data model
        writables = GoogleBusinessProfileDataModel()
        writables.maps_url = maps_url
        writables.extraction_timestamp = datetime.utcnow().isoformat() + "Z"

        writables = self._navigate_to_profile_url(writables, maps_url)
        writables = self._wait_for_profile_to_load(writables)
        writables = self._extract_basic_business_info(writables)
        writables = self._extract_contact_info(writables)
        writables = self._extract_hours_info(writables)
        writables = self._extract_business_attributes(writables)
        writables = self._extract_action_links(writables)
        writables = self._extract_coordinates_and_place_id(writables)
        writables = self._parse_address_components(writables)

        logger.info(f"Extracted profile for: {writables.business_name}")
        return asdict(writables)

    def extract_profile_from_current_page(self) -> dict:
        """
        Extract profile data from the currently loaded page.
        Use this when you've already navigated to the profile.
        """
        from datetime import datetime

        writables = GoogleBusinessProfileDataModel()
        writables.extraction_timestamp = datetime.utcnow().isoformat() + "Z"

        # Get current URL
        if self.driver:
            writables.maps_url = self.driver.current_url
        elif self.page:
            writables.maps_url = self.page.url

        writables = self._extract_basic_business_info(writables)
        writables = self._extract_contact_info(writables)
        writables = self._extract_hours_info(writables)
        writables = self._extract_business_attributes(writables)
        writables = self._extract_action_links(writables)
        writables = self._extract_coordinates_and_place_id(writables)
        writables = self._parse_address_components(writables)

        return asdict(writables)

    def _navigate_to_profile_url(self, writables: GoogleBusinessProfileDataModel, url: str) -> GoogleBusinessProfileDataModel:
        """Navigate browser to profile URL"""
        if self.driver:
            self.driver.get(url)
        elif self.page:
            self.page.goto(url)

        logger.info(f"Navigated to profile: {url}")
        time.sleep(2)
        return writables

    def _wait_for_profile_to_load(self, writables: GoogleBusinessProfileDataModel) -> GoogleBusinessProfileDataModel:
        """Wait for profile header to load"""
        wait_config = self.selectors.get("wait_conditions", {}).get("profile_loaded", {})
        timeout = wait_config.get("timeout_seconds", 10)
        css_selector = wait_config.get("css", "h1.DUwDvf")

        if self.driver:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
            except Exception as wait_error:
                logger.warning(f"Timeout waiting for profile: {wait_error}")

        elif self.page:
            try:
                self.page.wait_for_selector(css_selector, timeout=timeout * 1000)
            except Exception as wait_error:
                logger.warning(f"Timeout waiting for profile: {wait_error}")

        return writables

    def _extract_basic_business_info(self, writables: GoogleBusinessProfileDataModel) -> GoogleBusinessProfileDataModel:
        """Extract basic business information"""
        selectors = self.selectors.get("selectors", {})

        # Business Name
        writables.business_name = self._extract_text_by_selector(
            selectors.get("business_name", {})
        )

        # Rating
        rating_text = self._extract_text_by_selector(selectors.get("rating_stars", {}))
        if rating_text:
            try:
                writables.rating_stars = float(rating_text.replace(",", "."))
            except ValueError:
                pass

        # Review Count
        review_text = self._extract_text_by_selector(selectors.get("review_count", {}))
        if review_text:
            numbers = re.findall(r'[\d,]+', review_text)
            if numbers:
                writables.review_count = int(numbers[0].replace(",", ""))

        # Category
        writables.category_primary = self._extract_text_by_selector(
            selectors.get("category_primary", {})
        )

        # Price Level
        writables.price_level = self._extract_text_by_selector(
            selectors.get("price_level", {})
        )

        # Plus Code
        writables.plus_code = self._extract_text_by_selector(
            selectors.get("plus_code", {})
        )

        # Photos Count
        photos_text = self._extract_text_by_selector(selectors.get("photos_count", {}))
        if photos_text:
            numbers = re.findall(r'[\d,]+', photos_text)
            if numbers:
                writables.photos_count = int(numbers[0].replace(",", ""))

        # Claimed/Verified Status
        claimed_text = self._extract_attribute_by_selector(
            selectors.get("claimed_status", {}), "aria-label"
        )
        writables.owner_verified = "claimed" in claimed_text.lower() if claimed_text else False

        return writables

    def _extract_contact_info(self, writables: GoogleBusinessProfileDataModel) -> GoogleBusinessProfileDataModel:
        """Extract contact information"""
        selectors = self.selectors.get("selectors", {})

        # Address
        writables.address_full = self._extract_text_by_selector(
            selectors.get("address_full", {})
        )

        # Phone
        writables.phone_number = self._extract_text_by_selector(
            selectors.get("phone_number", {})
        )

        # Website URL
        writables.website_url = self._extract_attribute_by_selector(
            selectors.get("website_url", {}), "href"
        )

        # Website Display Text
        writables.website_display = self._extract_text_by_selector(
            selectors.get("website_display", {})
        )

        return writables

    def _extract_hours_info(self, writables: GoogleBusinessProfileDataModel) -> GoogleBusinessProfileDataModel:
        """Extract business hours information"""
        selectors = self.selectors.get("selectors", {})

        # Current status (Open/Closed)
        writables.hours_status = self._extract_text_by_selector(
            selectors.get("hours_status", {})
        )

        # Click to expand hours if needed
        hours_button = selectors.get("hours_button", {})
        self._click_element_by_selector(hours_button)
        time.sleep(0.5)  # Wait for expansion

        # Extract hours table
        hours_rows_selector = selectors.get("hours_table_rows", {})
        hours_structured = {}

        if self.driver:
            rows = self.driver.find_elements("css selector", hours_rows_selector.get("css", ""))
            for row in rows:
                try:
                    day = row.find_element("css selector", "td:first-child").text.strip()
                    times_elements = row.find_elements("css selector", "td:last-child li")
                    times = [t.text.strip() for t in times_elements] if times_elements else [row.find_element("css selector", "td:last-child").text.strip()]
                    if day:
                        hours_structured[day.lower()] = times[0] if len(times) == 1 else times
                except Exception:
                    continue

        elif self.page:
            rows = self.page.query_selector_all(hours_rows_selector.get("css", ""))
            for row in rows:
                try:
                    day_el = row.query_selector("td:first-child")
                    times_els = row.query_selector_all("td:last-child li")
                    day = day_el.inner_text().strip() if day_el else ""
                    times = [t.inner_text().strip() for t in times_els] if times_els else []
                    if not times:
                        time_el = row.query_selector("td:last-child")
                        times = [time_el.inner_text().strip()] if time_el else []
                    if day:
                        hours_structured[day.lower()] = times[0] if len(times) == 1 else times
                except Exception:
                    continue

        writables.hours_structured = hours_structured
        return writables

    def _extract_business_attributes(self, writables: GoogleBusinessProfileDataModel) -> GoogleBusinessProfileDataModel:
        """Extract business attributes/amenities"""
        selectors = self.selectors.get("selectors", {})
        attributes = {}

        # Common attribute patterns to look for
        attribute_keywords = [
            "wheelchair", "wifi", "outdoor", "delivery", "takeout", "dine-in",
            "parking", "reservations", "credit cards", "dogs", "kids",
            "vegetarian", "vegan", "halal", "kosher"
        ]

        # Try to extract from attributes section
        attr_section_selector = selectors.get("attributes_section", {}).get("css", "")

        if self.driver and attr_section_selector:
            try:
                sections = self.driver.find_elements("css selector", attr_section_selector)
                for section in sections:
                    text = section.text.lower()
                    for keyword in attribute_keywords:
                        if keyword in text:
                            # Check if it's available or not
                            has_negative = any(neg in text for neg in ["no ", "not ", "doesn't"])
                            attributes[keyword] = not has_negative
            except Exception:
                pass

        elif self.page and attr_section_selector:
            try:
                sections = self.page.query_selector_all(attr_section_selector)
                for section in sections:
                    text = section.inner_text().lower()
                    for keyword in attribute_keywords:
                        if keyword in text:
                            has_negative = any(neg in text for neg in ["no ", "not ", "doesn't"])
                            attributes[keyword] = not has_negative
            except Exception:
                pass

        writables.attributes = attributes
        return writables

    def _extract_action_links(self, writables: GoogleBusinessProfileDataModel) -> GoogleBusinessProfileDataModel:
        """Extract menu, reservation, and order links"""
        selectors = self.selectors.get("selectors", {})

        writables.menu_url = self._extract_attribute_by_selector(
            selectors.get("menu_link", {}), "href"
        )

        writables.reservation_url = self._extract_attribute_by_selector(
            selectors.get("reservation_link", {}), "href"
        )

        writables.order_url = self._extract_attribute_by_selector(
            selectors.get("order_link", {}), "href"
        )

        return writables

    def _extract_coordinates_and_place_id(self, writables: GoogleBusinessProfileDataModel) -> GoogleBusinessProfileDataModel:
        """Extract coordinates and Place ID from URL"""
        url = writables.maps_url

        # Coordinates: @lat,lng pattern
        coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
        if coord_match:
            writables.latitude = float(coord_match.group(1))
            writables.longitude = float(coord_match.group(2))

        # Place ID pattern
        place_match = re.search(r'!1s(0x[a-f0-9]+:[a-f0-9x]+)', url)
        if place_match:
            writables.place_id = place_match.group(1)

        # Alternative Place ID pattern
        if not writables.place_id:
            alt_match = re.search(r'place_id=([A-Za-z0-9_-]+)', url)
            if alt_match:
                writables.place_id = alt_match.group(1)

        return writables

    def _parse_address_components(self, writables: GoogleBusinessProfileDataModel) -> GoogleBusinessProfileDataModel:
        """Parse address string into components"""
        address = writables.address_full
        if not address:
            return writables

        # Pattern: "123 Main St, City, ST 12345, Country"
        # or "123 Main St, City, ST 12345"
        patterns = [
            # With country
            r'^(.+?),\s*([^,]+),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?),\s*(.+)$',
            # Without country
            r'^(.+?),\s*([^,]+),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?)$',
            # Just street and city, state
            r'^(.+?),\s*([^,]+),\s*([A-Z]{2})$'
        ]

        for pattern in patterns:
            match = re.match(pattern, address.strip())
            if match:
                groups = match.groups()
                writables.address_street = groups[0].strip() if len(groups) > 0 else ""
                writables.address_city = groups[1].strip() if len(groups) > 1 else ""
                writables.address_state = groups[2].strip() if len(groups) > 2 else ""
                writables.address_zip = groups[3].strip() if len(groups) > 3 and groups[3] else ""
                writables.address_country = groups[4].strip() if len(groups) > 4 else "USA"
                break

        return writables

    # =========================================================================
    # Helper methods for element extraction
    # =========================================================================

    def _extract_text_by_selector(self, selector_config: dict) -> str:
        """Extract text using selector configuration"""
        css = selector_config.get("css", "")
        fallback_css = selector_config.get("fallback_css", "")

        for selector in [css, fallback_css]:
            if not selector:
                continue

            try:
                if self.driver:
                    elements = self.driver.find_elements("css selector", selector)
                    if elements:
                        return elements[0].text.strip()
                elif self.page:
                    element = self.page.query_selector(selector)
                    if element:
                        return element.inner_text().strip()
            except Exception:
                continue

        return ""

    def _extract_attribute_by_selector(self, selector_config: dict, attribute: str) -> str:
        """Extract attribute using selector configuration"""
        css = selector_config.get("css", "")

        if not css:
            return ""

        try:
            if self.driver:
                elements = self.driver.find_elements("css selector", css)
                if elements:
                    return elements[0].get_attribute(attribute) or ""
            elif self.page:
                element = self.page.query_selector(css)
                if element:
                    return element.get_attribute(attribute) or ""
        except Exception:
            pass

        return ""

    def _click_element_by_selector(self, selector_config: dict) -> bool:
        """Click element using selector configuration"""
        css = selector_config.get("css", "")

        if not css:
            return False

        try:
            if self.driver:
                elements = self.driver.find_elements("css selector", css)
                if elements:
                    elements[0].click()
                    return True
            elif self.page:
                element = self.page.query_selector(css)
                if element:
                    element.click()
                    return True
        except Exception:
            pass

        return False

    def export_writables_to_json_file(self, writables: dict, output_filepath: str) -> None:
        """Export extracted data to JSON file"""
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            json.dump(writables, output_file, indent=2, ensure_ascii=False)
        logger.info(f"Exported profile to {output_filepath}")


# =============================================================================
# Standalone execution example
# =============================================================================

if __name__ == "__main__":
    print("Google Business Profile Schema Extractor")
    print("=" * 50)
    print("\nUsage with Selenium:")
    print("""
    from selenium import webdriver
    from google_business_profile_schema import GoogleBusinessProfileExtractor

    driver = webdriver.Chrome()
    extractor = GoogleBusinessProfileExtractor(selenium_webdriver=driver)

    # Extract from a specific Maps URL
    profile_url = "https://www.google.com/maps/place/Starbucks/@25.7617,-80.1918,17z"
    writables = extractor.extract_profile_from_url(profile_url)

    extractor.export_writables_to_json_file(writables, "starbucks_profile.json")
    driver.quit()
    """)
