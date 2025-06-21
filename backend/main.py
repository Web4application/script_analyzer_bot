# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List
from backend.llm import analyze_js_code, reorder_js_code, generate_readme
import subprocess

def push_to_github(repo_path: str, remote_name="origin"):
    subprocess.run(["git", "-C", repo_path, "init"])
    subprocess.run(["git", "-C", repo_path, "add", "."])
    subprocess.run(["git", "-C", repo_path, "commit", "-m", "Auto-generated README"])
    subprocess.run(["git", "-C", repo_path, "branch", "-M", "main"])
    subprocess.run(["git", "-C", repo_path, "remote", "add", remote_name, "<your-git-url>"])
    subprocess.run(["git", "-C", repo_path, "push", "-u", remote_name, "main"])

load_dotenv()

app = FastAPI(
    title="Script Analyzer Bot",
    description="Analyze JS dependencies, reorder files, and generate documentation with LLM",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeRequest(BaseModel):
    code: str


@app.post("/analyze")
async def analyze_endpoint(payload: CodeRequest):
    return {"analysis": analyze_js_code(payload.code)}


@app.post("/reorder")
async def reorder_endpoint(payload: CodeRequest):
    return {"order": reorder_js_code(payload.code)}


@app.post("/generate-doc")
async def generate_doc_endpoint(payload: CodeRequest):
    return {"readme": generate_readme(payload.code)}
