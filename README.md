# Fantasy Football Virtual Assistant

A comprehensive Python-based virtual assistant that helps you manage your fantasy football team using real-time data from NFL, ESPN, and Sleeper APIs.

## Features

### Core Features
- Real-time player statistics and performance tracking
- Data-driven lineup recommendations
- Advanced matchup analysis
- Trade value calculator
- Injury tracking and updates
- Waiver wire recommendations
- Multi-source data integration (NFL, ESPN, Sleeper)

### Data Sources
- NFL Official API
- ESPN Fantasy API
- Sleeper API
- Automated data aggregation and caching
- Real-time updates and notifications

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fantasy_football_assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up API credentials:
```bash
cp .env.template .env
```
Then edit `.env` with your API keys:
- Get NFL API key from https://api.nfl.com/
- Get ESPN API key from https://www.espn.com/apis/devcenter/docs/
- Sleeper API (no key required currently)

## Configuration

The project uses several configuration files:
- `config.py`: Main configuration settings
- `.env`: API keys and environment-specific settings
- `utils.py`: Utility functions and scoring calculations
- `data_manager.py`: Data fetching and processing logic

### Customizing Settings

You can customize various aspects of the assistant:
- Scoring settings in `config.py`
- Cache duration for different data types
- API rate limiting
- League-specific settings
- Position-specific weights for rankings

## Usage

Run the assistant:
```bash
python main.py
```

### Example Commands

1. Get comprehensive player stats:
```
Get stats for Patrick Mahomes
```

2. Get lineup recommendations based on multiple data sources:
```
Who should I start this week?
```

3. Check injury updates:
```
Any injured players?
```

4. Get data-driven waiver recommendations:
```
Show me waiver recommendations
```

5. Analyze matchups with advanced statistics:
```
How does the matchup look for Travis Kelce?
```

6. Evaluate trades using multi-source data:
```
Evaluate trade: giving Patrick Mahomes, getting Josh Allen
```

## Data Integration

The assistant integrates data from multiple sources:
- NFL API: Official statistics and player data
- ESPN API: Fantasy scoring and projections
- Sleeper API: Additional player data and trending information

### Data Refresh Rates
- Player Stats: Every 15 minutes
- Injury Reports: Every 30 minutes
- Projections: Every hour
- News Updates: Every 10 minutes

## Advanced Features

### Machine Learning Integration
- Trend analysis for player performance
- Matchup prediction algorithms
- Trade value optimization

### Analytics
- Advanced player performance metrics
- Strength of schedule analysis
- Historical performance tracking
- Trend-based predictions

## Error Handling

The assistant includes robust error handling:
- API rate limiting management
- Data validation and cleaning
- Fallback data sources
- Automatic retry mechanisms

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

1. Machine Learning Integration
   - Advanced player performance prediction
   - Matchup outcome probability
   - Trade value optimization

2. Additional Data Sources
   - Weather data integration
   - Social media sentiment analysis
   - Advanced statistics providers

3. Enhanced Features
   - Dynasty league support
   - Draft assistance
   - Custom scoring system support
   - Mobile app integration

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NFL for providing official statistics
- ESPN for fantasy sports data
- Sleeper for additional player insights
- Open-source community for various dependencies
