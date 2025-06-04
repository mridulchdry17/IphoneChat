from flask import Flask, request, jsonify, render_template
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=GROQ_API_KEY
)

def search_web(query: str) -> str:
    try:
        with DDGS() as ddgs:
            search_query = f"{query} iPhone"
            results = ddgs.text(search_query, max_results=3)
            output = ""
            for r in results:
                output += f"{r['title']}\n"
                output += f"Source: {r['href']}\n"
                output += f"Details: {r['body']}\n\n"
            return output or "No information found."
    except Exception as e:
        return f"Search error: {str(e)}"
    
tools = [
    Tool(
        name="iPhoneSearch",
        func=search_web,
        description="Search for specific iPhone information based on user query"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True
)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("query", "")
    if not user_input:
        return jsonify({"error": "Please ask a question about iPhones"}), 400
    
    try:
        prompt = f"""You are an iPhone information assistant. The user asks: {user_input}
        
        Provide a focused response that directly answers the user's question about any iPhone model or aspect (price, features, specs, comparison, etc).
        
        Guidelines:
        - Only include information that is specifically requested.
        - Always format the response in a clear, structured, markdown-style way.
        - Use bullet points, sub-bullets, or tables for clarity.
        - For prices, list each model/variant on a new line.
        - For features/specs, use bullet points for each feature/spec.
        - For comparisons, use a table or side-by-side bullet points.
        - Always include clickable source links at the end, if available.
        
        **Examples:**
        
        **Price Example:**
        - iPhone 16
            - 128GB: $799
            - 256GB: $899
            - 512GB: $1,099
        - iPhone 16 Pro
            - 128GB: $999
            - 256GB: $1,199
        
        **Features Example:**
        - iPhone 15 Pro Features:
            - A17 Pro chip
            - 48MP main camera
            - USB-C port
            - Titanium frame
        
        **Comparison Example:**
        | Feature         | iPhone 16         | iPhone 15 Pro      |
        |-----------------|------------------|--------------------|
        | Chipset         | Apple A18        | Apple A17 Pro      |
        | Battery         | 3561 mAh         | 3274 mAh           |
        | Max Storage     | 512GB            | 1024GB             |
        | Camera System   | Upgraded         | Pro Camera System  |
        | Starting Price  | $799             | $999               |
        
        Sources(for your reference):
        - [macrumors](https://www.macrumors.com/)
        - [apple](https://www.apple.com/)
        
        If the question is not about iPhones, politely redirect to iPhone-related topics.
        """
        
        response = agent.run(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
