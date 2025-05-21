# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS from your Node.js server or frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_script(script: UploadFile = File(...)):
    if not script.filename.endswith('.js'):
        raise HTTPException(status_code=400, detail="Only .js files allowed")

    content = await script.read()
    # Here’s where your script analysis magic happens
    # For now, return basic stats as a placeholder

    num_lines = content.decode('utf-8').count('\n') + 1
    size_kb = len(content) / 1024

    # Example: parse dependencies or call AI here...

    return {
        "filename": script.filename,
        "size_kb": round(size_kb, 2),
        "num_lines": num_lines,
        "message": "Script analyzed successfully"
    }
