const axios = require("axios");

/**
 * MCP Client for communicating with the Python MCP Server
 */
class MCPClient {
  constructor() {
    this.baseUrl = process.env.MCP_SERVER_URL || "http://localhost:8000";
    this.timeout = parseInt(process.env.MCP_TIMEOUT) || 30000;
  }

  /**
   * Send a request to the MCP server
   * @param {string} endpoint - The endpoint to call
   * @param {object} data - The data to send
   * @returns {Promise<object>} The response from the MCP server
   */
  async request(endpoint, data = {}) {
    try {
      const response = await axios({
        method: "POST",
        url: `${this.baseUrl}${endpoint}`,
        data,
        timeout: this.timeout,
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response.data;
    } catch (error) {
      console.error(`MCP Client Error [${endpoint}]:`, error.message);
      throw new Error(`MCP Server Error: ${error.message}`);
    }
  }

  /**
   * Compare goods/products
   * @param {object} params - Comparison parameters
   * @returns {Promise<object>} Comparison results
   */
  async compareGoods(params) {
    return this.request("/compare", params);
  }

  /**
   * Search for products
   * @param {string} query - Search query
   * @param {object} options - Search options
   * @returns {Promise<object>} Search results
   */
  async searchProducts(query, options = {}) {
    return this.request("/search", { query, ...options });
  }

  /**
   * Get product details
   * @param {string} productId - Product ID
   * @returns {Promise<object>} Product details
   */
  async getProductDetails(productId) {
    return this.request("/product", { productId });
  }

  /**
   * Health check for MCP server
   * @returns {Promise<object>} Health status
   */
  async healthCheck() {
    try {
      const response = await axios.get(`${this.baseUrl}/health`, {
        timeout: 5000,
      });
      return response.data;
    } catch (error) {
      return { status: "error", message: error.message };
    }
  }
}

// Export singleton instance
module.exports = new MCPClient();
