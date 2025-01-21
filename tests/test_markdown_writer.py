from link_blogger.markdown_writer import generate_introduction_with_chatgpt, save_to_markdown
from pathlib import Path

def test_generate_introduction_with_chatgpt(mocker):
    mock_openai = mocker.MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "This is an introduction."
    article_details = [
        {"title": "AI Innovations", "topic": "AI", "summary": "Advances in AI."},
        {"title": "Management Tips", "topic": "Management", "summary": "Leadership insights."},
    ]
    result = generate_introduction_with_chatgpt(article_details, mock_openai)
    # Ensure result is non-empty
    assert len(result) > 0

def test_save_to_markdown(tmp_path):
    grouped_summaries = {"AI": ["- AI Summary 1"], "Management": ["- Management Summary 1"]}
    introduction = "This is an introduction."
    output_dir = tmp_path / "output"
    save_to_markdown(grouped_summaries, introduction, output_dir)

    output_file = list(output_dir.iterdir())[0]
    assert output_file.exists()
    assert output_file.read_text().startswith("---")