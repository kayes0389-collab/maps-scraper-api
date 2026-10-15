from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_google_maps

app = FastAPI(
    title="Open Outscraper API",
    description="A self-hosted Google Maps scraper and lead enrichment API.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Open Outscraper API",
        "docs_url": "/docs"
    }

@app.get("/api/v1/search")
async def search_places(
    query: str = Query(..., description="Target search query (e.g., 'Boutiques in Dhaka')"),
    limit: int = Query(10, ge=1, le=50, description="Number of results to extract")
):
    """
    Search Google Maps and return enriched lead profiles with phone numbers and emails.
    """
    try:
        leads = await scrape_google_maps(query=query, limit=limit)
        return {
            "success": True,
            "query": query,
            "total_count": len(leads),
            "data": leads
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
