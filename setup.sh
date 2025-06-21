#!/bin/bash

echo "⚙️  Script Analyzer Bot: Setup Script Initializing..."

# --- ENV Setup ---
echo "📁 Creating virtual environment for Python backend..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt || pip install fastapi uvicorn openai pydantic

echo "📁 Creating .env template..."
cat <<EOF > .env
# === LLM Configuration ===
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# === Server Config ===
BACKEND_PORT=8000
FRONTEND_PORT=3000
EOF

# --- Node.js Setup ---
echo "📁 Installing Node.js dependencies..."
cd frontend || mkdir frontend && cd frontend
npm init -y
npm install axios dotenv chalk inquirer

echo "📁 Creating Node CLI entry point (index.js)..."
cat <<'EOF' > index.js
#!/usr/bin/env node
require('dotenv').config();
const inquirer = require('inquirer');
const axios = require('axios');

(async () => {
  const { filepath } = await inquirer.prompt([
    { type: 'input', name: 'filepath', message: 'Enter path to your JS file:' }
  ]);

  try {
    const res = await axios.post('http://localhost:8000/analyze', { filepath });
    console.log("🧠 Analysis Result:\n", res.data);
  } catch (err) {
    console.error("❌ Error:", err.message);
  }
})();
EOF
chmod +x index.js

cd ..

# --- Backend Run Script ---
echo "📁 Creating Python backend run script..."
cat <<'EOF' > run_backend.sh
#!/bin/bash
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
EOF
chmod +x run_backend.sh

# --- Docker Compose Scaffold (Optional) ---
echo "📁 Creating Docker scaffolding..."
cat <<EOF > docker-compose.yml
version: '3.9'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    command: node index.js
EOF

echo "📁 Creating .dockerignore and .gitignore..."
echo "node_modules\n.env\nvenv" > .dockerignore
echo "node_modules\n.env\nvenv\n__pycache__" > .gitignore

# --- Final Message ---
echo "✅ Setup Complete."
echo "➡️  Run: 'source venv/bin/activate && ./run_backend.sh'"
echo "➡️  Then: 'cd frontend && ./index.js' to analyze a script."

echo "📁 Creating CLI runner..."
cat <<EOF > autopilot_dev.sh
#!/bin/bash
source venv/bin/activate
python backend/autopilot_dev.py "\$@"
EOF
chmod +x autopilot_dev.sh
