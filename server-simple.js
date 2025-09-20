const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from frontend build
app.use(express.static(path.join(__dirname, 'frontend/build')));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    service: 'Comedy Social Platform'
  });
});

// API endpoints
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    api: 'comedy-social-api',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/posts', (req, res) => {
  res.json([
    {
      id: 1,
      content: "Why don't scientists trust atoms? Because they make up everything!",
      author: "ComedyBot",
      likes: 42,
      timestamp: new Date().toISOString()
    },
    {
      id: 2,
      content: "I told my wife she was drawing her eyebrows too high. She looked surprised.",
      author: "JokesMaster",
      likes: 38,
      timestamp: new Date().toISOString()
    }
  ]);
});

// Catch all handler for React routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/build', 'index.html'));
});

// Error handling
app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`API: http://localhost:${PORT}/api/health`);
});