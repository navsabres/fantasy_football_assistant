# Fantasy Football Virtual Assistant

A Python-based virtual assistant that helps you manage your fantasy football team with features like player stats, lineup recommendations, and matchup analysis.

## Features

- Player Stats and Insights
- Lineup Recommendations
- Matchup Analysis
- Trade Evaluations
- Performance Trend Analysis
- Waiver Wire Recommendations

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fantasy_football_assistant
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the assistant:
```bash
python main.py
```

### Example Commands

1. Get player stats:
```
Get stats for Patrick Mahomes
```

2. Get lineup recommendations:
```
Who should I start this week?
```

3. Check injury updates:
```
Any injured players?
```

4. Get waiver wire recommendations:
```
Show me waiver recommendations
```

5. Analyze matchups:
```
How does the matchup look for Travis Kelce?
```

## Project Structure

- `main.py`: Main application entry point
- `data_manager.py`: Handles data operations and storage
- `utils.py`: Utility functions and constants
- `data/`: Directory for storing user data and cached information

## Sample Data

The assistant currently uses sample data for demonstration purposes. In a production environment, you would integrate with fantasy football APIs to get real-time data.

## Future Enhancements

1. Integration with real fantasy football APIs
2. Machine learning for better predictions
3. Web interface
4. Mobile app support
5. Custom league scoring support
6. Trade analyzer improvements
7. Player comparison features
8. Historical performance analytics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
