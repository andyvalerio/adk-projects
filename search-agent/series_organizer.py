from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools import LongRunningFunctionTool
from google.adk.tools.tool_context import ToolContext
import re, os

def suggest_new_path(file_path: str, info: dict) -> str:
    """
    Suggest a new correct location of the file based on series info.
    Args:
        file_path: The current path to the file.
        info: A dictionary with 'series', 'season', and 'episode' keys.
    Returns:
        The new path suggested.
    """
    # Extract series info
    series_name = re.sub(r'[^\w.-]', '.', info['series'])
    
    # Construct the destination directory path
    base_dir = os.getenv('SCAN_ROOT', os.path.dirname(file_path))

    series_dir = os.path.join(base_dir, series_name)
    
    # Create directories if they don't exist
    os.makedirs(series_dir, exist_ok=True)
    
    # Get the original filename
    filename = os.path.basename(file_path)
    
    # Construct new file path
    new_path = os.path.join(series_dir, filename)
    
    return new_path

# TODO This is an easy way to handle confirmation, but not very safe. The model 
# could just ignore it. The proper way is to use FunctionTool with a callback to get 
# confirmation. Good enough for local use for now.
def request_move_confirmation(file_path: str, new_path: str) -> dict:
    """
    Request confirmation for moving a file.
    Args:
        file_path: Source path of the file
        new_path: Destination path for the file
    Returns:
        Dictionary with confirmation status and details
    """
    return {
        'status': 'pending',
        'action': 'move_file',
        'source': file_path,
        'destination': new_path
    }

def move_file(file_path: str, new_path: str) -> str:
    """Execute the actual file move operation."""
    os.rename(file_path, new_path)
    return new_path
    
# Create the agent
series_organizer = Agent(
    name="SeriesOrganizerAgent",
    model="gemini-2.0-flash",
    instruction=(
        "You are an expert at organizing TV series video and subtitle files. You take as input the path" \
        "to a certain video or subtitle file, for example: " \
        "/data/mnt/f/tv_series/Silicon.Valley.S06E03.WEB-DLRip.RGzsRutracker.[Wentworth_Miller].avi" \
        "and the information about that episode, for example:" \
        "{'series': 'Silicon Valley', 'season': 6, 'episode': 3}" \
        "and with the help of suggest_new_path tool you are able to understand where that file "
        "should be placed. In the above example it should be placed in:" \
        "/data/mnt/f/tv_series/Silicon.Valley/" \
        "Then, with the help of a tool, when requested you move the file to the correct location. Moving "
        "the file is always subjected to human confirmation. "
        "You'll get a confirmation request with status 'pending' first."
    ),
    tools=[
        suggest_new_path,
        LongRunningFunctionTool(func=request_move_confirmation),
        FunctionTool(move_file)
    ],
)