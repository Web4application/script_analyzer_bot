import os
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import openai

app = FastAPI()

# Configure your OpenAI API key securely (use env vars in production!)
openai.api_key = os.getenv("OPENAI_API_KEY")

class FileContent(BaseModel):
    filename: str
    content: str

class AnalyzeRequest(BaseModel):
    files: List[FileContent]

def parse_dependencies_from_content(content: str) -> List[str]:
    pattern = re.compile(r'import\s+(?:[\w{}\s,*]+from\s+)?[\'"](.+?)[\'"];?')
    dependencies = []
    for line in content.splitlines():
        match = pattern.search(line)
        if match:
            dep = match.group(1)
            if dep.startswith(('.', '/')):
                dependencies.append(dep)
    return dependencies

def build_dependency_graph(files: List[FileContent]) -> Dict[str, List[str]]:
    graph = {}
    file_dict = {f.filename: f for f in files}
    for f in files:
        deps = parse_dependencies_from_content(f.content)
        normalized_deps = []
        base_dir = os.path.dirname(f.filename)
        for dep in deps:
            dep_path = os.path.normpath(os.path.join(base_dir, dep))
            if not dep_path.endswith('.js'):
                dep_path += '.js'
            # Only include if file exists in the given list
            if dep_path in file_dict:
                normalized_deps.append(dep_path)
        graph[f.filename] = normalized_deps
    return graph

def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    visited = set()
    temp_mark = set()
    result = []

    def visit(node):
        if node in temp_mark:
            raise HTTPException(status_code=400, detail=f"Cyclic dependency detected at {node}")
        if node not in visited:
            temp_mark.add(node)
            for neighbor in graph.get(node, []):
                visit(neighbor)
            temp_mark.remove(node)
            visited.add(node)
            result.append(node)

    for node in graph:
        if node not in visited:
            visit(node)
    return result[::-1]

def detect_unused_imports(content: str) -> List[str]:
    import_pattern = re.compile(r'import\s+(?:([\w{},*\s]+)\s+from\s+)?[\'"].+?[\'"];?')
    imports = {}
    lines = content.splitlines()
    for line in lines:
        m = import_pattern.match(line)
        if m:
            imported = m.group(1)
            if imported:
                ids = [x.strip(' {}') for x in imported.split(',')]
                for id_ in ids:
                    imports[id_] = True

    unused = []
    for ident in imports.keys():
        # crude usage check, ignoring import line itself
        usage_count = content.count(ident) - 1
        if usage_count <= 0:
            unused.append(ident)
    return unused

async def generate_readme_summary(files: List[FileContent]) -> str:
    combined_code = ""
    for f in files:
        combined_code += f"\n\n// File: {f.filename}\n" + f.content

    prompt = (
        "You are a seasoned developer and documenter. "
        "Generate a concise README summary describing the purpose and functionality of this codebase:\n\n"
        + combined_code
    )

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    return response.choices[0].message.content

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    files = request.files
    graph = build_dependency_graph(files)
    try:
        order = topological_sort(graph)
    except HTTPException as e:
        return {"error": e.detail}

    unused_map = {}
    for f in files:
        unused = detect_unused_imports(f.content)
        if unused:
            unused_map[f.filename] = unused

    readme = await generate_readme_summary(files)

    return {
        "execution_order": order,
        "unused_imports": unused_map,
        "readme_summary": readme
    }
