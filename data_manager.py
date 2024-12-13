import json
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime
import time

class DataManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent / 'data'
        self.data_dir.mkdir(exist_ok=True)
        
        # API endpoints
        self.ESPN_API_URL = "https://fantasy.espn.com/apis/v3/games/ffl"
        self.NFL_API_URL = "https://api.nfl.com/v3/shield"
        self.SLEEPER_API_URL = "https://api.sleeper.app/v1"
        
        # Cache data to avoid excessive API calls
        self.cache = {}
        self.cache_expiry = 3600  # 1 hour
        
    def _get_espn_data(self, endpoint, params=None):
        """
        Get data from ESPN Fantasy API
        Documentation: https://github.com/cwendt94/espn-api/wiki
        """
        url = f"{self.ESPN_API_URL}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching ESPN data: {e}")
            return None

    def _get_nfl_data(self, query):
        """
        Get data from NFL's Official API
        Requires registration at https://api.nfl.com/
        """
        headers = {
            "Authorization": "Bearer YOUR_NFL_API_TOKEN",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                self.NFL_API_URL,
                headers=headers,
                json={"query": query}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching NFL data: {e}")
            return None

    def _get_sleeper_data(self, endpoint):
        """
        Get data from Sleeper API
        Documentation: https://docs.sleeper.app/
        """
        url = f"{self.SLEEPER_API_URL}/{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Sleeper data: {e}")
            return None

    def get_player_stats(self, player_name):
        """Get comprehensive player stats from multiple sources"""
        cache_key = f"player_stats_{player_name}_{datetime.now().strftime('%Y-%m-%d')}"
        
        if cache_key in self.cache and time.time() - self.cache[cache_key]['timestamp'] < self.cache_expiry:
            return self.cache[cache_key]['data']
        
        # Get player ID from Sleeper
        players = self._get_sleeper_data("players")
        player_id = None
        for pid, data in players.items():
            if data.get('full_name', '').lower() == player_name.lower():
                player_id = pid
                break
        
        if not player_id:
            return None
            
        # Get stats from multiple sources
        stats = {}
        
        # ESPN Stats
        espn_stats = self._get_espn_data(f"players/{player_id}/stats")
        if espn_stats:
            stats['espn'] = espn_stats
            
        # NFL Stats
        nfl_query = """
        {
            player(id: "%s") {
                stats {
                    passing_yards
                    passing_touchdowns
                    rushing_yards
                    rushing_touchdowns
                    receptions
                    receiving_yards
                    receiving_touchdowns
                }
            }
        }
        """ % player_id
        nfl_stats = self._get_nfl_data(nfl_query)
        if nfl_stats:
            stats['nfl'] = nfl_stats
            
        # Sleeper Stats
        sleeper_stats = self._get_sleeper_data(f"stats/nfl/player/{player_id}")
        if sleeper_stats:
            stats['sleeper'] = sleeper_stats
            
        # Combine stats from different sources
        combined_stats = self._combine_stats(stats)
        
        # Cache the results
        self.cache[cache_key] = {
            'timestamp': time.time(),
            'data': combined_stats
        }
        
        return combined_stats

    def _combine_stats(self, stats):
        """Combine stats from different sources with priority order"""
        combined = {}
        
        # Priority: NFL > ESPN > Sleeper
        sources = ['nfl', 'espn', 'sleeper']
        
        for stat_type in ['passing_yards', 'passing_touchdowns', 'rushing_yards', 
                         'rushing_touchdowns', 'receptions', 'receiving_yards', 
                         'receiving_touchdowns', 'interceptions', 'fumbles']:
            for source in sources:
                if source in stats and stat_type in stats[source]:
                    combined[stat_type] = stats[source][stat_type]
                    break
        
        return combined

    def get_injuries(self):
        """Get latest injury reports"""
        cache_key = f"injuries_{datetime.now().strftime('%Y-%m-%d_%H')}"
        
        if cache_key in self.cache and time.time() - self.cache[cache_key]['timestamp'] < self.cache_expiry:
            return self.cache[cache_key]['data']
            
        injuries = self._get_sleeper_data("injuries/nfl")
        
        self.cache[cache_key] = {
            'timestamp': time.time(),
            'data': injuries
        }
        
        return injuries

    def get_projections(self, player_id):
        """Get player projections from multiple sources"""
        projections = {}
        
        # ESPN Projections
        espn_proj = self._get_espn_data(f"players/{player_id}/projections")
        if espn_proj:
            projections['espn'] = espn_proj
            
        # Sleeper Projections
        sleeper_proj = self._get_sleeper_data(f"projections/nfl/player/{player_id}")
        if sleeper_proj:
            projections['sleeper'] = sleeper_proj
            
        return self._combine_projections(projections)

    def _combine_projections(self, projections):
        """Average out projections from different sources"""
        if not projections:
            return None
            
        combined = {}
        for stat_type in ['points', 'passing_yards', 'rushing_yards', 'receiving_yards']:
            values = [
                proj[stat_type] for source, proj in projections.items()
                if stat_type in proj
            ]
            if values:
                combined[stat_type] = sum(values) / len(values)
                
        return combined

    def get_matchups(self, week=None):
        """Get NFL matchups for specified week"""
        if week is None:
            week = self._get_current_week()
            
        cache_key = f"matchups_week_{week}"
        
        if cache_key in self.cache and time.time() - self.cache[cache_key]['timestamp'] < self.cache_expiry:
            return self.cache[cache_key]['data']
            
        matchups = self._get_sleeper_data(f"schedule/nfl/{week}")
        
        self.cache[cache_key] = {
            'timestamp': time.time(),
            'data': matchups
        }
        
        return matchups

    def _get_current_week(self):
        """Get current NFL week"""
        return self._get_sleeper_data("state/nfl")['week']

    def get_waiver_recommendations(self, position=None):
        """Get waiver wire recommendations based on trends and projections"""
        players = self._get_sleeper_data("players/nfl")
        trends = self._get_sleeper_data("stats/nfl/trending/add")
        
        recommendations = []
        for trend in trends[:20]:  # Top 20 trending players
            player = players.get(str(trend['player_id']))
            if player and (position is None or player['position'] == position):
                proj = self.get_projections(trend['player_id'])
                recommendations.append({
                    'name': player['full_name'],
                    'position': player['position'],
                    'team': player['team'],
                    'trend_score': trend['count'],
                    'projections': proj
                })
                
        return sorted(recommendations, key=lambda x: x['trend_score'], reverse=True)

    def evaluate_trade(self, players_giving, players_receiving):
        """Evaluate trade based on current stats, projections, and trends"""
        giving_value = 0
        receiving_value = 0
        
        for player in players_giving:
            stats = self.get_player_stats(player)
            proj = self.get_projections(player)
            if stats and proj:
                giving_value += self._calculate_player_value(stats, proj)
                
        for player in players_receiving:
            stats = self.get_player_stats(player)
            proj = self.get_projections(player)
            if stats and proj:
                receiving_value += self._calculate_player_value(stats, proj)
                
        return {
            'giving_value': giving_value,
            'receiving_value': receiving_value,
            'difference': receiving_value - giving_value,
            'recommendation': 'Accept' if receiving_value > giving_value else 'Decline'
        }

    def _calculate_player_value(self, stats, projections):
        """Calculate player value based on stats and projections"""
        # Complex value calculation algorithm
        value = 0
        
        # Weight recent performance more heavily
        if stats:
            value += stats.get('passing_yards', 0) * 0.04
            value += stats.get('passing_touchdowns', 0) * 4
            value += stats.get('rushing_yards', 0) * 0.1
            value += stats.get('rushing_touchdowns', 0) * 6
            value += stats.get('receiving_yards', 0) * 0.1
            value += stats.get('receiving_touchdowns', 0) * 6
            
        # Add projected value
        if projections:
            value += projections.get('points', 0) * 0.5
            
        return value
