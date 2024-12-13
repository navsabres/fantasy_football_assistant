import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_KEYS = {
    'NFL_API_KEY': os.getenv('NFL_API_KEY', ''),
    'ESPN_API_KEY': os.getenv('ESPN_API_KEY', ''),
    'SLEEPER_API_KEY': os.getenv('SLEEPER_API_KEY', '')  # Note: Sleeper API currently doesn't require authentication
}

# API Endpoints
API_ENDPOINTS = {
    'NFL': 'https://api.nfl.com/v3/shield',
    'ESPN': 'https://fantasy.espn.com/apis/v3/games/ffl',
    'SLEEPER': 'https://api.sleeper.app/v1'
}

# Cache Settings
CACHE_CONFIG = {
    'DEFAULT_EXPIRY': 3600,  # 1 hour in seconds
    'PLAYER_STATS_EXPIRY': 1800,  # 30 minutes
    'MATCHUP_EXPIRY': 3600,  # 1 hour
    'NEWS_EXPIRY': 900,  # 15 minutes
    'PROJECTIONS_EXPIRY': 7200  # 2 hours
}

# Scoring Settings (Default PPR)
SCORING_SETTINGS = {
    'passing_touchdown': 4,
    'passing_yard': 0.04,
    'interception': -2,
    'rushing_touchdown': 6,
    'rushing_yard': 0.1,
    'reception': 1.0,  # PPR
    'receiving_yard': 0.1,
    'receiving_touchdown': 6,
    'fumble_lost': -2,
    'two_point_conversion': 2
}

# Rate Limiting
RATE_LIMITS = {
    'NFL_API': {
        'requests_per_second': 2,
        'requests_per_day': 1000
    },
    'ESPN_API': {
        'requests_per_second': 3,
        'requests_per_day': 2000
    },
    'SLEEPER_API': {
        'requests_per_second': 3,
        'requests_per_minute': 60
    }
}

# Data Update Intervals (in seconds)
UPDATE_INTERVALS = {
    'player_stats': 900,  # 15 minutes
    'injury_reports': 1800,  # 30 minutes
    'projections': 3600,  # 1 hour
    'news': 600  # 10 minutes
}

# League Settings
DEFAULT_LEAGUE_SETTINGS = {
    'roster_positions': {
        'QB': 1,
        'RB': 2,
        'WR': 2,
        'TE': 1,
        'FLEX': 1,
        'D/ST': 1,
        'K': 1,
        'BE': 7
    },
    'max_trades_per_day': 3,
    'waiver_period_hours': 48,
    'trade_review_period_hours': 24
}

# Position Rankings Weight Factors
POSITION_WEIGHTS = {
    'QB': {
        'passing_yards': 1.0,
        'passing_touchdowns': 1.2,
        'rushing_yards': 1.5  # Mobile QBs bonus
    },
    'RB': {
        'rushing_yards': 1.0,
        'rushing_touchdowns': 1.2,
        'receptions': 1.1  # Receiving backs bonus
    },
    'WR': {
        'receiving_yards': 1.0,
        'receiving_touchdowns': 1.2,
        'receptions': 1.0
    },
    'TE': {
        'receiving_yards': 1.1,  # Premium for TE production
        'receiving_touchdowns': 1.3,
        'receptions': 1.2
    }
}

# Data Sources Priority
DATA_SOURCES_PRIORITY = {
    'player_stats': ['NFL', 'ESPN', 'SLEEPER'],
    'projections': ['ESPN', 'SLEEPER'],
    'news': ['NFL', 'ESPN', 'SLEEPER'],
    'injuries': ['NFL', 'SLEEPER', 'ESPN']
}

# Error Messages
ERROR_MESSAGES = {
    'api_error': 'Error accessing fantasy football data. Please try again later.',
    'player_not_found': 'Player not found in the database.',
    'rate_limit': 'Rate limit exceeded. Please try again in a few minutes.',
    'invalid_query': 'Invalid query format. Please check your input.',
    'no_data': 'No data available for this request.'
}

# Feature Flags
FEATURES = {
    'use_machine_learning': False,  # Enable/disable ML-based predictions
    'advanced_analytics': True,
    'news_integration': True,
    'trade_analyzer': True,
    'injury_tracking': True,
    'weather_impact': False  # Future feature for weather impact analysis
}
