import os
from datetime import datetime, timedelta

from link_blogger.file_parser import load_yaml_config

def generate_introduction_with_chatgpt(article_details, openai_client):
    """
    Generate an engaging introduction for the blog post using OpenAI.

    Args:
        article_details (list): List of dictionaries with article information (title, topic, summary).
        openai_client: OpenAI client for making API calls.

    Returns:
        str: Generated introduction text.
    """
    # Default configuration
    default_config = {
        "model": "gpt-4o",
        "system_message": "You are a creative assistant that writes introductions for blog posts. \
                          You are really able to get to the core of the content and provide a concise summary.",
        "user_message": (
            "Every week you write an update post of recent readings. Write a concise and engaging introduction for a blog post summarizing recent readings. "
            "Provide a two sentences long introduction. Try to be really concise, consider the {topics} and the provided highlights of articles:\n\n{details}"
        ),
    }

    # Load configuration
    config_file = os.path.join(".conf", "introduction_prompt.yaml")
    config = load_yaml_config(config_file, default_config)

    # Prepare prompt
    topics = ", ".join({article['topic'] for article in article_details})
    article_context = "\n".join(
        f"Title: {article['title']}, Topic: {article['topic']}, Summary: {article['summary']}"
        for article in article_details
    )
    user_message = config["user_message"].format(topics=topics, article_context=article_context)

    try:
        completion = openai_client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": config["system_message"]},
                {"role": "user", "content": user_message},
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return "This post summarizes my recent readings on various topics, providing insights and key takeaways."

def save_to_markdown(grouped_summaries, introduction, output_dir):
    """
    Save summaries and introduction to a Markdown file.

    Args:
        grouped_summaries (dict): Summaries grouped by topic.
        introduction (str): Introduction text.
        output_dir (str): Directory to save the file.

    Returns:
        None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"wrapped_up_readings_{today}.md"
    filepath = os.path.join(output_dir, filename)

    frontmatter = f"""---
title: Wrapped-up Readings {today}
date: {today}
tags:
  - link-blog
---

"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(introduction + "\n\n")
        for topic, summaries in grouped_summaries.items():
            f.write(f"## {topic}\n\n")
            for summary in summaries:
                f.write(summary + "\n")