from link_blogger.markdown_writer import generate_introduction_with_chatgpt, save_to_markdown
from pathlib import Path
import yaml

def test_save_to_markdown(tmp_path):
    grouped_summaries = {"AI": ["- AI Summary 1"], "Management": ["- Management Summary 1"]}
    introduction = "This is an introduction."
    output_dir = tmp_path / "output"
    save_to_markdown(grouped_summaries, introduction, output_dir)

    output_file = list(output_dir.iterdir())[0]
    assert output_file.exists()
    assert output_file.read_text().startswith("---")


def test_generate_introduction_with_yaml_config(tmp_path, mocker):
    # Mock OpenAI client
    mock_openai = mocker.MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "This is a test introduction."

    # Create a temporary YAML file
    yaml_content = {
        "model": "gpt-4o",
        "system_message": "You are a creative assistant.",
        "user_message": "Test intro for {topics}. Details: {article_context}"
    }
    yaml_path = tmp_path / "introduction_prompt.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f)

    # Mock the YAML file path
    mocker.patch("os.path.join", return_value=str(yaml_path))

    # Prepare test input
    article_details = [
        {"title": "AI Innovations", "topic": "AI", "summary": "Advances in AI."},
        {"title": "Management Tips", "topic": "Management", "summary": "Leadership insights."},
    ]

    # Call the function
    result = generate_introduction_with_chatgpt(article_details, mock_openai)

    # Assertions
    # Ensure result is non-empty
    assert len(result) > 0

def test_generate_introduction_fallback(tmp_path, mocker):
    # Mock OpenAI client
    mock_openai = mocker.MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "This is a fallback introduction about AI."

    # Ensure YAML file does not exist
    yaml_path = tmp_path / "missing_prompt.yaml"
    mocker.patch("os.path.join", return_value=str(yaml_path))

    # Prepare test input
    article_details = [
        {"title": "AI Innovations", "topic": "AI", "summary": "Advances in AI."},
    ]

    # Call the function
    result = generate_introduction_with_chatgpt(article_details, mock_openai)

    # Assertions
    assert "AI" in result
    # Ensure result is non-empty
    assert len(result) > 0