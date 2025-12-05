"""
Google Search Results Schema Extractor

Extraction schema for Google Search Results Pages (SERPs).
Extracts organic results, ads, featured snippets, and SERP features.

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
from urllib.parse import urlencode, urlparse, parse_qs
from typing import Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path

SELECTORS_PATH = Path(__file__).parent / "selectors.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google_search_results_schema")


@dataclass
class OrganicResultDataModel:
    """Data model for a single organic search result"""
    position: int = 0
    title: str = ""
    url: str = ""
    displayed_url: str = ""
    description: str = ""
    date_published: str = ""
    rich_snippet: dict = field(default_factory=dict)


@dataclass
class AdResultDataModel:
    """Data model for a sponsored/ad result"""
    position: int = 0
    title: str = ""
    url: str = ""
    displayed_url: str = ""
    description: str = ""
    ad_extensions: list = field(default_factory=list)


@dataclass
class FeaturedSnippetDataModel:
    """Data model for featured snippet"""
    content: str = ""
    source_title: str = ""
    source_url: str = ""


@dataclass
class LocalPackResultDataModel:
    """Data model for local pack result"""
    position: int = 0
    business_name: str = ""
    rating: Optional[float] = None
    review_count: Optional[int] = None
    category: str = ""
    address: str = ""


@dataclass
class GoogleSearchResultsDataModel:
    """Complete data model for Google SERP - Ghostless field naming"""
    query: str = ""
    search_url: str = ""
    results_count_text: str = ""
    results_count_estimated: Optional[int] = None
    current_page: int = 1
    organic_results: list = field(default_factory=list)
    ads_top: list = field(default_factory=list)
    ads_bottom: list = field(default_factory=list)
    featured_snippet: Optional[dict] = None
    people_also_ask: list = field(default_factory=list)
    related_searches: list = field(default_factory=list)
    local_pack: list = field(default_factory=list)
    knowledge_panel: Optional[dict] = None
    has_next_page: bool = False
    next_page_url: str = ""
    extraction_timestamp: str = ""


class GoogleSearchResultsExtractor:
    """
    Extractor for Google Search Results Pages.

    Usage:
        extractor = GoogleSearchResultsExtractor(driver)
        writables = extractor.extract_results_by_query("plumbers miami")
    """

    def __init__(self, selenium_webdriver=None, playwright_page=None):
        """Initialize with either Selenium WebDriver or Playwright Page."""
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

    def extract_results_by_query(
        self,
        search_query: str,
        results_per_page: int = 10,
        max_pages: int = 1
    ) -> list[dict]:
        """
        Main extraction entry point.

        Writables Flow:
            writables = navigate_to_search()
            writables = check_for_captcha(writables)
            writables = extract_all_serp_features(writables)
            writables = paginate_if_needed(writables)
            return writables
        """
        all_results = []

        for page_num in range(1, max_pages + 1):
            search_url = self._build_search_url(search_query, results_per_page, page_num)

            writables = self._extract_single_page(search_query, search_url, page_num)
            all_results.append(writables)

            # Check if there's a next page
            if not writables.get("has_next_page", False) or page_num >= max_pages:
                break

            # Delay between pages
            time.sleep(3)

        logger.info(f"Extracted {len(all_results)} page(s) for query: '{search_query}'")
        return all_results

    def _extract_single_page(self, query: str, url: str, page_num: int) -> dict:
        """Extract all data from a single SERP page"""
        from datetime import datetime

        writables = GoogleSearchResultsDataModel()
        writables.query = query
        writables.search_url = url
        writables.current_page = page_num
        writables.extraction_timestamp = datetime.utcnow().isoformat() + "Z"

        writables = self._navigate_to_search_url(writables, url)
        writables = self._wait_for_results_to_load(writables)

        # Check for CAPTCHA
        if self._check_for_captcha():
            logger.warning("CAPTCHA detected! Manual intervention required.")
            return asdict(writables)

        writables = self._extract_search_stats(writables)
        writables = self._extract_organic_results(writables)
        writables = self._extract_ad_results(writables)
        writables = self._extract_featured_snippet(writables)
        writables = self._extract_people_also_ask(writables)
        writables = self._extract_related_searches(writables)
        writables = self._extract_local_pack(writables)
        writables = self._extract_knowledge_panel(writables)
        writables = self._extract_pagination_info(writables)

        return asdict(writables)

    def _build_search_url(self, query: str, num: int, page: int) -> str:
        """Build Google search URL with parameters"""
        params = {
            "q": query,
            "num": num
        }

        if page > 1:
            params["start"] = (page - 1) * num

        return f"https://www.google.com/search?{urlencode(params)}"

    def _navigate_to_search_url(self, writables: GoogleSearchResultsDataModel, url: str) -> GoogleSearchResultsDataModel:
        """Navigate browser to search URL"""
        if self.driver:
            self.driver.get(url)
        elif self.page:
            self.page.goto(url)

        logger.info(f"Navigated to: {url}")
        time.sleep(2)
        return writables

    def _wait_for_results_to_load(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Wait for search results container to load"""
        wait_config = self.selectors.get("wait_conditions", {}).get("results_loaded", {})
        timeout = wait_config.get("timeout_seconds", 10)
        css_selector = wait_config.get("css", "div#search")

        if self.driver:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
            except Exception:
                logger.warning("Timeout waiting for search results")

        elif self.page:
            try:
                self.page.wait_for_selector(css_selector, timeout=timeout * 1000)
            except Exception:
                logger.warning("Timeout waiting for search results")

        return writables

    def _check_for_captcha(self) -> bool:
        """Check if CAPTCHA is present"""
        captcha_css = self.selectors.get("wait_conditions", {}).get("captcha_check", {}).get("css", "")

        if self.driver:
            elements = self.driver.find_elements("css selector", captcha_css)
            return len(elements) > 0
        elif self.page:
            element = self.page.query_selector(captcha_css)
            return element is not None

        return False

    def _extract_search_stats(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract search statistics (results count)"""
        stats_css = self.selectors.get("selectors", {}).get("search_stats", {}).get("results_count", {}).get("css", "")

        text = self._extract_text(stats_css)
        writables.results_count_text = text

        # Parse estimated count
        if text:
            match = re.search(r'About ([\d,]+) results', text)
            if match:
                writables.results_count_estimated = int(match.group(1).replace(",", ""))

        return writables

    def _extract_organic_results(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract organic search results"""
        selectors = self.selectors.get("selectors", {}).get("organic_results", {})
        container_css = selectors.get("container", {}).get("css", "")

        results = []

        if self.driver:
            elements = self.driver.find_elements("css selector", container_css)
        elif self.page:
            elements = self.page.query_selector_all(container_css)
        else:
            elements = []

        for idx, element in enumerate(elements, 1):
            result = OrganicResultDataModel(position=idx)

            result.title = self._extract_child_text(element, selectors.get("title", {}).get("css", ""))
            result.url = self._extract_child_attribute(element, selectors.get("url", {}).get("css", ""), "href")
            result.displayed_url = self._extract_child_text(element, selectors.get("displayed_url", {}).get("css", ""))
            result.description = self._extract_child_text(element, selectors.get("description", {}).get("css", ""))
            result.date_published = self._extract_child_text(element, selectors.get("date_published", {}).get("css", ""))

            # Rich snippet data
            rich_selectors = self.selectors.get("selectors", {}).get("rich_snippets", {})
            rating = self._extract_child_text(element, rich_selectors.get("rating_stars", {}).get("css", ""))
            if rating:
                result.rich_snippet["rating"] = rating

            review_count = self._extract_child_text(element, rich_selectors.get("rating_count", {}).get("css", ""))
            if review_count:
                result.rich_snippet["review_count"] = review_count

            price = self._extract_child_text(element, rich_selectors.get("price", {}).get("css", ""))
            if price:
                result.rich_snippet["price"] = price

            # Only add if we have a title and URL
            if result.title and result.url:
                results.append(asdict(result))

        writables.organic_results = results
        logger.info(f"Extracted {len(results)} organic results")
        return writables

    def _extract_ad_results(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract sponsored/ad results"""
        selectors = self.selectors.get("selectors", {}).get("ads", {})
        container_css = selectors.get("container", {}).get("css", "")

        ads = []

        if self.driver:
            elements = self.driver.find_elements("css selector", container_css)
        elif self.page:
            elements = self.page.query_selector_all(container_css)
        else:
            elements = []

        for idx, element in enumerate(elements, 1):
            ad = AdResultDataModel(position=idx)

            ad.title = self._extract_child_text(element, selectors.get("title", {}).get("css", ""))
            ad.url = self._extract_child_attribute(element, selectors.get("url", {}).get("css", ""), "href")
            ad.displayed_url = self._extract_child_text(element, selectors.get("displayed_url", {}).get("css", ""))
            ad.description = self._extract_child_text(element, selectors.get("description", {}).get("css", ""))

            if ad.title:
                ads.append(asdict(ad))

        writables.ads_top = ads
        logger.info(f"Extracted {len(ads)} ads")
        return writables

    def _extract_featured_snippet(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract featured snippet if present"""
        selectors = self.selectors.get("selectors", {}).get("featured_snippet", {})
        container_css = selectors.get("container", {}).get("css", "")

        if self.driver:
            container = self.driver.find_elements("css selector", container_css)
        elif self.page:
            container = self.page.query_selector(container_css)
        else:
            container = None

        if container:
            snippet = FeaturedSnippetDataModel()
            snippet.content = self._extract_text(selectors.get("content", {}).get("css", ""))
            snippet.source_title = self._extract_text(selectors.get("source_title", {}).get("css", ""))
            snippet.source_url = self._extract_attribute(selectors.get("source_url", {}).get("css", ""), "href")

            if snippet.content:
                writables.featured_snippet = asdict(snippet)
                logger.info("Extracted featured snippet")

        return writables

    def _extract_people_also_ask(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract People Also Ask questions"""
        selectors = self.selectors.get("selectors", {}).get("people_also_ask", {})
        container_css = selectors.get("container", {}).get("css", "")
        question_css = selectors.get("question", {}).get("css", "")

        questions = []

        if self.driver:
            elements = self.driver.find_elements("css selector", container_css)
            for el in elements:
                text = self._extract_child_text(el, question_css)
                if text:
                    questions.append(text)
        elif self.page:
            elements = self.page.query_selector_all(container_css)
            for el in elements:
                q = el.query_selector(question_css)
                if q:
                    questions.append(q.inner_text().strip())

        writables.people_also_ask = questions
        return writables

    def _extract_related_searches(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract related searches"""
        selectors = self.selectors.get("selectors", {}).get("related_searches", {})
        container_css = selectors.get("container", {}).get("css", "")

        related = []

        if self.driver:
            elements = self.driver.find_elements("css selector", container_css)
            for el in elements:
                text = el.text.strip()
                if text:
                    related.append(text)
        elif self.page:
            elements = self.page.query_selector_all(container_css)
            for el in elements:
                text = el.inner_text().strip()
                if text:
                    related.append(text)

        writables.related_searches = related
        return writables

    def _extract_local_pack(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract local pack (3-pack) results"""
        selectors = self.selectors.get("selectors", {}).get("local_pack", {})
        container_css = selectors.get("container", {}).get("css", "")

        local_results = []

        if self.driver:
            elements = self.driver.find_elements("css selector", container_css)
        elif self.page:
            elements = self.page.query_selector_all(container_css)
        else:
            elements = []

        for idx, element in enumerate(elements, 1):
            local = LocalPackResultDataModel(position=idx)
            local.business_name = self._extract_child_text(element, selectors.get("business_name", {}).get("css", ""))
            rating_text = self._extract_child_text(element, selectors.get("rating", {}).get("css", ""))
            if rating_text:
                try:
                    local.rating = float(rating_text)
                except ValueError:
                    pass
            local.category = self._extract_child_text(element, selectors.get("category", {}).get("css", ""))
            local.address = self._extract_child_text(element, selectors.get("address", {}).get("css", ""))

            if local.business_name:
                local_results.append(asdict(local))

        writables.local_pack = local_results
        return writables

    def _extract_knowledge_panel(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract knowledge panel data"""
        selectors = self.selectors.get("selectors", {}).get("knowledge_panel", {})
        container_css = selectors.get("container", {}).get("css", "")

        if self.driver:
            container = self.driver.find_elements("css selector", container_css)
        elif self.page:
            container = self.page.query_selector(container_css)
        else:
            container = None

        if container:
            panel = {
                "title": self._extract_text(selectors.get("title", {}).get("css", "")),
                "subtitle": self._extract_text(selectors.get("subtitle", {}).get("css", "")),
                "description": self._extract_text(selectors.get("description", {}).get("css", ""))
            }

            if panel["title"]:
                writables.knowledge_panel = panel

        return writables

    def _extract_pagination_info(self, writables: GoogleSearchResultsDataModel) -> GoogleSearchResultsDataModel:
        """Extract pagination information"""
        selectors = self.selectors.get("selectors", {}).get("pagination", {})

        next_page_url = self._extract_attribute(selectors.get("next_page", {}).get("css", ""), "href")

        writables.has_next_page = bool(next_page_url)
        writables.next_page_url = next_page_url if next_page_url else ""

        return writables

    # =========================================================================
    # Helper methods
    # =========================================================================

    def _extract_text(self, css_selector: str) -> str:
        """Extract text from element"""
        if not css_selector:
            return ""

        try:
            if self.driver:
                elements = self.driver.find_elements("css selector", css_selector)
                if elements:
                    return elements[0].text.strip()
            elif self.page:
                element = self.page.query_selector(css_selector)
                if element:
                    return element.inner_text().strip()
        except Exception:
            pass

        return ""

    def _extract_attribute(self, css_selector: str, attribute: str) -> str:
        """Extract attribute from element"""
        if not css_selector:
            return ""

        try:
            if self.driver:
                elements = self.driver.find_elements("css selector", css_selector)
                if elements:
                    return elements[0].get_attribute(attribute) or ""
            elif self.page:
                element = self.page.query_selector(css_selector)
                if element:
                    return element.get_attribute(attribute) or ""
        except Exception:
            pass

        return ""

    def _extract_child_text(self, parent_element, css_selector: str) -> str:
        """Extract text from child element"""
        if not css_selector:
            return ""

        try:
            if self.driver:
                children = parent_element.find_elements("css selector", css_selector)
                if children:
                    return children[0].text.strip()
            elif self.page:
                child = parent_element.query_selector(css_selector)
                if child:
                    return child.inner_text().strip()
        except Exception:
            pass

        return ""

    def _extract_child_attribute(self, parent_element, css_selector: str, attribute: str) -> str:
        """Extract attribute from child element"""
        if not css_selector:
            return ""

        try:
            if self.driver:
                children = parent_element.find_elements("css selector", css_selector)
                if children:
                    return children[0].get_attribute(attribute) or ""
            elif self.page:
                child = parent_element.query_selector(css_selector)
                if child:
                    return child.get_attribute(attribute) or ""
        except Exception:
            pass

        return ""

    def export_writables_to_json_file(self, writables: list, output_filepath: str) -> None:
        """Export extracted data to JSON file"""
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            json.dump(writables, output_file, indent=2, ensure_ascii=False)
        logger.info(f"Exported results to {output_filepath}")


# =============================================================================
# Standalone execution example
# =============================================================================

if __name__ == "__main__":
    print("Google Search Results Schema Extractor")
    print("=" * 50)
    print("\nUsage:")
    print("""
    from selenium import webdriver
    from google_search_results_schema import GoogleSearchResultsExtractor

    driver = webdriver.Chrome()
    extractor = GoogleSearchResultsExtractor(selenium_webdriver=driver)

    writables = extractor.extract_results_by_query(
        search_query="plumbers miami",
        results_per_page=10,
        max_pages=1
    )

    extractor.export_writables_to_json_file(writables, "serp_results.json")
    driver.quit()
    """)
