# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Project Name**: Goods Comparator  
**Type**: Personal Project  
**Scale**: <100 users (MVP)  
**Goal**: Build a web app that lets users search and compare general goods (starting with electronics) in a clean, customizable table format.

### Core Pain Point

Users cannot easily compare products from different stores in a table with common criteria.

## Tech Stack (Locked)

- **Frontend**: Next.js 15 (TypeScript + Tailwind + App Router)
- **Backend**: Node.js + Express (separate folder)
- **MCP Server**: Python (separate folder) using MCP protocol + stdio
- **Database**: MongoDB (Atlas free tier)
- **Browser Automation**: browser-use library
- **LLM**: Anthropic (via OpenRouter API)
- **Search**: Fuse.js (non-AI fuzzy matching)

## MVP Scope (Must-Have Only)

### Features

**Search Tab**

- Search products by name (fuzzy matching via Fuse.js)
- Show 25 results per page with pagination
- "Add to Compare" button on each product

**Compare Tab**

- Side-by-side comparison table (maximum 4 products)
- Columns:
  - price (sortable)
  - dimension (free-text, not sortable)
  - weight (sortable)
  - brand (not sortable)
  - source store (not sortable)
  - rating (sortable)

**Data**

- 50 electronics products
- Scraped from: https://www.fortress.com.hk/zh-hk/ and https://www.broadwaylifestyle.com/

## Out of Scope for MVP

- User authentication
- Comparison history
- Generative AI comparison criteria
- Custom user-defined criteria
- More product categories

## Key Architecture

- Frontend (Next.js) → calls REST API
- Node.js Backend (MCP Client) → spawns and communicates with Python via **stdio** (JSON-RPC)
- Python MCP Server → uses `browser-use` + Anthropic LLM to scrape, extract, clean, and save data to MongoDB

## Week-by-Week Plan

**Week 1**: Project Setup + Python MCP Server

- Create folder structure
- Initialize Next.js, Node.js, Python venv
- Set up MongoDB Atlas
- Build Python MCP Server with tools (`browse_page`, `extract_product_fields`, `insert_product`)

**Week 2**: Scraping & Data Ingestion

- Implement full scraping flow to populate 50 products

**Week 3**: Search Tab (Frontend + Backend)

**Week 4**: Compare Tab (Dynamic Table)

**Week 5**: Testing + Free Tier Deployment (Vercel + Railway/Render + MongoDB Atlas)

**Week 6**: Bug fixes + Polish + Prepare for post-MVP features

## Important Notes

- Use separate backend because of heavy Playwright + LLM operations.
- MCP uses stdio transport between Node.js and Python.
- All work must stay on free tier.
- Keep code clean and well-commented.

## Success Criteria for MVP Launch

User can:

1. Search product name
2. See paginated results
3. Add up to 4 products to comparison
4. View clean comparison table with all 6 columns

## Architecture Overview

This is a three-service monorepo. Each service runs independently and must be started separately:

```
comparator-frontend/   # Next.js 15 (port 3000)
comparator-backend/    # Express 5 (port 5000)
mcp-server/            # FastAPI (port 8000)
```

**Request flow:** Frontend → Backend → MCP Server → External sources

The backend acts purely as a proxy/orchestrator. All product comparison, search, and scraping logic lives in the MCP server (`mcp-server/main.py`). The backend exposes `/api/compare`, `/api/search`, `/api/product/:id`, and `/api/mcp-health` — each of which delegates to the corresponding MCP endpoint via `comparator-backend/src/mcpClient.js`.

The MCP server currently returns placeholder data. The three endpoints (`/compare`, `/search`, `/product`) all have `# TODO` comments where real browser automation and Anthropic SDK calls should be implemented.

## Development Commands

**Frontend** (Next.js 15 — see note below):

```bash
cd comparator-frontend && npm install && npm run dev   # port 3000
npm run build   # production build
npm run lint    # ESLint
```

**Backend:**

```bash
cd comparator-backend && npm install && npm run dev    # port 5000, nodemon
```

**MCP Server:**

```bash
cd mcp-server
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py                # port 8000, reload off
DEBUG=true python main.py     # enable hot reload via uvicorn
```

## Important: Next.js Version

The frontend uses Next.js 15 which has breaking changes from prior versions. Before writing any frontend code, read the relevant guide in `comparator-frontend/node_modules/next/dist/docs/`. APIs, conventions, and file structure may differ from training data.

## Environment Variables

Each service reads from its own `.env` file (not committed).

**Backend** (`comparator-backend/.env`):
| Variable | Default |
|---|---|
| `PORT` | `5000` |
| `NODE_ENV` | `development` |
| `FRONTEND_URL` | `http://localhost:3000` |
| `MCP_SERVER_URL` | `http://localhost:8000` |
| `MCP_TIMEOUT` | `30000` |
| `CORS_ORIGIN` | `http://localhost:3000` |

**MCP Server** (`mcp-server/.env`):
| Variable | Default |
|---|---|
| `HOST` | `0.0.0.0` |
| `PORT` | `8000` |
| `DEBUG` | `false` |
| `BACKEND_URL` | `http://localhost:5000` |

The MCP server also expects an Anthropic API key and potentially MongoDB credentials (PyMongo is a dependency) — check `requirements.txt` for all installed packages.

## Key Files

- `comparator-backend/src/mcpClient.js` — singleton MCPClient that proxies all calls to the MCP server
- `comparator-backend/src/config/index.js` — centralized backend config from env vars
- `mcp-server/main.py` — entire MCP server: Pydantic models, FastAPI routes, placeholder logic
- `comparator-frontend/` — boilerplate Next.js app, no pages implemented yet
