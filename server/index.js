// Server/index.js
import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import fileUpload from 'express-fileupload';
import path from 'path';

// Initialize app
const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(cors()); // Allow cross-origin for frontend
app.use(express.json()); // Parse JSON payloads
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded payloads
app.use(fileUpload()); // For file uploads
app.use(morgan('dev')); // Logging HTTP requests for debugging

// Basic health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// API endpoint: Upload and analyze script file
app.post('/api/analyze', async (req, res) => {
  try {
    if (!req.files || !req.files.script) {
      return res.status(400).json({ error: 'No script file uploaded' });
    }

    const scriptFile = req.files.script;
    // Here you might save the file, then call your Python backend or analyze here
    // For now, just return some basic info as placeholder

    // For example, save the file temporarily (optional)
    const uploadPath = path.join(__dirname, 'uploads', scriptFile.name);
    await scriptFile.mv(uploadPath);

    // TODO: Integrate with Python backend or LLM service here to analyze the script

    // Dummy response:
    res.json({
      message: 'File received, analysis pending',
      filename: scriptFile.name,
      size: scriptFile.size,
    });
  } catch (error) {
    console.error('Error processing analysis:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// 404 for unknown routes
app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Script Analyzer Bot server running on port ${PORT}`);
});
