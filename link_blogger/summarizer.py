def summarize_with_chatgpt(content, openai_client):
    """
    Summarize content using OpenAI.

    Args:
        content (str): The content to summarize.
        openai_client: OpenAI client for making API calls.

    Returns:
        str: A summary of the content.
    """
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following text in one paragraph, using less than 500 chars. Provide the summary in English:\n\n{content}"}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing content: {e}"