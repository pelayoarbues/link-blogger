import os
import argparse
import re
from datetime import datetime, timedelta
from collections import defaultdict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .conf folder
load_dotenv(dotenv_path=".conf/openai.conf")

# Set OpenAI API key from environment variable
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not openai_client:
    raise ValueError("OpenAI API key is not set. Please define it in the .conf/openai.conf file.")

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

def get_recent_files(directory, days=7, exclude_patterns=None):
    recent_files = []
    now = datetime.now()
    cutoff_date = now - timedelta(days=days)
    exclude_patterns = exclude_patterns or []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):  # Ensure it's a file
            if any(re.search(pattern, filename) for pattern in exclude_patterns):
                continue  # Skip files matching exclude patterns
            modification_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if modification_time >= cutoff_date:
                recent_files.append(filepath)
    
    return recent_files

def parse_metadata(file_content):
    metadata = {}
    metadata_pattern = re.compile(r"---(.*?)---", re.DOTALL)
    match = metadata_pattern.search(file_content)
    if match:
        metadata_block = match.group(1)
        for line in metadata_block.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip().lower()] = value.strip().strip('"')
    
    url_pattern = re.compile(r"- URL:\s*(https?://\S+)", re.IGNORECASE)
    url_match = url_pattern.search(file_content)
    if url_match:
        metadata["url"] = url_match.group(1)

    return metadata

def summarize_with_chatgpt(content):
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

def classify_article_with_chatgpt(title, summary, topics):
    """
    Classify the article into one of the predefined topics using OpenAI.

    Args:
        title (str): The title of the article.
        summary (str): The summary of the article.
        topics (list): Predefined list of topics.

    Returns:
        str: A validated topic from the predefined list.
    """
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are an AI classifier that categorizes articles into specific topics."},
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

        # Validate the classification against the predefined topics
        if classification in topics:
            return classification
        else:
            return "Others"
    except Exception as e:
        return "Others"

def review_and_summarize_readings(files, topics):
    grouped_summaries = defaultdict(list)
    article_details = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            metadata = parse_metadata(content)
            title = metadata.get("title", "Untitled")
            url = metadata.get("url", "#")
            summary = summarize_with_chatgpt(content)
            topic = classify_article_with_chatgpt(title, summary, topics)
            formatted_summary = f"- [{title}]({url}): {summary}"
            grouped_summaries[topic].append(formatted_summary)
            article_details.append({"title": title, "url": url, "summary": summary, "topic": topic})
    return grouped_summaries, article_details

def generate_introduction_with_chatgpt(article_details):
    try:
        details = "\n".join(
            f"Title: {article['title']}, Topic: {article['topic']}, Summary: {article['summary']}" for article in article_details
        )
        topics = ", ".join(set(article['topic'] for article in article_details))
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a creative assistant that writes introductions for blog posts. \
                                You are really able to get to the core of the content and provide a concise summary."},
                {
                    "role": "user",
                    "content": (
                        f"Every week you write an update post of recent readings."
                        f"Provide a two sentences long introduction. Try to be really concise, consider the {topics} and the provided highlights of articles:\n\n{details}"
                    ),
                },
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return "This post summarizes my recent readings on various topics, providing insights and key takeaways."


def save_to_markdown(grouped_summaries, introduction, output_dir):
    """
    Save the summaries to a Markdown file with grouped topics.
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
            f.write("\n".join(summaries) + "\n\n")

    print(f"Markdown file saved to {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Review and summarize recent reading files.")
    parser.add_argument("directory", type=str, help="Directory containing your reading files.")
    parser.add_argument("--days", type=int, default=7, help="Number of days to review (default: 7).")
    parser.add_argument("--output_dir", type=str, default="./summaries", help="Directory to save the Markdown file (default: current directory).")
    parser.add_argument("--exclude", nargs="*", help="Patterns of files to exclude (e.g., '^000', '\\.pdf$').")
    args = parser.parse_args()

    directory = args.directory
    days = args.days
    output_dir = args.output_dir
    exclude_patterns = args.exclude or ["^000", r"\.pdf$"]

    topics = load_topics()

    print(f"\nSearching for files in '{directory}' modified in the last {days} days...\n")
    recent_files = get_recent_files(directory, days, exclude_patterns)

    if not recent_files:
        print("No files found.")
        return

    print(f"Found {len(recent_files)} file(s):")
    for file in recent_files:
        print(f" - {file}")

    print("\nGenerating summaries and classifications...\n")
    grouped_summaries, article_details = review_and_summarize_readings(recent_files, topics)

    print("\nGenerating short introduction...\n")
    introduction = generate_introduction_with_chatgpt(article_details)

    print("Saving to Markdown file...")
    save_to_markdown(grouped_summaries, introduction, output_dir)

if __name__ == "__main__":
    main()