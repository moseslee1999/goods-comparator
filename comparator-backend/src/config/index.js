/**
 * Application configuration
 * Loads and exports all config values from environment variables
 */

const config = {
  // Server configuration
  port: parseInt(process.env.PORT) || 5000,
  nodeEnv: process.env.NODE_ENV || "development",

  // Frontend configuration
  frontendUrl: process.env.FRONTEND_URL || "http://localhost:3000",

  // MCP Server configuration
  mcp: {
    serverUrl: process.env.MCP_SERVER_URL || "http://localhost:8000",
    timeout: parseInt(process.env.MCP_TIMEOUT) || 30000,
  },

  // CORS configuration
  cors: {
    origin: process.env.CORS_ORIGIN || "http://localhost:3000",
    credentials: true,
  },
};

module.exports = config;
