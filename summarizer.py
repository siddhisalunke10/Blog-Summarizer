"""
Blog Summarizer using Gemini API
Author: Siddhi Salunke
Description: Fetches a blog from a URL, extracts clean text,
             summarizes it using Gemini API, and validates the output.
"""

import requests
from bs4 import BeautifulSoup
from google import genai
from dotenv import load_dotenv
import os


load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def fetch_blog(url):
    """Fetches and cleans blog content from a given URL"""
    print(f"Fetching blog from: {url}")
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch blog. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
   
    for tag in soup(["nav", "footer", "header", "script", "style", "aside"]):
        tag.decompose()
    
    
    text = soup.get_text(separator=" ", strip=True)
    return text


def summarize(text):
    """Sends blog text to Gemini API and returns a summary"""
    print("Generating summary using Gemini...")

    prompt = f"""Summarize the following blog article in no more than 300 words and 20 sentences.

Write it as a clean, informative paragraph-style summary (no bullet points).
Focus on the key points, technologies mentioned, and main takeaways.

Important: if the blog includes specific concrete details such as install
commands, CLI commands, version numbers, percentages, or statistics, include
those exact details in the summary rather than describing them vaguely.

Blog content:
{text}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def validate_summary(summary):
    """Checks if summary is within 300 words and 20 sentences"""
    words = len(summary.split())
    sentences = len([s for s in summary.split(".") if s.strip()])
    
    print(f"\nValidation Results:")
    print(f"Word count: {words}/300")
    print(f"Sentence count: {sentences}/20")
    
    if words > 300:
        print("Warning: Summary exceeds 300 words")
    if sentences > 20:
        print("Warning: Summary exceeds 20 sentences")
    
    return words, sentences


def save_summary(summary):
    """Saves the summary to a text file"""
    with open("summary.txt", "w") as f:
        f.write(summary)
    print("\nSummary saved to summary.txt")


def main():
    url = "https://www.langchain.com/blog/langsmith-cli-skills"
    
    # Step 1: Fetch blog
    blog_text = fetch_blog(url)
    
    # Step 2: Summarize
    summary = summarize(blog_text)
    
    # Step 3: Validate
    validate_summary(summary)
    
    # Step 4: Print summary
    print("\n--- GENERATED SUMMARY ---\n")
    print(summary)
    
    # Step 5: Save summary
    save_summary(summary)


if __name__ == "__main__":
    main()