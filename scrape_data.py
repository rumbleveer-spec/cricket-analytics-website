#!/usr/bin/env python3
"""
Cricket Analytics - Web Scraper using Playwright
Scrapes data from T20 dashboard websites
"""

import sys
import os
import asyncio
from playwright.async_api import async_playwright
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, BBLMatch, BBLBatting, BBLBowling

# Target URLs - Update these with actual T20 dashboard URLs
URLS = {
    'matches': 'https://www.espncricinfo.com/series/big-bash-league-2024-25-1423141/match-schedule-fixtures',
    'batting': 'https://www.espncricinfo.com/records/tournament/batting-most-runs-career/big-bash-league-2024-25-15517',
    'bowling': 'https://www.espncricinfo.com/records/tournament/bowling-most-wickets-career/big-bash-league-2024-25-15517'
}

async def scrape_matches(page):
    """Scrape match data from T20 dashboard"""
    print("🏏 Scraping match data...")

    try:
        await page.goto(URLS['matches'], wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)

        # Adjust selectors based on actual website structure
        matches = []

        # Example selectors - UPDATE THESE based on actual site
        match_cards = await page.query_selector_all('.ds-rounded-lg')

        for idx, card in enumerate(match_cards[:20]):  # Limit to 20 matches
            try:
                # Extract match details - UPDATE selectors
                team1 = await card.query_selector('.team1-name')
                team2 = await card.query_selector('.team2-name')
                venue = await card.query_selector('.venue-name')
                date = await card.query_selector('.match-date')
                result = await card.query_selector('.match-result')

                match_data = {
                    'match_no': idx + 1,
                    'date': await date.inner_text() if date else 'TBD',
                    'venue': await venue.inner_text() if venue else 'Unknown',
                    'team1': await team1.inner_text() if team1 else 'Team 1',
                    'team2': await team2.inner_text() if team2 else 'Team 2',
                    'result': await result.inner_text() if result else 'TBD'
                }
                matches.append(match_data)

            except Exception as e:
                print(f"  ⚠️  Error scraping match {idx + 1}: {e}")
                continue

        print(f"✅ Scraped {len(matches)} matches")
        return matches

    except Exception as e:
        print(f"❌ Error scraping matches: {e}")
        return []

async def scrape_batting_stats(page):
    """Scrape batting statistics"""
    print("📊 Scraping batting stats...")

    try:
        await page.goto(URLS['batting'], wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)

        players = []

        # Find stats table - UPDATE selector based on actual site
        table = await page.query_selector('table.ds-table')
        if not table:
            print("⚠️  Batting stats table not found")
            return []

        rows = await table.query_selector_all('tbody tr')

        for idx, row in enumerate(rows[:20]):  # Top 20
            try:
                cells = await row.query_selector_all('td')
                if len(cells) < 8:
                    continue

                player_data = {
                    'rank': idx + 1,
                    'player_name': await cells[0].inner_text(),
                    'team': await cells[1].inner_text() if len(cells) > 1 else 'Unknown',
                    'matches': int((await cells[2].inner_text()).strip()) if len(cells) > 2 else 0,
                    'runs': int((await cells[3].inner_text()).strip()) if len(cells) > 3 else 0,
                    'average': float((await cells[4].inner_text()).strip()) if len(cells) > 4 else 0.0,
                    'strike_rate': float((await cells[5].inner_text()).strip()) if len(cells) > 5 else 0.0,
                    'high_score': await cells[6].inner_text() if len(cells) > 6 else '0',
                    'sixes': int((await cells[7].inner_text()).strip()) if len(cells) > 7 else 0
                }
                players.append(player_data)

            except Exception as e:
                print(f"  ⚠️  Error scraping player {idx + 1}: {e}")
                continue

        print(f"✅ Scraped {len(players)} batting records")
        return players

    except Exception as e:
        print(f"❌ Error scraping batting stats: {e}")
        return []

async def scrape_bowling_stats(page):
    """Scrape bowling statistics"""
    print("🎳 Scraping bowling stats...")

    try:
        await page.goto(URLS['bowling'], wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)

        players = []

        # Find stats table - UPDATE selector
        table = await page.query_selector('table.ds-table')
        if not table:
            print("⚠️  Bowling stats table not found")
            return []

        rows = await table.query_selector_all('tbody tr')

        for idx, row in enumerate(rows[:20]):  # Top 20
            try:
                cells = await row.query_selector_all('td')
                if len(cells) < 7:
                    continue

                player_data = {
                    'rank': idx + 1,
                    'player_name': await cells[0].inner_text(),
                    'team': await cells[1].inner_text() if len(cells) > 1 else 'Unknown',
                    'matches': int((await cells[2].inner_text()).strip()) if len(cells) > 2 else 0,
                    'wickets': int((await cells[3].inner_text()).strip()) if len(cells) > 3 else 0,
                    'average': float((await cells[4].inner_text()).strip()) if len(cells) > 4 else 0.0,
                    'economy': float((await cells[5].inner_text()).strip()) if len(cells) > 5 else 0.0,
                    'best_figures': await cells[6].inner_text() if len(cells) > 6 else '0/0'
                }
                players.append(player_data)

            except Exception as e:
                print(f"  ⚠️  Error scraping bowler {idx + 1}: {e}")
                continue

        print(f"✅ Scraped {len(players)} bowling records")
        return players

    except Exception as e:
        print(f"❌ Error scraping bowling stats: {e}")
        return []

def save_to_database(matches, batting, bowling):
    """Save scraped data to database"""
    print("\n💾 Saving to database...")

    with app.app_context():
        # Clear existing data
        print("🗑️  Clearing old data...")
        BBLMatch.query.delete()
        BBLBatting.query.delete()
        BBLBowling.query.delete()
        db.session.commit()

        # Import matches
        for match in matches:
            m = BBLMatch(
                match_no=match.get('match_no'),
                date=match.get('date', 'TBD'),
                venue=match.get('venue', 'Unknown'),
                team1=match.get('team1', 'Team 1'),
                score1=match.get('score1', 'TBD'),
                team2=match.get('team2', 'Team 2'),
                score2=match.get('score2', 'TBD'),
                result=match.get('result', 'TBD'),
                winner=match.get('winner', 'TBD'),
                margin=match.get('margin', 'TBD'),
                player_of_match=match.get('player_of_match', 'TBD')
            )
            db.session.add(m)

        # Import batting
        for player in batting:
            p = BBLBatting(
                rank=player.get('rank'),
                player_name=player.get('player_name'),
                team=player.get('team', 'Unknown'),
                matches=player.get('matches', 0),
                runs=player.get('runs', 0),
                average=player.get('average', 0.0),
                strike_rate=player.get('strike_rate', 0.0),
                high_score=player.get('high_score', '0'),
                hundreds=player.get('hundreds', 0),
                fifties=player.get('fifties', 0),
                fours=player.get('fours', 0),
                sixes=player.get('sixes', 0)
            )
            db.session.add(p)

        # Import bowling
        for player in bowling:
            p = BBLBowling(
                rank=player.get('rank'),
                player_name=player.get('player_name'),
                team=player.get('team', 'Unknown'),
                matches=player.get('matches', 0),
                wickets=player.get('wickets', 0),
                best_figures=player.get('best_figures', '0/0'),
                average=player.get('average', 0.0),
                economy=player.get('economy', 0.0),
                strike_rate=player.get('strike_rate', 0.0)
            )
            db.session.add(p)

        db.session.commit()

        print(f"✅ Saved {len(matches)} matches")
        print(f"✅ Saved {len(batting)} batting records")
        print(f"✅ Saved {len(bowling)} bowling records")

async def main():
    """Main scraping function"""
    print("="*60)
    print("🕷️  Cricket Analytics - Web Scraper")
    print("="*60)
    print()

    async with async_playwright() as p:
        # Launch browser
        print("🌐 Launching browser...")
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        page = await context.new_page()

        try:
            # Scrape all data
            matches = await scrape_matches(page)
            batting = await scrape_batting_stats(page)
            bowling = await scrape_bowling_stats(page)

            # Save to JSON backup
            data = {
                'matches': matches,
                'batting': batting,
                'bowling': bowling
            }

            with open('scraped_data.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("\n💾 Backup saved to scraped_data.json")

            # Save to database
            save_to_database(matches, batting, bowling)

            print()
            print("="*60)
            print("✅ SCRAPING COMPLETE!")
            print("="*60)
            print()
            print("🌐 Refresh your website:")
            print("   → https://whatsapp.ankitrajput.cloud")

        finally:
            await browser.close()

if __name__ == "__main__":
    # Install playwright if not installed
    import subprocess
    try:
        import playwright
    except ImportError:
        print("📦 Installing playwright...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"])
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])

    asyncio.run(main())
