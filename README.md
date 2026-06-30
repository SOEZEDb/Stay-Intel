 StayIntel

Scrapes hotel data (name, link, provisions, rating) from Google Maps using Playwright and stores it in a SQLAlchemy database. Includes a Flask API to query the data, deployed live on Railway.

 Live API
https://stay-intel-production.up.railway.app

 Tech Stack
- Python
- Playwright
- Flask
- SQLAlchemy
- SQLite
- Docker
- Railway

 SETUP
pip install playwright flask flask-sqlalchemy
playwright install chromium

USAGE
python main.py   # runs the scraper
python api.py    # starts the API at localhost:5000

 ENDPOINTS
| Endpoint | Description |
|----------|-------------|
| GET /list | List all hotels (supports ?name= and ?page=) |
| GET /list/<id> | Get a single hotel by ID |
| GET /top | Top rated hotels (supports ?limit=) |
| GET /search?q= | Search hotels by partial name |
| GET /hotels/provision/<provision_name> | Filter hotels by amenity |
