import pytest
from pathlib import Path
import subprocess

def test_generate_link_post_integration(tmp_path, mocker):
    # Mock the OpenAI client
    mock_openai = mocker.patch("generate_link_post.OpenAI")

    # Create sample files
    file_content = """---
title: "Sample Article"
url: "https://example.com"
---
Sample highlights."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text(file_content)

    output_dir = tmp_path / "output"

    # Run the script
    subprocess.run(
        [
            "python",
            "generate_link_post.py",
            str(tmp_path),
            "--output_dir",
            str(output_dir),
        ],
        check=True,
    )

    # Check output
    output_file = list(output_dir.iterdir())[0]
    assert output_file.exists()
    assert "Sample Article" in output_file.read_text()