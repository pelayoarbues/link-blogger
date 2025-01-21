from openai import OpenAI
from dotenv import load_dotenv
from collections import defaultdict
import os
import argparse
from link_blogger.file_parser import get_recent_files, parse_metadata
from link_blogger.summarizer import summarize_with_chatgpt
from link_blogger.classifier import classify_article_with_chatgpt, load_topics
from link_blogger.markdown_writer import save_to_markdown, generate_introduction_with_chatgpt

def main():
    # Load environment variables from the .conf folder
    load_dotenv(dotenv_path=".conf/openai.conf")

    # Set OpenAI API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is not set. Please define it in the .conf/openai.conf file.")

    # Initialize the OpenAI client
    openai_client = OpenAI(api_key=api_key)

    parser = argparse.ArgumentParser(description="Review and summarize recent reading files.")
    parser.add_argument("directory", type=str, help="Directory containing your reading files.")
    parser.add_argument("--days", type=int, default=7, help="Number of days to review (default: 7).")
    parser.add_argument("--output_dir", type=str, default="./summaries", help="Directory to save the Markdown file.")
    parser.add_argument("--exclude", nargs="*", help="Patterns of files to exclude.")
    args = parser.parse_args()

    directory = args.directory
    days = args.days
    output_dir = args.output_dir
    exclude_patterns = args.exclude or ["^000", r"\.pdf$"]

    # Load topics
    topics = load_topics()

    # Fetch recent files
    print(f"\nSearching for files in '{directory}' modified in the last {days} days...\n")
    recent_files = get_recent_files(directory, days, exclude_patterns)

    if not recent_files:
        print("No files found.")
        return

    print(f"Found {len(recent_files)} file(s):")
    for file in recent_files:
        print(f" - {file}")

    # Process files: summarize and classify
    print("\nGenerating summaries and classifications...\n")
    grouped_summaries = defaultdict(list)
    article_details = []
    for file in recent_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            metadata = parse_metadata(content)
            title = metadata["title"]
            url = metadata["url"]
            summary = summarize_with_chatgpt(content, openai_client)
            topic = classify_article_with_chatgpt(title, summary, topics, openai_client)
            grouped_summaries[topic].append(f"- [{title}]({url}): {summary}")
            article_details.append({"title": title, "url": url, "summary": summary, "topic": topic})

    # Generate introduction with OpenAI
    print("\nGenerating introduction...\n")
    introduction = generate_introduction_with_chatgpt(article_details, openai_client)

    # Save to Markdown
    print("Saving to Markdown file...")
    save_to_markdown(grouped_summaries, introduction, output_dir)

if __name__ == "__main__":
    main()