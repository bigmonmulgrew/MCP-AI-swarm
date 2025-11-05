import express from "express";
import axios from "axios";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

dotenv.config();
const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const FRONTEND_PORT = process.env.FRONTEND_PORT_I || 5173;
const MCPS_HOST = process.env.MCPS_HOST || "localhost";
const MCPS_PORT = process.env.MCPS_PORT_I || 8080;
const MCPS_URL = `http://${MCPS_HOST}:${MCPS_PORT}`;
const MCP_VISUALISER_URL = process.env.MCP_VISUALISER_URL || "http://localhost:8070";
const MCP_DATA_URL = process.env.MCP_DATA_URL || "http://localhost:8060";

// Serve static frontend
app.use(express.static(path.join(__dirname, "public")));

// Example status route
app.get("/status", async (req, res) => {
  try {
    const { data } = await axios.get(`${MCP_VISUALISER_URL}/status`);
    res.json({ status: data.status });
  } catch {
    res.json({ status: "unreachable" });
  }
});

// Proxy routes
app.get("/call-query", async (req, res) => {
  try {
    const payload = {
      Query: "status check from frontend",
      RecursionDepth: 1,
      OriginalSPrompt: "initial prompt",
      MessageHistory: { step1: "ok" },
      CurrentTime: Date.now() / 1000
    };
    const { data } = await axios.post(`${MCP_VISUALISER_URL}/query`, payload);
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Failed to call API", details: String(err) });
  }
});

app.get("/call-query-data", async (req, res) => {
  try {
    const payload = {
      Query: "status check from frontend",
      RecursionDepth: 1,
      OriginalSPrompt: "initial prompt",
      MessageHistory: { step1: "ok" },
      CurrentTime: Date.now() / 1000
    };
    const { data } = await axios.post(`${MCP_DATA_URL}/query`, payload);
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Failed to call API", details: String(err) });
  }
});

// Send a sample user query to MCPS
app.get("/call-user-query", async (req, res) => {
  try {
    const payload = {
      query: "Hello from frontend sample query!",
      system_prompt: "You are a helpful AI assistant.",
      chat_name: "frontend_debug_chat",
      debug_test: true,
      verbose: true
    };

    const { data } = await axios.post(`${MCPS_URL}/query`, payload, {
      headers: { "Content-Type": "application/json" }
    });

    res.json(data);
  } catch (err) {
    console.error("Error calling MCPS /query:", err.message);
    res.status(500).json({ error: "Failed to call MCPS /query", details: String(err) });
  }
});

// Send a sample user query to MCPS forcing full stack
app.get("/call-user-query-stack", async (req, res) => {
  try {
    const payload = {
      query: "Hello from frontend sample query!",
      system_prompt: "You are a helpful AI assistant.",
      chat_name: "frontend_debug_chat",
      debug_test: true,
      verbose: true
    };

    const { data } = await axios.post(`${MCPS_URL}/query-stack`, payload, {
      headers: { "Content-Type": "application/json" }
    });

    res.json(data);
  } catch (err) {
    console.error("Error calling MCPS /query-stack:", err.message);
    res.status(500).json({ error: "Failed to call MCPS /query-stack", details: String(err) });
  }
});

app.listen(FRONTEND_PORT, "0.0.0.0", () => {
  console.log(`Frontend running on port ${FRONTEND_PORT}`);
});

process.on("SIGTERM", () => {
  console.log("Frontend shutting down gracefully...");
  process.exit(0);
});
