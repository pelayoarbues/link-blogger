import os
from datetime import datetime, timedelta

def generate_introduction_with_chatgpt(article_details, openai_client):
    """
    Generate an engaging introduction for the blog post using OpenAI.

    Args:
        article_details (list): List of dictionaries with article information (title, topic, summary).
        openai_client: OpenAI client for making API calls.

    Returns:
        str: Generated introduction text.
    """
    try:
        topics = ", ".join({article['topic'] for article in article_details})
        article_context = "\n".join(
            f"Title: {article['title']}, Topic: {article['topic']}, Summary: {article['summary']}"
            for article in article_details
        )
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a really experienced and creative assistant that writes introductions for blog posts. \
                                You are really able to get to the core of the content and provide a concise summary."},
                {
                    "role": "user",
                    "content": (
                        f"Every week you write an update post of recent readings."
                        f"Provide a two sentences long introduction. Try to be really concise, use first person, consider the {topics} and the provided highlights of articles:\n\n{details}"
                    ),
                },
            ]
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
title: Wrapped-up readings {today}
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