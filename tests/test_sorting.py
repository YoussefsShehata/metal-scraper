import pytest
from app.scrape_made_in_china import scrape_made_in_china

@pytest.fixture
def sample_data(monkeypatch):
    # Bypass real scraping: return a fixed, unsorted list
    def fake_scrape():
        return [
            {"name": "A", "price": 200},
            {"name": "B", "price": 50},
            {"name": "C", "price": 150},
        ]
    monkeypatch.setattr(
        "app.scrape_made_in_china.scrape_made_in_china",
        fake_scrape
    )
    return fake_scrape()

def test_scrape_returns_sorted_by_price(sample_data):
    products = scrape_made_in_china()
    prices = [p["price"] for p in products]
    assert prices == sorted(prices), (
        f"Expected sorted prices {sorted(prices)}, got {prices}"
    )
