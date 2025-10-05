import json
import re, os
import shutil
from difflib import SequenceMatcher
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from .series_expert import series_expert
from .series_organizer import series_organizer
from google.adk.tools import FunctionTool
from google.adk.tools import LongRunningFunctionTool


load_dotenv()

# --- TOOL IMPLEMENTATION ---

class FileSearchTool:
    def __init__(self, json_path: str):
        with open(json_path, "r", encoding="utf-8") as f:
            self.files = json.load(f)
        self.index = list(self.files.keys())

    def normalize(self, text: str) -> str:
        return re.sub(r"[^a-z0-9 ]", " ", text.lower())

    def search(self, query: str, top_k: int = 5):
        norm_query = self.normalize(query)
        scored = []

        for path in self.index:
            filename = Path(path).name
            norm_filename = self.normalize(filename)

            score = SequenceMatcher(None, norm_query, norm_filename).ratio()
            if norm_query in norm_filename:
                score += 0.5

            scored.append((score, path))

        scored.sort(reverse=True, key=lambda x: x[0])

        results = []
        for score, path in scored[:top_k]:
            results.append({
                "path": path,
                "score": round(score, 3),
                "size": self.files[path]["size"],
                "mtime": self.files[path]["mtime"]
            })
        return results


# --- AGENT DEFINITION ---

# Wrap the tool so ADK knows about it
def search_files(query: str, top_k: int = 5) -> list[dict]:
    """
    Search for media files by title from the JSON index.
    Args:
        query: The search string (e.g. 'avatar season 1 episode 16').
        top_k: Max number of results to return.
    """
    file_tool = FileSearchTool(os.getenv("SCAN_OUTPUT"))
    return file_tool.search(query, top_k)

def list_directory(path: str) -> list[str]:
    """
    List files and directories in the given path.
    Args: 
    """
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Error: {str(e)}"]

def request_delete_directory_confirmation(dir_path: str) -> dict:
    return {
        'status': 'pending',
        'action': 'delete_directory',
        'directory_path': dir_path,
    }

def delete_directory(dir_path: str) -> str:
    """Execute the actual removal of a directory."""
    shutil.rmtree(dir_path)
    return dir_path

# Create the agent
root_agent = Agent(
    name="FileSearchAgent",
    model="gemini-2.0-flash",
    instruction=(
        "You are an assistant that helps users find files and directories by name from "
        "a JSON index. You are able to delete directories as well, after confirming with the user."
    ),
    tools=[search_files, list_directory, 
            LongRunningFunctionTool(func=request_delete_directory_confirmation),
            FunctionTool(delete_directory)],
    sub_agents=[series_expert, series_organizer]
)
