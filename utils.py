import re
from datetime import datetime, timedelta

# Constants for scoring settings (standard scoring)
SCORING_SETTINGS = {
    'passing_touchdown': 4,
    'passing_yard': 0.04,  # 1 point per 25 yards
    'interception': -2,
    'rushing_touchdown': 6,
    'rushing_yard': 0.1,  # 1 point per 10 yards
    'reception': 1,  # PPR scoring
    'receiving_yard': 0.1,
    'receiving_touchdown': 6,
    'fumble_lost': -2,
    'two_point_conversion': 2
}

# Position requirements for a standard lineup
LINEUP_REQUIREMENTS = {
    'QB': 1,
    'RB': 2,
    'WR': 2,
    'TE': 1,
    'FLEX': 1,  # RB/WR/TE
    'DST': 1,
    'K': 1
}

class TextProcessor:
    @staticmethod
    def extract_player_name(text):
        """Extract player name from user input"""
        # Common patterns for player name queries
        patterns = [
            r"stats for (.+?)(?:\?|$)",
            r"how is (.+?) doing",
            r"what about (.+?)(?:\?|$)",
            r"start (.+?) or",
            r"should i start (.+?)(?:\?|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).strip().title()
        return None

    @staticmethod
    def extract_position(text):
        """Extract position from user input"""
        positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        text = text.upper()
        for pos in positions:
            if pos in text:
                return pos
        return None

class StatCalculator:
    @staticmethod
    def calculate_fantasy_points(stats, scoring_settings=SCORING_SETTINGS):
        """Calculate fantasy points based on player stats and scoring settings"""
        points = 0
        
        # Passing points
        points += stats.get('passing_yards', 0) * scoring_settings['passing_yard']
        points += stats.get('passing_touchdowns', 0) * scoring_settings['passing_touchdown']
        points += stats.get('interceptions', 0) * scoring_settings['interception']
        
        # Rushing points
        points += stats.get('rushing_yards', 0) * scoring_settings['rushing_yard']
        points += stats.get('rushing_touchdowns', 0) * scoring_settings['rushing_touchdown']
        
        # Receiving points
        points += stats.get('receptions', 0) * scoring_settings['reception']
        points += stats.get('receiving_yards', 0) * scoring_settings['receiving_yard']
        points += stats.get('receiving_touchdowns', 0) * scoring_settings['receiving_touchdown']
        
        # Miscellaneous
        points += stats.get('fumbles_lost', 0) * scoring_settings['fumble_lost']
        points += stats.get('two_point_conversions', 0) * scoring_settings['two_point_conversion']
        
        return round(points, 2)

    @staticmethod
    def calculate_trend(historical_points, weeks=4):
        """Calculate player's scoring trend over last few weeks"""
        if len(historical_points) < 2:
            return None
            
        recent_points = historical_points[-weeks:]
        avg_first_half = sum(recent_points[:len(recent_points)//2]) / (len(recent_points)//2)
        avg_second_half = sum(recent_points[len(recent_points)//2:]) / (len(recent_points)//2)
        
        trend_value = avg_second_half - avg_first_half
        
        if trend_value > 3:
            return "Strongly Improving"
        elif trend_value > 1:
            return "Slightly Improving"
        elif trend_value < -3:
            return "Strongly Declining"
        elif trend_value < -1:
            return "Slightly Declining"
        else:
            return "Stable"

def format_player_stats(stats, include_projections=True):
    """Format player stats into readable string"""
    output = []
    
    if 'passing_yards' in stats:
        output.append(f"Passing: {stats['passing_yards']} yards")
    if 'rushing_yards' in stats:
        output.append(f"Rushing: {stats['rushing_yards']} yards")
    if 'receiving_yards' in stats:
        output.append(f"Receiving: {stats['receiving_yards']} yards")
    if 'touchdowns' in stats:
        output.append(f"Total TDs: {stats['touchdowns']}")
    
    if include_projections and 'projected_points' in stats:
        output.append(f"Projected Points: {stats['projected_points']}")
    
    return " | ".join(output)

def get_current_week():
    """Calculate current NFL week based on date"""
    # Assuming NFL season starts in September
    season_start = datetime(2023, 9, 7)  # Adjust date for current season
    current_date = datetime.now()
    
    if current_date < season_start:
        return "Preseason"
    
    week_number = ((current_date - season_start).days // 7) + 1
    
    if week_number > 18:
        return "Postseason"
    
    return f"Week {week_number}"
