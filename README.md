# Trading Bot

## Project Overview
Automated stock trading bot using Alpaca Markets API

## Prerequisites
- Python 3.8+
- Alpaca Markets account

## Setup

### Linux/macOS Setup
```bash
# Clone the repository
git clone https://github.com/IanSpeelman/trading-bot
cd trading-bot

# Create environment variables file
cp .env.example .env
```

Edit `.env` with your Alpaca credentials:
```
export API_KEY="<YOUR_API_KEY>"
export API_SECRET="<YOUR_API_SECRET>"
export ACCOUNT_NAME="<YOUR_IDENTIFIER>"
```

Notes:
- API credentials can be created in Alpaca settings > Profile > Manage Accounts

## Running the Bot
```bash
# Create virtual environment
python3 -m venv env

# Load environment variables and activate environment
source .env
source env/bin/activate

# Run the trading bot
python3 index.py
```


## Usage
Use the CLI to:
- Add/remove trading symbols
- Change trading intervals
- Start/stop trading
- Trigger panic mode to exit all positions
