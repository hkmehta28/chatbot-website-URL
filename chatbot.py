import os
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)


def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup(["script", "style", "noscript", "header", "footer", "aside"]):
        tag.extract()

    text_parts = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "li", "span"]):
        content = tag.get_text(separator=" ", strip=True)
        if content:
            text_parts.append(content)

    text = " ".join(text_parts).strip()
    if len(text) < 120:
        text = soup.get_text(separator=" ")

    return text


def fetch_website_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        content_div = soup.find('div', {'id': 'mw-content-text'})

        if not content_div:
            return ""

        paragraphs = content_div.find_all('p')

        text = ' '.join([p.get_text() for p in paragraphs])

        return text

    except Exception as e:
        print(f"Error fetching website: {e}")
        return ""


def clean_text(text):
    """
    Clean raw text by removing extra whitespace.
    """
    return ' '.join(text.split())


def chunk_text(text, chunk_size=500):
    """
    Split text into chunks for retrieval.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


import re

def find_relevant_chunks(query, chunks):
    """
    Improved retrieval with punctuation removal + keyword scoring
    """

    # Remove punctuation
    query = re.sub(r'[^\w\s]', '', query.lower())

    stopwords = {"what", "is", "a", "the", "of", "in", "on", "and", "to", "for"}

    query_words = [
        word for word in query.split()
        if word not in stopwords
    ]

    best_chunk = ""
    max_score = 0

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for word in query_words if word in chunk_lower)

        if score > max_score:
            max_score = score
            best_chunk = chunk

    return best_chunk if best_chunk else chunks[0]


def ask_chatbot(query, context):
    """
    Generate response using OpenAI API.
    """
    try:
        prompt = f"""
You are an AI assistant that answers questions ONLY based on the given context.

If the answer is not found in the context, say:
"I don't have enough information from the website."

Context:
{context}

Question:
{query}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200 
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating response: {e}"



def chatbot_loop(chunks):
    """
    Interactive chatbot in console.
    """
    print("\nChatbot is ready! Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            print("Please enter a valid question.")
            continue

        context = find_relevant_chunks(query, chunks)
        response = ask_chatbot(query, context)

        print("\nBot:", response)
        print("-" * 60)



def main():
    """
    Main pipeline controller.
    """
    print("=" * 60)
    print("WEBSITE CHATBOT (RAG SYSTEM)")
    print("=" * 60)

    # Step 1: Get URL
    url = input("Enter website URL: ").strip()

    if not url.startswith("http"):
        print("Invalid URL. Please include http/https.")
        return

    # Step 2: Fetch content
    print("\nFetching website content...")
    raw_text = fetch_website_content(url)

    if not raw_text:
        print("Failed to fetch content. Exiting...")
        return

    print("Content fetched successfully!")

    # Step 3: Clean text
    print("\nCleaning text...")
    cleaned_text = clean_text(raw_text)

    if not cleaned_text:
        print("No usable content found.")
        return

    # Step 4: Chunking
    print("\nCreating chunks...")
    chunks = chunk_text(cleaned_text)

    if not chunks:
        print("Chunking failed.")
        return

    print(f"{len(chunks)} chunks created.")

    # Step 5: Start chatbot
    print("\nStarting chatbot...\n")
    chatbot_loop(chunks)


if __name__ == "__main__":
    main()