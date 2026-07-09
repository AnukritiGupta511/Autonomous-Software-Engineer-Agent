import os
import git
from typing import Dict, List, Any
from langchain_core.tools import tool
import httpx
from config.settings import settings

@tool
def clone_repository_tool(github_url: str, target_dir: str) -> str:
    """Clones a GitHub repository to a local directory."""
    try:
        if os.path.exists(target_dir):
            return f"Directory {target_dir} already exists."
        git.Repo.clone_from(github_url, target_dir)
        return f"Successfully cloned {github_url} to {target_dir}"
    except Exception as e:
        return f"Error cloning repository: {str(e)}"

@tool
def get_repo_info_tool(owner: str, repo: str) -> Dict[str, Any]:
    """Gets metadata for a GitHub repository using the GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"
        
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            "name": data.get("name"),
            "description": data.get("description"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "language": data.get("language"),
            "default_branch": data.get("default_branch")
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def list_repo_files_tool(owner: str, repo: str, branch: str = "main") -> List[str]:
    """Lists all files in a repository branch using the GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"
        
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]
    except Exception as e:
        return [f"Error: {str(e)}"]
