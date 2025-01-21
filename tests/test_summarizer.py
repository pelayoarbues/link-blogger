from link_blogger.summarizer import summarize_with_chatgpt
from unittest.mock import MagicMock
import yaml


def test_summarize_with_chatgpt(mocker):
    mock_openai = mocker.MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "This is a summary."
    result = summarize_with_chatgpt("Sample content to summarize.", mock_openai)
    assert result == "This is a summary."


def test_summarize_with_yaml_config(tmp_path, mocker):
    # Mock OpenAI client
    mock_openai = MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "This is a test summary."

    # Create a temporary YAML file
    yaml_content = {
        "model": "gpt-4o",
        "system_message": "You are a helpful assistant.",
        "user_message": "Summarize this content: {content}"
    }
    yaml_path = tmp_path / "summarization_prompt.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f)

    # Mock the YAML file path
    mocker.patch("os.path.join", return_value=str(yaml_path))

    # Call the function
    content = "This is the content to summarize."
    result = summarize_with_chatgpt(content, mock_openai)

    # Assertions
    assert "This is a test summary." in result
    assert mock_openai.chat.completions.create.called

def test_summarize_fallback(tmp_path, mocker):
    # Mock OpenAI client
    mock_openai = MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "This is a fallback summary."

    # Ensure YAML file does not exist
    yaml_path = tmp_path / "missing_prompt.yaml"
    mocker.patch("os.path.join", return_value=str(yaml_path))

    # Call the function
    content = "Fallback content to summarize."
    result = summarize_with_chatgpt(content, mock_openai)

    # Assertions
    assert "This is a fallback summary." in result
    assert mock_openai.chat.completions.create.called