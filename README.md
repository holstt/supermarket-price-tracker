# supermarket-price-tracker

Scrape and analyze the prices of online supermarkets.

:warning: This is a work in progress. The program currently scrapes prices from the supermarket Rema1000 and stores them as json files at `./data/rema/<scrape_time>`

#### Todo:

-   [ ] Store scraped json files in a database
-   [ ] UI to view price changes for individual products over time
-   [ ] Subscribe on price changes and get notified on discord
-   [ ] Add more supermarkets

## Getting Started

```bash
# Clone the repo
git clone https://github.com/holstt/supermarket-price-tracker.git
cd supermarket-price-tracker

# Use poetry to install dependencies and create a virtual environment
poetry install
poetry shell

# (while in virtual environment)

# Run the scraper
python ./main.py

# Run tests
pytest
```

### Docker 🐳

It is also possible to run the scraper in a docker container using Docker Compose:

```bash
cd docker
docker-compose up -d
```

The script run as a cron job as specified in `./cron`
