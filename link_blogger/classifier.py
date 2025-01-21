import os

def load_topics():
    """
    Load the list of topics from a configuration file.
    """
    topics_file = os.path.join(".conf", "topics.conf")
    if not os.path.exists(topics_file):
        raise FileNotFoundError(f"Topics configuration file not found at {topics_file}.")
    
    with open(topics_file, 'r', encoding='utf-8') as f:
        topics = [line.strip() for line in f if line.strip()]
    return topics

def classify_article_with_chatgpt(title, summary, topics, openai_client):
    """
    Classify the article into one of the predefined topics using OpenAI.

    Args:
        title (str): The title of the article.
        summary (str): The summary of the article.
        topics (list): Predefined list of topics.
        openai_client: OpenAI client for making API calls.

    Returns:
        str: A validated topic from the predefined list.
    """
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI classifier that categorizes articles into specific topics."},
                {
                    "role": "user",
                    "content": (
                        f"Classify the following article into one of the topics: {', '.join(topics)}.\n\n"
                        f"Title: {title}\n\n"
                        f"Summary: {summary}"
                    ),
                },
            ]
        )
        classification = completion.choices[0].message.content.strip()

        if classification in topics:
            return classification
        else:
            return "Others"
    except Exception:
        return "Others"