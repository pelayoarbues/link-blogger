# Link Blogger

Link Blogger is a Python project designed to streamline the process of generating concise summaries of recent readings and organizing them into a Markdown blog post. The tool automates:
- Summarizing content using OpenAI's GPT API.
- Classifying articles into predefined topics.
- Generating an engaging introduction.
- Saving the results as a Markdown file.

## About The Project

The purpose of Link Blogger is to help users efficiently organize and document their reading activities. It has been inspired by [Simon Willison call to share link blogs](https://simonwillison.net/2024/Dec/22/link-blog/).

 By analyzing recently modified files, the tool:
1. Extracts metadata and highlights from articles or notes. Metadata includes Title and URL from Readwise's Reader highlights. 
2. Summarizes content using OpenAI's advanced natural language processing models.
3. Classifies articles into user-defined topics.
4. Generates a formatted blog post in Markdown, grouped by topics and complete with an engaging introduction.

This is ideal for bloggers, researchers, or professionals who want to share insights from their recent readings with minimal manual effort.

---

## Getting Started

To get started with Link Blogger, follow the steps below.

### Prerequisites

- **Python 3.9+**: Ensure Python is installed on your system.
- **Virtual Environment Management**: Use `uv` to isolate dependencies.
- **OpenAI API Key**: You need an OpenAI account and an API key to access GPT models. Sign up [here](https://platform.openai.com/signup/).

### Environment Variables

Create a `.conf/openai.conf` file in the project directory and add your OpenAI API key:
```plaintext
OPENAI_API_KEY=your_openai_api_key
```

---

## Installation

Follow these steps to set up the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pelayoarbues/link_blogger.git
   cd link_blogger
   ```

2. **Install uv if necessary**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Use virtual environment**:
   ```bash
   uv sync
   source .venv/bin/activate   # On macOS/Linux
   ```

4. **Configure OpenAI API Key**:
   - Add the `.conf/openai.conf` file as described above.

5. **Create list of topics**:
   - Add the `.conf/topics.conf` file for topic classification:
    ```plaintext
    AI
    Technology
    Politics
    Management
    Economics
    ```

---

## Usage

The main script is `generate_link_post.py`, which processes your recent reading files and generates a Markdown blog post.

### Command-Line Arguments

Run the script using:
```bash
python generate_link_post.py <directory> [--days DAYS] [--output_dir OUTPUT_DIR] [--exclude EXCLUDE_PATTERN]
```

#### Arguments:
- `<directory>`: The directory containing your reading files.
- `--days`: Number of days to review for recently modified files (default: `7`).
- `--output_dir`: Directory to save the Markdown file (default: `./summaries`).
- `--exclude`: Patterns of files to exclude, e.g., `--exclude "^000" ".pdf$"`.

### Example Usage

1. **Summarize readings from the last 7 days**:
   ```bash
   python generate_link_post.py /path/to/files
   ```

2. **Summarize readings from the last 14 days, excluding `.pdf` files**:
   ```bash
   python generate_link_post.py /path/to/files --days 14 --exclude ".pdf$"
   ```

3. **Save output to a custom directory**:
   ```bash
   python generate_link_post.py /path/to/files --output_dir ./custom_output
   ```

---

## Output

The script generates a Markdown file (e.g., `wrapped_up_readings_YYYY-MM-DD.md`) in the specified `output_dir` or the default `./summaries` directory. The file includes:
- A frontmatter block for blog metadata.
- A dynamically generated introduction summarizing the topics.
- Summaries grouped by topics.

Example output:
```markdown
---
title: Wrapped-up readings 2025-01-16
date: 2025-01-16
tags:
  - link-blog
---

The past few days I have been reading mainly about AI and Business models.

## AI

- [A Dive Into Vision-Language Models](https://huggingface.co/blog/vision_language_pretraining): This article explores how multi-modal learning leverages human-like capabilities to link and process information from different modalities. Vision-language models are highlighted for their impressive performance in tasks like image captioning, text-guided image generation, and zero-shot classification.

## Business Models

- [Stackable Business Models in the Age of AI](https://www.nfx.com/post/stackable-business-models): This article discusses strategies for AI startups to build sustainable and scalable business models by stacking multiple revenue streams over time.
```


---

Let me know if you'd like any further refinements or if there's something specific to include!
