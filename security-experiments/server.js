require("dotenv").config();
const express = require("express");
const connectDB = require("./db");

const app = express();

// connect to MongoDB
connectDB();

app.get("/", (req, res) => {
  res.send("MindMate Security Test ✅");
});

const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
