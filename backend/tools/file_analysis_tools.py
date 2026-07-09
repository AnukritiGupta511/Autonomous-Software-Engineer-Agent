import os
from typing import Dict, List, Any
from langchain_core.tools import tool

@tool
def analyze_file_tool(file_path: str) -> Dict[str, Any]:
    """Analyzes a single file to determine language and line count."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        ext = os.path.splitext(file_path)[1].lower()
        lines = content.splitlines()
        
        return {
            "file_path": file_path,
            "extension": ext,
            "line_count": len(lines),
            "size_bytes": len(content),
            "preview": "\n".join(lines[:10]) + ("\n..." if len(lines) > 10 else "")
        }
    except Exception as e:
        return {"error": f"Failed to analyze file: {str(e)}"}

@tool
def get_project_structure_tool(directory: str, max_depth: int = 3) -> Dict[str, Any]:
    """Gets the directory tree structure for a project."""
    if not os.path.exists(directory):
        return {"error": f"Directory not found: {directory}"}
        
    def _build_tree(path, depth):
        if depth > max_depth:
            return "..."
            
        tree = {}
        try:
            for item in os.listdir(path):
                # Skip common hidden/build dirs
                if item in ['.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build']:
                    continue
                    
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    tree[item] = _build_tree(full_path, depth + 1)
                else:
                    tree[item] = "file"
        except Exception as e:
            tree["_error"] = str(e)
        return tree
        
    return _build_tree(directory, 1)
