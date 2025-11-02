import express from "express";
import axios from "axios";

const app = express();
const PORT = process.env.PORT || 5173;
const API_URL = process.env.API_URL || "http://localhost:8080";

app.get("/", (req, res) => {
  res.send(`
    <h1>MCO Frontend</h1>
    <p>Connected to API at: ${API_URL}</p>
    <p><a href="/status">Check API Status</a></p>
  `);
});

app.get("/status", async (req, res) => {
  try {
    const { data } = await axios.get(`${API_URL}/status`);
    res.send(`<h2>API Status: ${data.status}</h2>`);
  } catch (err) {
    res.send(`<h2>API Status: Unreachable</h2>`);
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Frontend running on port ${PORT}`);
});
