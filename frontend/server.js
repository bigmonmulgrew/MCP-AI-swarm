import express from "express";
import axios from "axios";
import dotenv from "dotenv";

// Load .env variables
dotenv.config();

const app = express();

const FRONTEND_PORT = process.env.FRONTEND_PORT_I || 5173;

// Get MCPS config from .env
const MCPS_HOST = process.env.MCPS_HOST || "localhost";
const MCPS_PORT = process.env.MCPS_PORT_I || 8080;

// Build the full URL for the MCPS server
const MCPS_URL = `http://${MCPS_HOST}:${MCPS_PORT}`;

// Direct connections to MCP drones
const MCP_VISUALISER_URL = process.env.MCP_VISUALISER_URL || "http://localhost:8070";
const MCP_DATA_URL = process.env.MCP_DATA_URL || "http://localhost:8060";

app.get("/", (req, res) => {
  res.send(`
    <h1>MCO Frontend</h1>
    <p>Connected to API at: ${MCPS_URL}</p>
    <p><a href="/status">Check Multi Context Protocol Server (MCPS) Status</a></p>

    <hr/>
    <button id="callBtn">Call /query on Visualiser</button>
    <pre id="out" style="white-space:pre-wrap; border:1px solid #ccc; padding:8px; max-height:300px; overflow:auto;"></pre>

    <script>
      document.getElementById('callBtn').addEventListener('click', async () => {
        try {
          const resp = await fetch('/call-query');
          const data = await resp.json();
          console.log('API response:', data);
          document.getElementById('out').textContent = JSON.stringify(data, null, 2);
        } catch (err) {
          console.error('Error calling /call-query:', err);
          document.getElementById('out').textContent = 'Error: ' + err;
        }
      });
    </script>

    <button id="callBtnData">Call /query on Data</button>
    <pre id="out2" style="white-space:pre-wrap; border:1px solid #ccc; padding:8px; max-height:300px; overflow:auto;"></pre>

    <script>
      document.getElementById('callBtnData').addEventListener('click', async () => {
        try {
          const resp = await fetch('/call-query-data');
          const data = await resp.json();
          console.log('API response:', data);
          document.getElementById('out2').textContent = JSON.stringify(data, null, 2);
        } catch (err) {
          console.error('Error calling /call-query-data:', err);
          document.getElementById('out2').textContent = 'Error: ' + err;
        }
      });
    </script>
  `);
});

app.get("/status", async (req, res) => {
  try {
    const { data } = await axios.get(`${MCP_VISUALISER_URL}/status`);
    res.send(`<h2>API Status: ${data.status}</h2>`);
  } catch (err) {
    res.send(`<h2>API Status: Unreachable</h2>`);
  }
});

// New proxy route: server-side posts to API_URL/query to avoid browser CORS issues
app.get("/call-query", async (req, res) => {
  try {
    const payload = {
      Query: "status check from frontend",
      RecursionDepth: 1,
      OriginalSPrompt: "initial prompt",
      MessageHistory: { step1: "ok" },
      CurrentTime: Date.now() / 1000
    };

    const { data } = await axios.post(`${MCP_VISUALISER_URL}/query`, payload, {
      headers: { "Content-Type": "application/json" }
    });

    res.json(data);
  } catch (err) {
    console.error(err && err.message ? err.message : err);
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

    const { data } = await axios.post(`${MCP_DATA_URL}/query`, payload, {
      headers: { "Content-Type": "application/json" }
    });

    res.json(data);
  } catch (err) {
    console.error(err && err.message ? err.message : err);
    res.status(500).json({ error: "Failed to call API", details: String(err) });
  }
});

// New proxy route: server-side posts to API_URL/query to avoid browser CORS issues
app.get("/call-query", async (req, res) => {
  try {
    const payload = {
      Query: "status check from frontend",
      RecursionDepth: 1,
      OriginalSPrompt: "initial prompt",
      MessageHistory: { step1: "ok" },
      CurrentTime: Date.now() / 1000
    };

    const { data } = await axios.post(`${MCP_VISUALISER_URL}/query`, payload, {
      headers: { "Content-Type": "application/json" }
    });

    res.json(data);
  } catch (err) {
    console.error(err && err.message ? err.message : err);
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

    const { data } = await axios.post(`${MCP_DATA_URL}/query`, payload, {
      headers: { "Content-Type": "application/json" }
    });

    res.json(data);
  } catch (err) {
    console.error(err && err.message ? err.message : err);
    res.status(500).json({ error: "Failed to call API", details: String(err) });
  }
});

app.listen(FRONTEND_PORT, "0.0.0.0", () => {
  console.log(`Frontend running on port ${FRONTEND_PORT}`);
});