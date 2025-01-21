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
    Classify the article into topics using OpenAI.

    Args:
        title (str): The title of the article.
        summary (str): The summary of the article.
        topics (list): Predefined list of topics. If None, GPT classifies freely.
        openai_client: OpenAI client for making API calls.

    Returns:
        str: A topic classification.
    """
    try:
        if topics:
            prompt = (
                f"Classify the following article into one of the topics: {', '.join(topics)}.\n\n"
                f"Title: {title}\n\n"
                f"Summary: {summary}"
            )
        else:
            prompt = (
                "Classify the following article into a broad category like AI, Technology, Business, "
                "Health, Science, Philosophy, or similar. Suggest a category if none fit.\n\n"
                f"Title: {title}\n\n"
                f"Summary: {summary}"
            )
        
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI classifier that categorizes articles into topics."},
                {"role": "user", "content": prompt},
            ],
        )
        classification = completion.choices[0].message.content.strip()

        if classification in topics:
            return classification
        else:
            return "Others"
    except Exception:
        return "Others"