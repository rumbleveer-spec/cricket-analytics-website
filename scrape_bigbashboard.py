#!/usr/bin/env python3
"""
Cricket Analytics - BigBashboard.com Complete Scraper
Scrapes BBL, Super Smash, and International T20 data
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed!")
    print("Run: pip install playwright && playwright install chromium")
    sys.exit(1)

from app import app, db, BBLMatch, BBLBatting, BBLBowling

BASE_URL = 'http://bigbashboard.com'

class BigBashboardScraper:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.data = {
            'matches': [],
            'batting': [],
            'bowling': [],
            'teams': []
        }

    async def init_browser(self):
        """Initialize Playwright browser"""
        print("🌐 Launching browser...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = await self.context.new_page()
        print("✅ Browser ready!")

    async def scrape_homepage(self):
        """Scrape main page to find all sections"""
        print(f"\n📊 Accessing {BASE_URL}...")
        try:
            await self.page.goto(BASE_URL, wait_until='networkidle', timeout=30000)
            await self.page.wait_for_timeout(2000)

            title = await self.page.title()
            print(f"✅ Page loaded: {title}")

            # Get all links
            links = await self.page.query_selector_all('a')
            urls = []
            for link in links:
                href = await link.get_attribute('href')
                text = await link.inner_text()
                if href:
                    urls.append({'text': text.strip(), 'href': href})

            print(f"✅ Found {len(urls)} navigation links")
            return urls

        except Exception as e:
            print(f"❌ Error accessing homepage: {e}")
            return []

    async def scrape_matches(self):
        """Scrape match data"""
        print("\n🏏 Scraping match data...")

        try:
            # Look for matches/fixtures page
            await self.page.goto(f"{BASE_URL}/matches", wait_until='networkidle', timeout=30000)
            await self.page.wait_for_timeout(2000)

            # Generic selectors - adjust based on site structure
            match_elements = await self.page.query_selector_all('.match-card, .match-item, [class*="match"]')

            matches = []
            for idx, elem in enumerate(match_elements[:40]):
                try:
                    # Extract all text from match element
                    text = await elem.inner_text()
                    html = await elem.inner_html()

                    # Store raw data for processing
                    match = {
                        'match_no': idx + 1,
                        'raw_text': text,
                        'raw_html': html[:500]  # Truncate
                    }
                    matches.append(match)

                except Exception as e:
                    continue

            print(f"✅ Scraped {len(matches)} match elements")
            self.data['matches'] = matches
            return matches

        except Exception as e:
            print(f"❌ Error scraping matches: {e}")
            return []

    async def scrape_batting_stats(self):
        """Scrape batting statistics"""
        print("\n📊 Scraping batting stats...")

        try:
            # Try common stats URLs
            possible_urls = [
                f"{BASE_URL}/stats/batting",
                f"{BASE_URL}/statistics/batting",
                f"{BASE_URL}/players/batting",
                f"{BASE_URL}/bbl/batting"
            ]

            for url in possible_urls:
                try:
                    await self.page.goto(url, wait_until='networkidle', timeout=15000)

                    # Check if stats table exists
                    table = await self.page.query_selector('table')
                    if table:
                        print(f"✅ Found stats at: {url}")
                        break
                except:
                    continue

            # Extract table data
            rows = await self.page.query_selector_all('table tbody tr')

            players = []
            for idx, row in enumerate(rows[:20]):
                try:
                    cells = await row.query_selector_all('td, th')
                    if len(cells) >= 5:
                        player = {
                            'rank': idx + 1,
                            'data': [await cell.inner_text() for cell in cells]
                        }
                        players.append(player)
                except:
                    continue

            print(f"✅ Scraped {len(players)} batting records")
            self.data['batting'] = players
            return players

        except Exception as e:
            print(f"❌ Error scraping batting: {e}")
            return []

    async def scrape_bowling_stats(self):
        """Scrape bowling statistics"""
        print("\n🎳 Scraping bowling stats...")

        try:
            possible_urls = [
                f"{BASE_URL}/stats/bowling",
                f"{BASE_URL}/statistics/bowling",
                f"{BASE_URL}/players/bowling",
                f"{BASE_URL}/bbl/bowling"
            ]

            for url in possible_urls:
                try:
                    await self.page.goto(url, wait_until='networkidle', timeout=15000)
                    table = await self.page.query_selector('table')
                    if table:
                        print(f"✅ Found stats at: {url}")
                        break
                except:
                    continue

            rows = await self.page.query_selector_all('table tbody tr')

            players = []
            for idx, row in enumerate(rows[:20]):
                try:
                    cells = await row.query_selector_all('td, th')
                    if len(cells) >= 5:
                        player = {
                            'rank': idx + 1,
                            'data': [await cell.inner_text() for cell in cells]
                        }
                        players.append(player)
                except:
                    continue

            print(f"✅ Scraped {len(players)} bowling records")
            self.data['bowling'] = players
            return players

        except Exception as e:
            print(f"❌ Error scraping bowling: {e}")
            return []

    async def take_screenshot(self, name='screenshot'):
        """Take screenshot for debugging"""
        try:
            await self.page.screenshot(path=f'{name}.png')
            print(f"📸 Screenshot saved: {name}.png")
        except:
            pass

    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()

async def main():
    """Main scraping orchestrator"""
    print("="*70)
    print("🕷️  BigBashboard.com - Complete Data Scraper")
    print("="*70)
    print()

    scraper = BigBashboardScraper()

    try:
        await scraper.init_browser()

        # Scrape homepage to understand structure
        print("🔍 Analyzing website structure...")
        links = await scraper.scrape_homepage()

        # Save link structure
        with open('site_structure.json', 'w') as f:
            json.dump(links, f, indent=2)
        print("💾 Site structure saved to site_structure.json")

        # Take screenshot
        await scraper.take_screenshot('homepage')

        # Try to scrape each section
        await scraper.scrape_matches()
        await scraper.scrape_batting_stats()
        await scraper.scrape_bowling_stats()

        # Save all scraped data
        with open('scraped_data.json', 'w') as f:
            json.dump(scraper.data, f, indent=2)

        print()
        print("="*70)
        print("✅ SCRAPING COMPLETE!")
        print("="*70)
        print()
        print("📊 Data collected:")
        print(f"   • {len(scraper.data['matches'])} matches")
        print(f"   • {len(scraper.data['batting'])} batting records")
        print(f"   • {len(scraper.data['bowling'])} bowling records")
        print()
        print("💾 Files created:")
        print("   • scraped_data.json - All scraped data")
        print("   • site_structure.json - Website navigation map")
        print("   • homepage.png - Screenshot")
        print()
        print("📝 Next step:")
        print("   Review scraped_data.json and customize selectors if needed")
        print("   Then run data import to populate database")

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await scraper.close()

if __name__ == "__main__":
    # Check dependencies
    print("🔍 Checking dependencies...")
    try:
        import playwright
        print("✅ Playwright installed")
    except ImportError:
        print("❌ Installing playwright...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"])
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])

    # Run scraper
    asyncio.run(main())
