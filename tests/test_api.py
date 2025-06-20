from fastapi.testclient import TestClient
from app.fastapi_server import app

client = TestClient(app)

def test_products_endpoint_sorted():
    response = client.get("/products")  # adjust path if yours differs
    assert response.status_code == 200

    data = response.json()
    prices = [item["price"] for item in data]
    assert prices == sorted(prices), (
        f"API returned prices {prices}, which are not sorted"
    )
