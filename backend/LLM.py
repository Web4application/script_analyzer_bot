import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_llm(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can change to gpt-3.5-turbo if needed
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024
    )
    return response['choices'][0]['message']['content'].strip()


def analyze_js_code(js_code: str) -> str:
    prompt = f"""
    Analyze the following JavaScript code and explain:
    - Module imports/exports
    - Key functions and classes
    - Dependency relationships
    
    ```javascript
    {js_code}
    ```
    """
    return ask_llm(prompt)


def reorder_js_code(js_code: str) -> str:
    prompt = f"""
    Given the following JavaScript code, determine and return a valid execution order
    of functions and modules, considering dependencies:

    ```javascript
    {js_code}
    ```
    """
    return ask_llm(prompt)


def generate_readme(js_code: str) -> str:
    prompt = f"""
    Generate a professional README.md section describing what this JavaScript code does.
    Include sections for:
    - Project Overview
    - Installation (if needed)
    - Features
    - Example Usage

    ```javascript
    {js_code}
    ```
    """
    return ask_llm(prompt)
