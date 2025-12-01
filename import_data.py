#!/usr/bin/env python3
"""
Cricket Analytics - Bulk Data Import Script
Imports all cricket data from hardcoded dataset into SQLite database
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, BBLMatch, BBLBatting, BBLBowling

def import_bbl_matches():
    """Import BBL match data"""
    print("📊 Importing BBL matches...")

    matches_data = [
        (1, "Dec 15, 2024", "MCG", "Melbourne Stars", "133/9 (20)", "Perth Scorchers", "135/6 (18.3)", "Scorchers won", "Perth Scorchers", "4 wickets", "Aaron Hardie"),
        (2, "Dec 15, 2024", "Sydney", "Melbourne Renegades", "155/8 (20)", "Sydney Sixers", "159/5 (18.2)", "Sixers won", "Sydney Sixers", "5 wickets", "Jordan Silk"),
        (3, "Dec 17, 2024", "Adelaide", "Adelaide Strikers", "140/7 (20)", "Sydney Thunder", "141/5 (18.4)", "Thunder won", "Sydney Thunder", "5 wickets", "Sam Konstas"),
        (4, "Dec 18, 2024", "MCG", "Melbourne Stars", "180/5 (20)", "Brisbane Heat", "181/7 (19.4)", "Heat won", "Brisbane Heat", "3 wickets", "Marnus Labuschagne"),
        (5, "Dec 19, 2024", "Hobart", "Hobart Hurricanes", "74/10 (14.3)", "Melbourne Renegades", "75/2 (10.4)", "Renegades won", "Melbourne Renegades", "8 wickets", "Tom Rogers"),
        (6, "Dec 20, 2024", "Adelaide", "Adelaide Strikers", "189/7 (20)", "Melbourne Stars", "165/9 (20)", "Strikers won", "Adelaide Strikers", "24 runs", "Matthew Short"),
        (7, "Dec 21, 2024", "Perth", "Perth Scorchers", "146/9 (20)", "Hobart Hurricanes", "147/5 (19.2)", "Hurricanes won", "Hobart Hurricanes", "5 wickets", "Mitchell Owen"),
        (8, "Dec 22, 2024", "Sydney", "Sydney Thunder", "178/8 (20)", "Sydney Sixers", "150/7 (20)", "Thunder won", "Sydney Thunder", "28 runs", "David Warner"),
        (9, "Dec 23, 2024", "Adelaide", "Adelaide Strikers", "169/7 (20)", "Brisbane Heat", "171/6 (19.4)", "Heat won", "Brisbane Heat", "4 wickets", "Xavier Bartlett"),
        (10, "Dec 26, 2024", "Perth", "Perth Scorchers", "139/8 (20)", "Melbourne Renegades", "142/7 (19.3)", "Renegades won", "Melbourne Renegades", "3 wickets", "Jake Fraser-McGurk"),
        (11, "Dec 27, 2024", "MCG", "Melbourne Stars", "180/4 (20)", "Sydney Sixers", "182/5 (19.3)", "Sixers won", "Sydney Sixers", "5 wickets", "Steven Smith"),
        (12, "Dec 28, 2024", "Perth", "Perth Scorchers", "187/6 (20)", "Brisbane Heat", "166/8 (20)", "Scorchers won", "Perth Scorchers", "21 runs", "Ashton Turner"),
        (13, "Dec 29, 2024", "Hobart", "Hobart Hurricanes", "172/6 (20)", "Adelaide Strikers", "145/9 (20)", "Hurricanes won", "Hobart Hurricanes", "27 runs", "Ben McDermott"),
        (14, "Dec 30, 2024", "Sydney", "Sydney Thunder", "158/7 (20)", "Melbourne Stars", "162/6 (19.2)", "Stars won", "Melbourne Stars", "4 wickets", "Glenn Maxwell"),
        (15, "Dec 31, 2024", "Brisbane", "Brisbane Heat", "169/8 (20)", "Sydney Sixers", "170/6 (19.4)", "Sixers won", "Sydney Sixers", "4 wickets", "Jordan Silk"),
        (16, "Jan 1, 2025", "Sydney", "Sydney Thunder", "179/5 (20)", "Melbourne Renegades", "166/8 (20)", "Thunder won", "Sydney Thunder", "13 runs", "Jason Sangha"),
        (17, "Jan 2, 2025", "Adelaide", "Adelaide Strikers", "161/7 (20)", "Perth Scorchers", "162/5 (18.3)", "Scorchers won", "Perth Scorchers", "5 wickets", "Cooper Connolly"),
        (18, "Jan 3, 2025", "Hobart", "Hobart Hurricanes", "179/4 (20)", "Sydney Sixers", "162/8 (20)", "Hurricanes won", "Hobart Hurricanes", "17 runs", "Nikhil Chaudhary"),
        (19, "Jan 4, 2025", "Brisbane", "Brisbane Heat", "190/5 (20)", "Melbourne Stars", "154/9 (20)", "Heat won", "Brisbane Heat", "36 runs", "Colin Munro"),
        (20, "Jan 4, 2025", "Melbourne", "Melbourne Renegades", "187/7 (20)", "Adelaide Strikers", "147/9 (20)", "Renegades won", "Melbourne Renegades", "40 runs", "Josh Brown"),
    ]

    count = 0
    for match_data in matches_data:
        match = BBLMatch(
            match_no=match_data[0],
            date=match_data[1],
            venue=match_data[2],
            team1=match_data[3],
            score1=match_data[4],
            team2=match_data[5],
            score2=match_data[6],
            result=match_data[7],
            winner=match_data[8],
            margin=match_data[9],
            player_of_match=match_data[10]
        )
        db.session.add(match)
        count += 1

    db.session.commit()
    print(f"✅ Imported {count} BBL matches")

def import_bbl_batting():
    """Import BBL batting statistics"""
    print("📊 Importing BBL batting stats...")

    batting_data = [
        (1, "Mitchell Owen", "Hobart Hurricanes", 11, 452, 41.09, 203.60, "108", 2, 0, 35, 36),
        (2, "David Warner", "Sydney Thunder", 11, 357, 32.45, 140.55, "86", 0, 3, 44, 10),
        (3, "Glenn Maxwell", "Melbourne Stars", 11, 325, 29.55, 162.81, "90*", 0, 2, 27, 18),
        (4, "Cooper Connolly", "Perth Scorchers", 10, 294, 32.67, 146.27, "66", 0, 3, 28, 12),
        (5, "Josh Brown", "Melbourne Renegades", 11, 291, 26.45, 158.15, "73", 0, 2, 30, 16),
        (6, "Ben McDermott", "Hobart Hurricanes", 11, 287, 26.09, 139.32, "68", 0, 2, 32, 8),
        (7, "Jason Sangha", "Sydney Thunder", 11, 285, 25.91, 134.91, "67", 0, 2, 28, 7),
        (8, "Jake Fraser-McGurk", "Melbourne Renegades", 11, 277, 25.18, 172.67, "79", 0, 2, 20, 19),
        (9, "Jordan Silk", "Sydney Sixers", 11, 275, 30.56, 142.49, "70", 0, 2, 25, 9),
        (10, "Matthew Short", "Adelaide Strikers", 10, 268, 26.80, 151.41, "69", 0, 2, 31, 11),
        (11, "Marnus Labuschagne", "Brisbane Heat", 8, 263, 32.88, 131.66, "77", 0, 2, 28, 7),
        (12, "Tim David", "Hobart Hurricanes", 10, 256, 42.67, 171.81, "62*", 0, 2, 13, 20),
        (13, "Steven Smith", "Sydney Sixers", 8, 238, 29.75, 128.65, "66", 0, 1, 29, 4),
        (14, "Ashton Turner", "Perth Scorchers", 10, 236, 33.71, 137.21, "55", 0, 1, 18, 11),
        (15, "Marcus Stoinis", "Melbourne Stars", 9, 228, 28.50, 144.30, "53", 0, 1, 16, 14),
        (16, "Sam Konstas", "Sydney Thunder", 9, 224, 24.89, 168.42, "73", 0, 2, 24, 11),
        (17, "Colin Munro", "Brisbane Heat", 10, 221, 22.10, 161.31, "62", 0, 1, 21, 13),
        (18, "Moises Henriques", "Sydney Sixers", 11, 219, 24.33, 131.73, "48", 0, 0, 20, 6),
        (19, "Alex Ross", "Adelaide Strikers", 10, 213, 21.30, 124.42, "51", 0, 1, 21, 5),
        (20, "Nick Hobson", "Perth Scorchers", 10, 208, 26.00, 145.10, "52", 0, 1, 18, 10),
    ]

    count = 0
    for player_data in batting_data:
        player = BBLBatting(
            rank=player_data[0],
            player_name=player_data[1],
            team=player_data[2],
            matches=player_data[3],
            runs=player_data[4],
            average=player_data[5],
            strike_rate=player_data[6],
            high_score=player_data[7],
            hundreds=player_data[8],
            fifties=player_data[9],
            fours=player_data[10],
            sixes=player_data[11]
        )
        db.session.add(player)
        count += 1

    db.session.commit()
    print(f"✅ Imported {count} BBL batting records")

def import_bbl_bowling():
    """Import BBL bowling statistics"""
    print("📊 Importing BBL bowling stats...")

    bowling_data = [
        (1, "Jason Behrendorff", "Perth Scorchers", 10, 17, "3/21", 17.82, 7.05, 13.41),
        (2, "Tom Rogers", "Melbourne Renegades", 10, 16, "4/23", 17.38, 7.51, 13.88),
        (3, "Lance Morris", "Perth Scorchers", 8, 15, "3/22", 15.67, 8.10, 11.60),
        (4, "Lloyd Pope", "Sydney Sixers", 10, 15, "3/25", 20.87, 8.49, 14.73),
        (5, "Riley Meredith", "Hobart Hurricanes", 9, 13, "3/27", 19.54, 7.73, 15.15),
        (6, "Spencer Johnson", "Adelaide Strikers", 7, 13, "4/20", 13.08, 6.54, 11.08),
        (7, "Ben Dwarshuis", "Sydney Sixers", 11, 14, "4/32", 22.57, 7.76, 17.43),
        (8, "Nathan Ellis", "Hobart Hurricanes", 11, 14, "3/23", 23.71, 7.93, 17.93),
        (9, "Xavier Bartlett", "Brisbane Heat", 9, 13, "3/22", 19.69, 7.53, 15.69),
        (10, "Nathan McAndrew", "Sydney Thunder", 10, 13, "5/26", 21.69, 7.68, 16.92),
        (11, "Chris Green", "Sydney Thunder", 11, 12, "3/18", 23.25, 7.15, 19.50),
        (12, "Wes Agar", "Adelaide Strikers", 9, 11, "3/28", 24.09, 8.00, 18.00),
        (13, "Kane Richardson", "Melbourne Renegades", 11, 11, "3/26", 29.09, 8.03, 21.73),
        (14, "Adam Zampa", "Melbourne Stars", 9, 11, "3/21", 24.18, 7.85, 18.55),
        (15, "Joel Paris", "Perth Scorchers", 9, 10, "3/19", 22.70, 7.32, 18.60),
        (16, "Ben Cutting", "Sydney Sixers", 8, 9, "3/24", 21.56, 7.76, 16.67),
        (17, "Hayden Kerr", "Sydney Sixers", 11, 9, "3/27", 32.22, 7.84, 24.67),
        (18, "Doug Warren", "Melbourne Stars", 8, 8, "3/31", 24.00, 7.38, 19.50),
        (19, "Matthew Kuhnemann", "Brisbane Heat", 8, 8, "2/21", 28.75, 7.93, 21.75),
        (20, "Mark Steketee", "Brisbane Heat", 7, 8, "2/18", 21.75, 7.25, 18.00),
    ]

    count = 0
    for player_data in bowling_data:
        player = BBLBowling(
            rank=player_data[0],
            player_name=player_data[1],
            team=player_data[2],
            matches=player_data[3],
            wickets=player_data[4],
            best_figures=player_data[5],
            average=player_data[6],
            economy=player_data[7],
            strike_rate=player_data[8]
        )
        db.session.add(player)
        count += 1

    db.session.commit()
    print(f"✅ Imported {count} BBL bowling records")

def main():
    """Main import function"""
    print("="*60)
    print("🏏 Cricket Analytics - Bulk Data Import")
    print("="*60)
    print()

    with app.app_context():
        # Clear existing data
        print("🗑️  Clearing existing data...")
        BBLMatch.query.delete()
        BBLBatting.query.delete()
        BBLBowling.query.delete()
        db.session.commit()
        print("✅ Cleared old data")
        print()

        # Import all data
        import_bbl_matches()
        import_bbl_batting()
        import_bbl_bowling()

        print()
        print("="*60)
        print("✅ BULK IMPORT COMPLETE!")
        print("="*60)
        print()
        print("📊 Imported:")
        print(f"   • {BBLMatch.query.count()} matches")
        print(f"   • {BBLBatting.query.count()} batting records")
        print(f"   • {BBLBowling.query.count()} bowling records")
        print()
        print("🌐 Refresh your website to see the data!")
        print("   → https://whatsapp.ankitrajput.cloud")

if __name__ == "__main__":
    main()
