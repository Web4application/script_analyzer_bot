import json
import sys
import openai
import os
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")

def load_failures(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return [t for t in data.get("tests", []) if t.get("outcome") == "failed"]

def generate_fix_prompt(failure):
    return f"""
A test failed in the following context:

Test name: {failure['name']}
Error message: {failure['message']}
Stack trace: {failure.get('traceback', '')}

Please suggest a corrected version of the test or the function it calls, with explanation.
"""

def suggest_fix(failures):
    for fail in failures:
        prompt = generate_fix_prompt(fail)
        print(f"🧠 Prompting LLM for: {fail['name']}")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        print("🔧 Suggested Fix:\n", response['choices'][0]['message']['content'])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ci_llm_fix.py <test-results.json>")
        sys.exit(1)
    failures = load_failures(sys.argv[1])
    if not failures:
        print("✅ No failures found.")
    else:
        suggest_fix(failures)
