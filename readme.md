# iPhone Information Assistant Chatbot
A Flask-based web chatbot that answers all questions related to iPhones, providing up-to-date information about prices, features, specs, comparisons, and more. Powered by Groq's LLM and DuckDuckGo search for latest data.

## Features
Ask anything about iPhone models, prices, specs, and comparisons

Real-time web search integration for fresh and relevant answers

Clean, responsive web UI with Markdown rendering

Uses LangChain agents for structured interaction with LLM

Easily extendable to other product domains

## Tech Stack
* Backend: Flask, LangChain, ChatGroq (Groq LLM)

* Search: DuckDuckGo Search API (duckduckgo_search)

* Frontend: HTML/CSS/JS with Markdown rendering (marked.js)

* Environment management: python-dotenv for secrets

* Deployment: Local development with Flask (can be deployed on any WSGI-compatible host)

## Prerequisites
* Python 3.8+

* Git

* Groq API Key (sign up at Groq's platform to get your API key)

## Installation
Clone the repository:
```
git clone https://github.com/mridulchdry17/IphoneChat.git
cd IphoneChat
```
Create and activate a virtual environment:
```
python -m venv iphoneinfo
# Windows
iphoneinfo\Scripts\activate
# macOS/Linux
source iphoneinfo/bin/activate
```
Install dependencies:

```
pip install -r requirements.txt
```
Create a .env file in the project root with your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```
Running the App
```
python app.py
```
Open your browser and navigate to http://127.0.0.1:5000/ to chat with the iPhone assistant.