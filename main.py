import json
from datetime import datetime
from pathlib import Path
import os

class FantasyFootballAssistant:
    def __init__(self):
        self.data_path = Path(__file__).parent / 'data'
        self.data_path.mkdir(exist_ok=True)
        self.load_data()

    def load_data(self):
        """Load sample player data and stats"""
        self.players = {
            "Patrick Mahomes": {
                "position": "QB",
                "team": "KC",
                "stats": {"passing_yards": 4839, "touchdowns": 41, "interceptions": 12},
                "projected_points": 24.5,
                "status": "Active"
            },
            "Travis Kelce": {
                "position": "TE",
                "team": "KC",
                "stats": {"receptions": 110, "receiving_yards": 1338, "touchdowns": 12},
                "projected_points": 18.7,
                "status": "Active"
            },
            "Christian McCaffrey": {
                "position": "RB",
                "team": "SF",
                "stats": {"rushing_yards": 1139, "touchdowns": 14, "receptions": 85},
                "projected_points": 22.1,
                "status": "Questionable"
            }
        }

    def get_player_stats(self, player_name):
        """Get stats for a specific player"""
        player = self.players.get(player_name)
        if player:
            return f"Stats for {player_name}:\n" + \
                   f"Position: {player['position']}\n" + \
                   f"Team: {player['team']}\n" + \
                   f"Status: {player['status']}\n" + \
                   f"Projected Points: {player['projected_points']}\n" + \
                   f"Stats: {player['stats']}"
        return f"Player {player_name} not found."

    def get_lineup_recommendation(self):
        """Provide lineup recommendations based on projected points"""
        recommendations = []
        for name, data in self.players.items():
            if data['status'] == "Active" and data['projected_points'] > 15:
                recommendations.append(f"{name} ({data['position']}) - Projected: {data['projected_points']}")
        return "\n".join(recommendations) if recommendations else "No recommendations available."

    def process_query(self, query):
        """Process user queries and provide responses"""
        query = query.lower()
        
        if "stats" in query and "for" in query:
            # Extract player name after "for"
            player_name = query.split("for")[-1].strip().title()
            return self.get_player_stats(player_name)
        
        elif "lineup" in query or "who should i start" in query:
            return "Here are my recommendations for your lineup:\n" + self.get_lineup_recommendation()
        
        elif "injured" in query or "status" in query:
            injured_players = [
                f"{name} - {data['status']}"
                for name, data in self.players.items()
                if data['status'] != "Active"
            ]
            return "Injured/Questionable Players:\n" + "\n".join(injured_players) if injured_players else "No injured players to report."
        
        else:
            return "I can help you with:\n" + \
                   "- Player stats (e.g., 'Get stats for Patrick Mahomes')\n" + \
                   "- Lineup recommendations (e.g., 'Who should I start?')\n" + \
                   "- Injury updates (e.g., 'Any injured players?')"

def main():
    assistant = FantasyFootballAssistant()
    print("Fantasy Football Assistant Ready! (Type 'quit' to exit)")
    
    while True:
        query = input("\nWhat would you like to know? ").strip()
        
        if query.lower() == 'quit':
            print("Goodbye!")
            break
            
        response = assistant.process_query(query)
        print("\n" + response)

if __name__ == "__main__":
    main()
