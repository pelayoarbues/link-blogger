import pytest
from link_blogger.file_parser import get_recent_files, parse_metadata
from datetime import datetime, timedelta
import os

def test_get_recent_files(tmp_path):
    # Create sample files
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.touch()
    file2.touch()

    # Modify file2 to an earlier date
    earlier_date = datetime.now() - timedelta(days=10)
    os.utime(file2, (earlier_date.timestamp(), earlier_date.timestamp()))

    files = get_recent_files(tmp_path, days=7)
    assert len(files) == 1

def test_parse_metadata():
    content = """---
title: "Sample Title"
url: "https://example.com"
author: "Author Name"
---
Some content here."""
    metadata = parse_metadata(content)
    assert metadata["title"] == "Sample Title"
    assert metadata["url"] == "https://example.com"
    assert metadata["author"] == "Author Name"

def test_parse_metadata_with_missing_fields():
    content = """---
author: "Author Name"
---
Some content here."""
    metadata = parse_metadata(content)
    assert metadata["title"] == "Untitled Article"  # Default value
    assert metadata["url"] == "#"  # Default value