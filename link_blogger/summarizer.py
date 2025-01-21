import os
from link_blogger.file_parser import load_yaml_config

def summarize_with_chatgpt(content, openai_client):
    """
    Summarize content using OpenAI.

    Args:
        content (str): The content to summarize.
        openai_client: OpenAI client for making API calls.

    Returns:
        str: A summary of the content.
    """
    # Default configuration
    default_config = {
        "model": "gpt-4o",
        "system_message": "You are a helpful assistant.",
        "user_message": (
            "Summarize the following text in one paragraph, using less than 500 chars. "
            "Provide the summary in English:\n\n{content}"
        ),
    }

    # Load configuration
    config_file = os.path.join(".conf", "summarization_prompt.yaml")
    config = load_yaml_config(config_file, default_config)

    # Prepare prompt
    user_message = config["user_message"].format(content=content)

    try:
        completion = openai_client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": config["system_message"]},
                {"role": "user", "content": user_message},
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing content: {e}"