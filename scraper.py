import re
import urllib.parse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import requests

EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

async def extract_emails_from_url(website_url: str) -> list[str]:
    """Crawls a business website homepage to find email addresses."""
    if not website_url or website_url == "N/A":
        return []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(website_url, headers=headers, timeout=5)
        if resp.status_code == 200:
            found = re.findall(EMAIL_REGEX, resp.text)
            clean_emails = list(set([e for e in found if not e.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))]))
            return clean_emails
    except Exception:
        pass
    return []

async def scrape_google_maps(query: str, limit: int = 10) -> list[dict]:
    """Scrapes Google Maps search results using Playwright."""
    search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await context.new_page()

        await page.goto(search_url, wait_until="networkidle")

        try:
            await page.click('button[aria-label="Accept all"]', timeout=3000)
        except Exception:
            pass

        feed_selector = 'div[role="feed"]'
        try:
            await page.wait_for_selector(feed_selector, timeout=10000)
            for _ in range(max(1, limit // 3)):
                await page.evaluate(f'document.querySelector("{feed_selector}").scrollBy(0, 3000)')
                await page.wait_for_timeout(1000)
        except Exception:
            pass

        items = await page.query_selector_all('a[href*="/maps/place/"]')
        seen_names = set()

        for item in items:
            if len(results) >= limit:
                break

            name = await item.get_attribute("aria-label")
            if not name or name in seen_names:
                continue
            seen_names.add(name)

            card_href = await item.get_attribute("href")

            parent = await item.xpath("..")
            parent_text = await parent[0].inner_text() if parent else ""

            phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}', parent_text)
            phone = phone_match.group(0) if phone_match else "N/A"

            await item.click()
            await page.wait_for_timeout(1500)

            website = "N/A"
            website_elem = await page.query_selector('a[data-tooltip="Open website"]')
            if website_elem:
                website = await website_elem.get_attribute("href")

            address = "N/A"
            address_elem = await page.query_selector('button[data-item-id="address"]')
            if address_elem:
                address = await address_elem.inner_text()

            emails = await extract_emails_from_url(website)

            results.append({
                "name": name,
                "address": address,
                "phone": phone,
                "website": website,
                "emails": emails,
                "maps_url": card_href
            })

        await browser.close()

    return results
