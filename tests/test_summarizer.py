from link_blogger.summarizer import summarize_with_chatgpt

def test_summarize_with_chatgpt(mocker):
    mock_openai = mocker.MagicMock()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = "This is a summary."
    result = summarize_with_chatgpt("Sample content to summarize.", mock_openai)
    assert result == "This is a summary."