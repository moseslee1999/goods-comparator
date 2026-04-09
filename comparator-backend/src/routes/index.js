const express = require("express");
const router = express.Router();
const mcpClient = require("../mcpClient");

// Compare goods endpoint
router.post("/compare", async (req, res, next) => {
  try {
    const result = await mcpClient.compareGoods(req.body);
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// Search products endpoint
router.get("/search", async (req, res, next) => {
  try {
    const { q, ...options } = req.query;
    const result = await mcpClient.searchProducts(q, options);
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// Get product details endpoint
router.get("/product/:id", async (req, res, next) => {
  try {
    const result = await mcpClient.getProductDetails(req.params.id);
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// MCP Server health check
router.get("/mcp-health", async (req, res) => {
  const health = await mcpClient.healthCheck();
  res.json(health);
});

module.exports = router;
