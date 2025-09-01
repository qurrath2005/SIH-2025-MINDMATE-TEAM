require("dotenv").config();
const express = require("express");
const connectDB = require("./db");
const authRoutes = require("./routes/auth");

const app = express();

// Middleware
app.use(express.json());

// Connect DB
connectDB();

// Routes
app.use("/api/auth", authRoutes);

const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
