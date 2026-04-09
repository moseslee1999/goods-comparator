"""
Goods Comparator MCP Server
A Python-based MCP (Model Context Protocol) server for comparing goods/products.
"""

import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")


# Pydantic Models
class CompareRequest(BaseModel):
    """Request model for comparing goods"""
    products: list[str] = Field(..., description="List of product names or IDs to compare")
    criteria: Optional[list[str]] = Field(None, description="Comparison criteria (price, quality, etc.)")
    sources: Optional[list[str]] = Field(None, description="Sources to fetch data from")


class CompareResponse(BaseModel):
    """Response model for comparison results"""
    success: bool
    data: dict[str, Any]
    timestamp: str


class SearchRequest(BaseModel):
    """Request model for searching products"""
    query: str = Field(..., description="Search query")
    limit: Optional[int] = Field(10, description="Maximum number of results")
    category: Optional[str] = Field(None, description="Product category filter")


class SearchResponse(BaseModel):
    """Response model for search results"""
    success: bool
    results: list[dict[str, Any]]
    total: int
    timestamp: str


class ProductRequest(BaseModel):
    """Request model for product details"""
    productId: str = Field(..., description="Product ID")


class ProductResponse(BaseModel):
    """Response model for product details"""
    success: bool
    product: dict[str, Any]
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    service: str
    version: str
    timestamp: str


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    print(f"🚀 MCP Server starting on http://{HOST}:{PORT}")
    print(f"📡 Backend URL: {BACKEND_URL}")
    yield
    print("👋 MCP Server shutting down")


# Create FastAPI application
app = FastAPI(
    title="Goods Comparator MCP Server",
    description="MCP Server for comparing goods and products across different sources",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[BACKEND_URL, "http://localhost:5000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        service="mcp-server",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
    )


@app.post("/compare", response_model=CompareResponse)
async def compare_goods(request: CompareRequest):
    """
    Compare multiple goods/products based on specified criteria.
    
    This endpoint fetches product information from various sources
    and returns a comparison analysis.
    """
    try:
        # TODO: Implement actual comparison logic
        # This is a placeholder response
        comparison_data = {
            "products": request.products,
            "criteria": request.criteria or ["price", "rating", "availability"],
            "comparison": {
                product: {
                    "price": f"${(i + 1) * 10}.99",
                    "rating": 4.0 + (i * 0.2),
                    "availability": "In Stock",
                }
                for i, product in enumerate(request.products)
            },
            "recommendation": request.products[0] if request.products else None,
        }
        
        return CompareResponse(
            success=True,
            data=comparison_data,
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    """
    Search for products across multiple sources.
    
    Returns a list of products matching the search query.
    """
    try:
        # TODO: Implement actual search logic
        # This is a placeholder response
        mock_results = [
            {
                "id": f"prod_{i}",
                "name": f"{request.query} Product {i + 1}",
                "price": f"${(i + 1) * 15}.99",
                "rating": 4.0 + (i * 0.1),
                "source": "mock_source",
            }
            for i in range(min(request.limit or 10, 10))
        ]
        
        return SearchResponse(
            success=True,
            results=mock_results,
            total=len(mock_results),
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/product", response_model=ProductResponse)
async def get_product_details(request: ProductRequest):
    """
    Get detailed information about a specific product.
    
    Returns comprehensive product data including specs, reviews, etc.
    """
    try:
        # TODO: Implement actual product lookup logic
        # This is a placeholder response
        product_data = {
            "id": request.productId,
            "name": f"Product {request.productId}",
            "description": "A sample product description",
            "price": "$29.99",
            "rating": 4.5,
            "reviews_count": 150,
            "specifications": {
                "weight": "1.5 kg",
                "dimensions": "10x20x5 cm",
                "material": "Premium quality",
            },
            "availability": "In Stock",
            "sources": [
                {"name": "Source A", "price": "$29.99", "url": "#"},
                {"name": "Source B", "price": "$31.99", "url": "#"},
            ],
        }
        
        return ProductResponse(
            success=True,
            product=product_data,
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
    )
