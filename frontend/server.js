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

app.get("/", (req, res) => {
  res.send(`
    <h1>MCO Frontend</h1>
    <p>Connected to API at: ${MCPS_URL}</p>
    <p><a href="/status">Check Multi Context Protocol Server (MCPS) Status</a></p>
  `);
});

app.get("/status", async (req, res) => {
  try {
    const { data } = await axios.get(`${MCPS_URL}/status`);
    res.send(`<h2>API Status: ${data.status}</h2>`);
  } catch (err) {
    res.send(`<h2>API Status: Unreachable</h2>`);
  }
});

app.listen(FRONTEND_PORT, "0.0.0.0", () => {
  console.log(`Frontend running on port ${FRONTEND_PORT}`);
});
