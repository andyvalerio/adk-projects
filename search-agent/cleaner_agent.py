from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import os
import json

import os
import json

_next_candidate_index = 0  # simple in-process checkpoint

def next_candidates_for_deletion(batch_size: int = 10) -> dict:
    """
    Return the next `batch_size` JSON entries whose paths are directly under SCAN_ROOT.
    Uses the JSON file pointed to by SCAN_OUTPUT.
    """
    global _next_candidate_index

    scan_output_path = os.getenv("SCAN_OUTPUT")
    scan_root = os.getenv("SCAN_ROOT")

    if not scan_output_path or not scan_root:
        raise ValueError("Both SCAN_OUTPUT and SCAN_ROOT must be set.")

    scan_root = os.path.normpath(scan_root)

    with open(scan_output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # keep only paths that are direct children of scan_root
    top_level = {
        path: info
        for path, info in data.items()
        if os.path.normpath(os.path.dirname(path)) == scan_root
    }

    all_items = sorted(top_level.items(), key=lambda x: x[0])
    start, end = _next_candidate_index, _next_candidate_index + batch_size
    batch = dict(all_items[start:end])
    _next_candidate_index = end

    return batch

def reset_next_candidate_index():
    """Reset the internal index to start from the beginning."""
    global _next_candidate_index
    _next_candidate_index = 0

# Create the agent
cleaner_agent = Agent(
    name="CleanerAgent",
    model="gemini-2.0-flash",
    instruction=(
        "You are an expert in identifying files and directories that are not interesting to the user and " \
        "can be deleted to free up disk space. You help the main agent by suggesting directories and files." \
    ),
    tools=[FunctionTool(next_candidates_for_deletion), FunctionTool(reset_next_candidate_index)],

)
