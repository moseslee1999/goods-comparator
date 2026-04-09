# Goods Comparator

A full-stack application for comparing goods/products across different sources.

## Project Structure

```
goods-comparator/
├── comparator-frontend/    # Next.js 15 frontend (TypeScript + Tailwind CSS)
├── comparator-backend/     # Node.js Express backend
└── mcp-server/             # Python MCP Server
```

## Getting Started

### Frontend (Next.js)

```bash
cd comparator-frontend
npm install
npm run dev
```

### Backend (Express)

```bash
cd comparator-backend
npm install
npm run dev
```

### MCP Server (Python)

```bash
cd mcp-server
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Environment Variables

Each service has its own `.env` file. See the respective folders for configuration.

## License

MIT
