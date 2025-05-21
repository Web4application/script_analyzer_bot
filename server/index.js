// Server/index.js
import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import fileUpload from 'express-fileupload';
import fetch from 'node-fetch';
import FormData from 'form-data';

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(fileUpload());
app.use(morgan('dev'));

app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.post('/api/analyze', async (req, res) => {
  try {
    if (!req.files || !req.files.script) {
      return res.status(400).json({ error: 'No script file uploaded' });
    }

    const scriptFile = req.files.script;

    // Prepare form data for Python backend
    const formData = new FormData();
    formData.append('script', scriptFile.data, scriptFile.name);

    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      body: formData,
      headers: formData.getHeaders(),
    });

    if (!response.ok) {
      const error = await response.json();
      return res.status(response.status).json({ error: error.detail || 'Analysis failed' });
    }

    const analysisResult = await response.json();
    res.json(analysisResult);

  } catch (error) {
    console.error('Error in /api/analyze:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Something went wrong!' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
