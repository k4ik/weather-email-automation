# Weather Email Automation

Automate the process of retrieving weather data, generating reports, and emailing them at specified times. This project uses Python to scrape and store weather information, compile it into a CSV report, and send the report via email.

## Features
- **Weather Data Extraction**: Fetch temperature data from specified cities.
- **CSV Report Generation**: Generate daily weather reports.
- **Automated Email Delivery**: Schedule email reports to be sent automatically.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-email-automation.git
cd weather-email-automation
```

Create a virtual environment and install dependencies:

```bash

python -m venv venv
source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Create an .env file (based on .env.example) with your email credentials.

## Usage

Run the main script to schedule daily weather email reports:

```bash
python3 main.py
```
