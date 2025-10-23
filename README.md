# StockWise
StockWise is a web-based financial analytics platform designed to empower investors with data-driven insights for the Colombo Stock Exchange (CSE). Our mission is to provide clear, actionable visualizations of stock profits, portfolio performance, and key financial metrics.


🇱🇰 CSE Portfolio Tracker Dashboard - StockWise

A dynamic Django-based web application designed to provide Colombo Stock Exchange (CSE) investors with a comprehensive, real-time-like view of their investment portfolio performance, P&L, and best-performing assets.

🚀 Key Features

This dashboard focuses on providing critical metrics in an easily digestible, visual format:

Portfolio Overview (P&L): Calculate and display the current total profit/loss (P&L) of the entire portfolio, including percentage and absolute value changes for the day and overall.

Best Performer: Automatically identify and highlight the single best-performing stock (based on total return or daily percentage gain).

Stock Performance Breakdowns: Visual, interactive charts (using Plotly/Chart.js) showing the individual performance of each held stock against its cost basis.

Holdings Management: A user-friendly interface to add, edit, or remove stock holdings (Ticker, Quantity, Purchase Price, Purchase Date).

Market Watch (Simulated): Display simulated market data for key CSE indices (ASPI, S&P SL20) and top movers.

💻 Tech Stack

Backend Framework: Python / Django (MVT Architecture)

Database: SQLite (for development)



⚙️ Installation and Setup

Follow these steps to get your project running locally.

1. Environment Setup

# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate.bat # Windows

# 3. Install dependencies (Django, Pandas, etc.)
pip install Django pandas requests python-dotenv # Add specific charting libraries later


2. Project Initialization

Navigate to the directory containing manage.py.

# 4. Apply Database Migrations (creates default Django tables)
python manage.py migrate

# 5. Create a Superuser (for Admin access)
python manage.py createsuperuser


3. Run the Dashboard

# 6. Start the local development server
python manage.py runserver


Open your browser and navigate to http://127.0.0.1:8000/.

