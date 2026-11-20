# 🤖 AI Agent with Tool Calling

An AI-powered command-line assistant built with **Python** and the **OpenAI API**. The agent can understand user queries, decide when external tools are needed, execute them, and generate intelligent responses using tool calling.

## ✨ Features

- 🧠 Conversational AI using OpenAI Chat Completions
- 🔧 Function Calling (Tool Calling)
- ⏰ Get current date and time
- 🌤️ Fetch live weather for any city
- 💬 Multi-turn conversation support
- 🔑 Environment variable configuration using `.env`
- 🏗️ Modular project structure

---

## 🛠️ Tech Stack

- Python 3.x
- OpenAI Python SDK
- Requests
- python-dotenv
- wttr.in Weather API

---

## 📂 Project Structure

```
AI_Agent/
│── simple_ai_assistant.py     # Main application
│── tools.py                   # Tool definitions & implementations
│── .gitignore
│── README.md
│── requirements.txt
│── .env                       # Not tracked
```

---

## ⚙️ How It Works

1. User enters a prompt.
2. The prompt is sent to the LLM.
3. The LLM determines whether a tool is required.
4. If needed, it returns a tool call.
5. Python executes the corresponding function.
6. The tool result is sent back to the LLM.
7. The LLM generates the final response.

---

## 🔄 Workflow

```text
          User
            │
            ▼
     Python Application
            │
            ▼
      OpenAI Chat Model
            │
      Tool Required?
        ┌────┴────┐
        │         │
       No        Yes
        │         │
        ▼         ▼
   Final Reply   Execute Tool
                    │
                    ▼
              Return Result
                    │
                    ▼
          Final AI Response
```

---

## 🔧 Available Tools

### 🕒 Current Time

Returns the current system date and time.

Example:

```
User: What time is it?
```

---

### 🌤️ Weather

Returns the live weather of a given city using the free wttr.in API.

Example:

```
User: What's the weather in Jaipur?
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/AnantAgarwal2006/AI_Agent.git
```

Move into the project

```bash
cd AI_Agent
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
BASE_URL=your_openai_base_url
API_KEY=your_api_key
MODEL=your_model_name
```

Example:

```env
BASE_URL=https://api.openai.com/v1
API_KEY=sk-xxxxxxxxxxxxxxxx
MODEL=gpt-4.1-mini
```

---

## ▶️ Run the Project

```bash
python simple_ai_assistant.py
```

---

## 💬 Example Conversation

```
User: What time is it?

Assistant:
The current time is 2026-11-20 13:45:12
```

---

```
User: What's the weather in Delhi?

Assistant:
Delhi: 🌤️ +29°C
```

---

## 📦 Dependencies

```
openai
python-dotenv
requests
```

Generate automatically:

```bash
pip freeze > requirements.txt
```

---

## 📚 Concepts Demonstrated

- Large Language Models (LLMs)
- OpenAI Function Calling
- Tool Calling
- Environment Variables
- REST API Integration
- Python Modules
- JSON Parsing
- Multi-turn Conversations

---

## 🚧 Future Improvements

- Conversation Memory
- Multiple Tool Support
- Calculator Tool
- File Reader Tool
- Web Search
- RAG Integration
- Voice Assistant
- GUI with Streamlit
- FastAPI Backend
- Docker Deployment

---

## 👨‍💻 Author

**Anant Agarwal**

- GitHub: https://github.com/AnantAgarwal2006

---

⭐ If you found this project useful, consider giving it a star!
