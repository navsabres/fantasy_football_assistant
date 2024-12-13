import json
import pandas as pd
from pathlib import Path
from datetime import datetime

class DataManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent / 'data'
        self.data_dir.mkdir(exist_ok=True)
        
        # Sample historical performance data
        self.historical_data = {
            "week1": {
                "Patrick Mahomes": {"points": 28.5, "opponent": "DET"},
                "Travis Kelce": {"points": 21.2, "opponent": "DET"},
                "Christian McCaffrey": {"points": 25.8, "opponent": "PIT"}
            },
            "week2": {
                "Patrick Mahomes": {"points": 22.1, "opponent": "JAX"},
                "Travis Kelce": {"points": 19.8, "opponent": "JAX"},
                "Christian McCaffrey": {"points": 27.4, "opponent": "LAR"}
            }
        }
        
        # Sample matchup data
        self.matchups = {
            "KC": {"defense_rank": 15, "points_allowed": 21.5},
            "SF": {"defense_rank": 3, "points_allowed": 17.2},
            "DET": {"defense_rank": 22, "points_allowed": 24.8}
        }
    
    def get_player_trend(self, player_name):
        """Calculate player's performance trend based on historical data"""
        points = []
        for week in self.historical_data.values():
            if player_name in week:
                points.append(week[player_name]["points"])
        
        if points:
            trend = "Improving" if points[-1] > points[0] else "Declining"
            avg_points = sum(points) / len(points)
            return {
                "trend": trend,
                "average_points": round(avg_points, 2),
                "last_game": points[-1]
            }
        return None

    def analyze_matchup(self, player_team, opponent):
        """Analyze upcoming matchup based on team statistics"""
        if opponent in self.matchups:
            defense_rating = "Strong" if self.matchups[opponent]["defense_rank"] <= 10 else \
                           "Average" if self.matchups[opponent]["defense_rank"] <= 20 else "Weak"
            
            return {
                "defense_rating": defense_rating,
                "points_allowed": self.matchups[opponent]["points_allowed"],
                "defense_rank": self.matchups[opponent]["defense_rank"]
            }
        return None

    def get_waiver_recommendations(self, position=None):
        """Get waiver wire recommendations based on recent performance"""
        # Sample waiver wire players
        waiver_players = {
            "Jerome Ford": {
                "position": "RB",
                "team": "CLE",
                "recent_points": 15.2,
                "ownership": "25%",
                "outlook": "Potential breakout candidate"
            },
            "Tank Dell": {
                "position": "WR",
                "team": "HOU",
                "recent_points": 16.8,
                "ownership": "40%",
                "outlook": "Rising rookie with good target share"
            }
        }
        
        if position:
            return {name: data for name, data in waiver_players.items() 
                   if data["position"] == position.upper()}
        return waiver_players

    def save_user_team(self, team_data, user_id):
        """Save user's team data to JSON file"""
        file_path = self.data_dir / f"user_{user_id}_team.json"
        with open(file_path, 'w') as f:
            json.dump(team_data, f, indent=4)

    def load_user_team(self, user_id):
        """Load user's team data from JSON file"""
        file_path = self.data_dir / f"user_{user_id}_team.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return None

    def evaluate_trade(self, players_giving, players_receiving):
        """Evaluate a potential trade based on player values and trends"""
        giving_value = 0
        receiving_value = 0
        
        for player in players_giving:
            trend_data = self.get_player_trend(player)
            if trend_data:
                giving_value += trend_data["average_points"]
        
        for player in players_receiving:
            trend_data = self.get_player_trend(player)
            if trend_data:
                receiving_value += trend_data["average_points"]
        
        value_difference = receiving_value - giving_value
        
        return {
            "giving_value": round(giving_value, 2),
            "receiving_value": round(receiving_value, 2),
            "value_difference": round(value_difference, 2),
            "recommendation": "Accept" if value_difference > 0 else "Decline"
        }
