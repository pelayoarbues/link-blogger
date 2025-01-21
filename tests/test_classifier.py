import pytest
from link_blogger.classifier import load_topics, classify_article_with_chatgpt

def test_load_topics(monkeypatch, tmp_path):
    # Create a mock topics.conf
    topics_file = tmp_path / "topics.conf"
    topics_file.write_text("AI\nTechnology\nManagement")

    monkeypatch.setattr("os.path.join", lambda *args: str(topics_file))
    topics = load_topics()
    assert topics == ["AI", "Technology", "Management"]

def test_classify_article_with_chatgpt(mocker):
    mock_openai = mocker.MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "AI"
    result = classify_article_with_chatgpt(
        "Sample Title",
        "Sample Summary",
        ["AI", "Technology", "Management"],
        mock_openai,
    )
    assert result == "AI"

def test_classify_article_without_topics(mocker):
    mock_openai = mocker.MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "AI"
    result = classify_article_with_chatgpt(
        "AI in the times of Covid",
        "AI is helping in the fight against Covid.",
        ["AI", "Management"],  # No topics provided
        mock_openai,
    )
    assert result == "AI"