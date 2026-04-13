# Website Chatbot using Retrieval-Augmented Generation (RAG)

## Overview
This project implements a console-based chatbot that interacts with the content of a given website URL. It extracts relevant information from the website and generates responses using the OpenAI API.

The system follows a Retrieval-Augmented Generation (RAG) approach, where relevant content is retrieved from the website and passed as context to the language model.

---

## Objective
The objective of this project is to:
- Extract meaningful data from a website
- Process and structure the data
- Retrieve relevant information based on user queries
- Generate responses using the OpenAI API
- Enable interaction through a console interface

---

## Features
- Web scraping using requests and BeautifulSoup
- Data cleaning and preprocessing
- Text chunking for efficient processing
- Keyword-based retrieval mechanism
- OpenAI ChatGPT API integration
- Console-based chatbot interaction
- Basic error handling and input validation

---

## Project Workflow
1. User enters a website URL
2. Website content is fetched using HTTP requests
3. HTML is parsed and meaningful text is extracted
4. Extracted text is cleaned and processed
5. Text is divided into smaller chunks
6. User enters a query
7. Relevant chunk is retrieved using keyword matching
8. Context + query is sent to OpenAI API
9. Response is displayed in the console

---

## Implementation Details

### 1. Environment Setup
- API key is stored in a `.env` file
- Loaded using `python-dotenv`
- OpenAI client initialized using the API key

### 2. Web Scraping
- Uses `requests` to fetch webpage content
- Uses `BeautifulSoup` to parse HTML
- Removes unwanted elements (scripts, styles, etc.)
- Extracts meaningful text from paragraphs and headings

### 3. Data Cleaning
- Removes extra whitespace
- Normalizes text for better processing

### 4. Text Chunking
- Splits text into chunks (default: 500 words)
- Helps manage token limits
- Improves retrieval efficiency

### 5. Retrieval Mechanism
- Removes punctuation using regex
- Removes stopwords from query
- Matches query keywords with chunks
- Selects the most relevant chunk

### 6. OpenAI API Integration
- Uses `gpt-4o-mini` model
- Context-based prompting
- Limits response tokens for cost control

### 7. Chatbot Interface
- Runs in a loop in the console
- Accepts user queries
- Displays generated responses
- Exits when user types "exit"

---

## How to Run

1. Install dependencies  
   `pip install -r requirements.txt`

2. Create a `.env` file in the project root  
   `OPENAI_API_KEY=your_api_key_here`

3. Run the script  
   `python chatbot.py`

4. Usage  
   - Enter a valid website URL  
   - Ask questions related to the website content  
   - Type `exit` to quit the chatbot  