from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
import time
import json

# Changed this line to import from the app package:
from app.scrape_made_in_china import scrape_made_in_china

app = FastAPI()

# ✅ CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Schema for results
class ScrapeResult(BaseModel):
    title: str
    supplier: str
    raw_price: str
    moq: str
    link: str

# ✅ Original scrape endpoint (unchanged)
@app.get("/scrape", response_model=List[ScrapeResult])
def scrape(search: str = Query(...)):
    try:
        df = scrape_made_in_china(search)
        expected_columns = ["title", "supplier", "raw_price", "moq", "link"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""
        df = df[expected_columns].fillna("")
        return df.to_dict(orient="records")
    except Exception as e:
        return [{
            "title": "Error",
            "supplier": "",
            "raw_price": str(e),
            "moq": "",
            "link": ""
        }]

# ✅ NEW: Streaming scrape with progress events
@app.get("/scrape-stream")
def scrape_with_progress(search: str = Query(...)):

    def event_stream():
        try:
            yield f"data: {json.dumps({'progress': 10, 'message': 'Launching browser'})}\n\n"
            time.sleep(1)

            yield f"data: {json.dumps({'progress': 30, 'message': 'Loading search results'})}\n\n"
            time.sleep(1)

            yield f"data: {json.dumps({'progress': 60, 'message': 'Scraping data'})}\n\n"
            df = scrape_made_in_china(search)

            yield f"data: {json.dumps({'progress': 90, 'message': 'Cleaning results'})}\n\n"
            expected_columns = ["title", "supplier", "raw_price", "moq", "link"]
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""
            df = df[expected_columns].fillna("")

            yield f"data: {json.dumps({'progress': 100, 'message': 'done', 'data': df.to_dict(orient='records')})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'progress': 100, 'message': 'error', 'error': str(e)})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
