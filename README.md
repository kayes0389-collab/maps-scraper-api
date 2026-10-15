# Open Outscraper API 🗺️🔍

An open-source, self-hosted alternative to Outscraper for extracting Google Maps leads, phone numbers, websites, and verified contact emails.

## 🚀 Features
- **Google Maps Scraping:** Automated browser-based lead extraction using Playwright.
- **Deep Email Enrichment:** Crawls official websites of extracted businesses to find contact emails.
- **RESTful API:** Built on FastAPI with auto-generated Swagger UI (`/docs`).
- **AI Ready:** Compatible with custom ChatGPT / Claude connectors.

## 📦 Quick Start Setup

### 1. Set up Virtual Environment
\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 2. Install Dependencies & Playwright Browsers
\`\`\`bash
pip install -r requirements.txt
playwright install chromium
\`\`\`

### 3. Launch the Server
\`\`\`bash
python main.py
\`\`\`

The server will be running at `http://localhost:8000`. You can access interactive API docs at `http://localhost:8000/docs`.

## 📡 Example API Usage

**Request:**
\`\`\`bash
curl -X GET "http://localhost:8000/api/v1/search?query=Garments%20Manufacturer%20in%20Dhaka&limit=5"
\`\`\`
