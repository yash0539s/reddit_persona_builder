# Main script for building Reddit personas

import praw
import os
import sys
import re
import torch
from transformers import pipeline
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

# Initialize Reddit API using credentials from .env
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Initialize HuggingFace text generation pipeline (using GPT-2)
generator = pipeline(
    "text-generation",
    model="gpt2",
    device=0 if torch.cuda.is_available() else -1  # Use GPU if available
)

def extract_username(url_or_username):
    """
    Extracts the Reddit username from a URL or direct input.
    """
    match = re.search(r'reddit\.com/user/([^/]+)/?', url_or_username)
    return match.group(1) if match else url_or_username.strip("/")

def scrape_user_data(username, limit=30):
    """
    Scrapes the latest Reddit posts and comments for a given username.
    """
    redditor = reddit.redditor(username)
    posts, comments = [], []

    print(f"[+] Scraping u/{username}'s posts...")
    for post in tqdm(redditor.submissions.new(limit=limit)):
        posts.append({
            "title": post.title,
            "selftext": post.selftext
        })

    print(f"[+] Scraping u/{username}'s comments...")
    for comment in tqdm(redditor.comments.new(limit=limit)):
        comments.append({
            "body": comment.body
        })

    return posts, comments

def build_prompt(posts, comments):
    """
    Constructs a prompt for the LLM using top posts and comments.
    """
    prompt = "Based on the following Reddit posts and comments, generate a detailed user persona:\n\n"
    
    for post in posts[:10]:
        prompt += f"[Post] {post['title']}: {post['selftext']}\n"
    
    for comment in comments[:10]:
        prompt += f"[Comment] {comment['body']}\n"
    
    prompt += "\nUser Persona:\n"
    return prompt

def generate_persona(prompt):
    """
    Generates a user persona using the GPT-2 model.
    """
    print("\n[+] Generating persona using GPT-2...")
    result = generator(prompt, max_length=700, do_sample=True, temperature=0.7)
    return result[0]['generated_text']

def cite_sources(persona, posts, comments):
    """
    Adds citation lines for each inferred persona trait.
    """
    citations = "\n\n[Citations]\n"
    for trait in ['interest', 'personality', 'location', 'profession']:
        found = False

        for source in posts + comments:
            text = source.get('title') or source.get('selftext') or source.get('body')
            if trait in persona.lower() and trait in text.lower():
                citations += f"- {trait.title()} from: \"{text[:100].strip()}...\"\n"
                found = True
                break

        if not found:
            citations += f"- {trait.title()}: Not explicitly found, inferred by model.\n"
    
    return citations

def save_output(username, content):
    """
    Saves the final persona + citations into the personas/ directory.
    """
    os.makedirs("personas", exist_ok=True)
    path = f"personas/{username}_persona.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"\n Persona saved to: {path}")

def main():
    """
    Main execution function. Gets input, scrapes data, builds prompt,
    generates persona, cites sources, and saves output.
    """
    if len(sys.argv) < 2:
        print("Usage: python reddit_persona_builder.py <reddit_profile_url>")
        return

    url = sys.argv[1]
    username = extract_username(url)

    posts, comments = scrape_user_data(username)

    if not posts and not comments:
        print("[-] No posts/comments found.")
        return

    prompt = build_prompt(posts, comments)
    persona = generate_persona(prompt)
    citations = cite_sources(persona, posts, comments)

    full_output = persona + citations
    save_output(username, full_output)

if __name__ == "__main__":
    main()
