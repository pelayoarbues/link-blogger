import os
import re
from datetime import datetime, timedelta

def get_recent_files(directory, days=7, exclude_patterns=None):
    """
    Get files modified within the last `days` days.

    Args:
        directory (str): Path to the directory to scan.
        days (int): Number of days to look back.
        exclude_patterns (list): List of regex patterns to exclude files.

    Returns:
        list: List of file paths.
    """
    recent_files = []
    now = datetime.now()
    cutoff_date = now - timedelta(days=days)
    exclude_patterns = exclude_patterns or []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):  # Ensure it's a file
            if any(re.search(pattern, filename) for pattern in exclude_patterns):
                continue
            modification_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if modification_time >= cutoff_date:
                recent_files.append(filepath)
    
    return recent_files

def parse_metadata(file_content):
    """
    Extract metadata from file content.

    Args:
        file_content (str): Content of the file.

    Returns:
        dict: Metadata dictionary with keys like 'title', 'url', etc.
    """
    metadata = {}
    metadata_pattern = re.compile(r"---(.*?)---", re.DOTALL)
    match = metadata_pattern.search(file_content)
    if match:
        metadata_block = match.group(1)
        for line in metadata_block.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip().lower()] = value.strip().strip('"')
    
    # Default values for missing metadata
    metadata["title"] = metadata.get("title", "Untitled Article")
    metadata["url"] = metadata.get("url", "#")
    
    return metadata