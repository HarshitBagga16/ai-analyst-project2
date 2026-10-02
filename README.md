# 🤖 AI Data Analyst

Live Url : https://ai-analyst-project2-dytfspvkaexr3biui69nza.streamlit.app/
An LLM-powered data analysis application that combines **deterministic Python/Pandas analysis with Generative AI** to answer natural-language questions about CSV datasets.

The core principle of this project is:

> **Python calculates the facts. The LLM explains the facts.**

Instead of blindly sending an entire CSV file to an LLM, the application first processes and analyzes the dataset using Python and Pandas, then provides the calculated results to the LLM for natural-language interpretation.

---

## 🚀 Project Overview

### Traditional approach

```text
CSV
 ↓
Human manually analyzes
 ↓
Charts / statistics
 ↓
Human interpretation
```

### This project

```text
CSV
 ↓
Pandas
 ↓
Data processing & statistical analysis
 ↓
Structured analytical results
 ↓
LLM
 ↓
Natural-language explanation
```

Example:

```text
User:
Which region generated the most revenue?

Python:
West → ₹45,000
East → ₹35,000
North → ₹25,000
South → ₹18,000

LLM:
The West region generated the highest revenue at ₹45,000,
followed by East at ₹35,000.
```

The LLM does **not** calculate the revenue itself.

---

# 🎯 Why I Built This

A common mistake when building LLM data-analysis applications is:

```text
CSV → LLM → Answer
```

This can lead to:

* unnecessary token usage
* higher cost
* slower processing
* context-window limitations
* numerical errors
* hallucinated statistics
* unnecessary exposure of raw data

This project uses a more reliable architecture:

```text
CSV
 ↓
Python/Pandas
 ↓
Deterministic calculations
 ↓
Relevant facts
 ↓
LLM
 ↓
Explanation
```

This separates **computation** from **language generation**.

---

# 🧠 Key Concept Learned

## Deterministic Python + Probabilistic LLM

### Python is responsible for:

* Data loading
* Data cleaning
* Calculations
* Aggregations
* Statistics
* Grouping
* Revenue calculations
* Missing-value analysis
* Outlier analysis
* Trend calculations

### LLM is responsible for:

* Understanding natural-language questions
* Interpreting calculated results
* Summarizing findings
* Explaining insights
* Generating human-readable responses

This creates a useful division of responsibilities:

```text
Python → "What are the facts?"

LLM → "How should those facts be explained?"
```

---

# 🏗️ Architecture

```text
                  ┌──────────────┐
                  │   CSV File   │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │    Pandas    │
                  │ Load + Clean │
                  └──────┬───────┘
                         ↓
              ┌─────────────────────┐
              │ Deterministic       │
              │ Analysis             │
              │                     │
              │ • Statistics        │
              │ • Aggregations      │
              │ • IQR               │
              │ • Revenue           │
              │ • Trends            │
              └──────────┬──────────┘
                         ↓
                Structured Results
                         ↓
              ┌─────────────────────┐
              │        LLM          │
              │      via Groq       │
              └──────────┬──────────┘
                         ↓
              Natural-language Answer
                         ↓
                        User
```

---

# 📁 Project Structure

```text
ai-data-analyst/
│
├── data/
│   └── sales.csv
│
├── app.py
├── analyzer.py
├── llm.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

| Technology                   | Purpose                         |
| ---------------------------- | ------------------------------- |
| Python                       | Application logic               |
| Pandas                       | Data processing and analysis    |
| NumPy                        | Numerical operations            |
| Groq API                     | LLM inference                   |
| Llama / supported Groq model | Natural-language generation     |
| OpenAI Python SDK            | API client                      |
| python-dotenv                | Environment variable management |
| Git/GitHub                   | Version control                 |

---

# 📊 Dataset

The initial dataset contains sales information such as:

```text
date
region
product
quantity
unit_price
```

A derived `revenue` column is calculated using:

```python
df["revenue"] = df["quantity"] * df["unit_price"]
```

This demonstrates how raw business data can be transformed into useful analytical features before involving an LLM.

---

# 🔬 Data Analysis Layer

The `analyzer.py` module performs deterministic analysis.

### Dataset exploration

```python
df.shape
df.columns
df.dtypes
```

### Missing-value analysis

```python
df.isnull().sum()
```

### Descriptive statistics

```python
df.describe()
```

### Numeric feature selection

```python
df.select_dtypes(include="number")
```

### IQR calculation

```python
Q1 = numeric_df.quantile(0.25)
Q3 = numeric_df.quantile(0.75)

IQR = Q3 - Q1
```

### Business analysis

```python
df.groupby("region")["revenue"].sum()
```

```python
df.groupby("product")["revenue"].sum()
```

```python
df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()
```

These calculations produce structured facts that can be provided to the LLM.

---

# 🤖 LLM Layer

The LLM receives:

```text
1. Instructions
2. Calculated analytical results
3. User's question
```

For example:

```text
Calculated results:

Total revenue: ₹123,000

Revenue by region:

West: ₹45,000
East: ₹35,000
North: ₹25,000
South: ₹18,000

User question:

Which region generated the most revenue?
```

The LLM then converts those facts into a natural-language response.

---

# 🔌 Groq API

The project uses Groq's OpenAI-compatible API.

The client is initialized using:

```python
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)
```

This allows the standard OpenAI Python SDK interface to communicate with Groq.

---

# 💬 Chat Completions

The LLM request uses the Chat Completions structure:

```python
response = client.chat.completions.create(
    model="YOUR_GROQ_MODEL",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
```

## Understanding `messages`

Messages contain:

```python
{
    "role": "user",
    "content": "..."
}
```

Common roles include:

### `system`

Defines the model's behavior.

```python
{
    "role": "system",
    "content": "You are a data analyst."
}
```

### `user`

Contains the user's request.

```python
{
    "role": "user",
    "content": "Which region has the highest revenue?"
}
```

### `assistant`

Represents a previous AI response and is useful when maintaining conversation history.

---

# 📦 Understanding the API Response

The response from Chat Completions is structured roughly like:

```text
response
 └── choices
      └── [0]
           └── message
                └── content
```

Therefore:

```python
response.choices[0].message.content
```

means:

```text
response
 ↓
choices
 ↓
first choice [0]
 ↓
message
 ↓
content
 ↓
actual AI-generated text
```

And:

```python
return response.choices[0].message.content
```

returns that text to the rest of the Python application.

---

# 🔐 API Key Management

The API key is not hardcoded.

Instead:

### `.env`

```text
GROQ_API_KEY=your_api_key
```

### Python

```python
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
```

`.env` should be added to `.gitignore`:

```text
.env
venv/
__pycache__/
```

This prevents accidentally exposing API credentials in GitHub.

---

# 🔄 Current Application Flow

The application currently works as:

```text
1. Load CSV
        ↓
2. Read data using Pandas
        ↓
3. Create derived columns
        ↓
4. Calculate statistics
        ↓
5. Calculate business metrics
        ↓
6. Store results in Python structures
        ↓
7. Ask user for a question
        ↓
8. Combine question + calculated facts
        ↓
9. Send prompt to Groq
        ↓
10. Receive LLM response
        ↓
11. Return/display answer
```

---

# 🧩 Why We Return Instead of Print

Instead of:

```python
print(response.choices[0].message.content)
```

the application uses:

```python
return response.choices[0].message.content
```

### `print()`

Displays something directly in the terminal.

### `return`

Sends the result back to the calling function.

This makes the application easier to extend later into:

```text
CLI
 ↓
Web API
 ↓
Streamlit UI
 ↓
Chat application
```

---

# 💡 Important GenAI Concepts Learned

Through this project I learned:

### LLM fundamentals

* LLM API calls
* Models
* Prompts
* System messages
* User messages
* API responses
* Response parsing
* Tokens and context concepts

### LLM application development

* API key management
* Environment variables
* `.env`
* OpenAI-compatible APIs
* Groq inference
* Prompt construction
* Structured analytical context
* Separating computation from generation

### Data + AI

* Pandas preprocessing
* Statistical analysis
* GroupBy analysis
* Derived metrics
* IQR/outlier analysis
* Passing structured data to an LLM
* Grounding LLM responses in calculated facts

---

# 🧠 Key Engineering Lesson

The most important lesson from this project is:

```text
Don't ask the LLM to do everything.
```

Instead:

```text
Use traditional programming
for deterministic tasks.

Use the LLM
for language understanding and generation.
```

For example:

### Bad architecture

```text
CSV
 ↓
LLM
 ↓
"Calculate everything"
```

### Better architecture

```text
CSV
 ↓
Python/Pandas
 ↓
Calculate exact numbers
 ↓
LLM
 ↓
Explain those numbers
```

This makes the system easier to reason about and provides a cleaner separation of responsibilities.

---

# 🔮 Future Improvements

The current version is intentionally simple. Planned improvements:

## Version 2 — Continuous Questions

Instead of:

```text
Question
 ↓
Answer
 ↓
Program ends
```

build:

```text
Question
 ↓
Answer
 ↓
Question
 ↓
Answer
 ↓
Question
 ↓
Answer
```

---

## Version 3 — Conversation History

Maintain:

```python
messages = [
    {"role": "system", ...},
    {"role": "user", ...},
    {"role": "assistant", ...},
    {"role": "user", ...},
]
```

This allows follow-up questions such as:

```text
User:
Which region has the highest revenue?

AI:
West.

User:
What product performs best there?

AI:
Laptop.

User:
How much higher is it than East?
```

---

## Version 4 — Automatic Analysis Selection

Instead of calculating every possible metric beforehand:

```text
User:
Why did revenue fall in March?

             ↓

LLM identifies required analysis

             ↓

Python performs:
• Monthly revenue analysis
• Product comparison
• Region comparison
• Quantity analysis

             ↓

Results → LLM
             ↓
Final explanation
```

This moves the project closer to an **AI-powered analytical agent**.

---

## Version 5 — Visualization

Generate charts using Python:

```text
Revenue by Region
Monthly Revenue
Product Performance
Sales Trends
```

Then allow the LLM to explain the visualized findings.

---

## Version 6 — Web Interface

Build a UI where the user can:

```text
Upload CSV
    ↓
Ask questions
    ↓
View answers
    ↓
View charts
```

Potential technology:

```text
Streamlit
```

---

## Version 7 — Production Architecture

Final architecture:

```text
                    User
                     ↓
              Web Application
                     ↓
               LLM / Router
                     ↓
          ┌──────────┴──────────┐
          ↓                     ↓
    Python Analysis         Conversation
       Tools                   Memory
          ↓                     ↓
          └──────────┬──────────┘
                     ↓
               LLM Reasoning
                     ↓
              Final Response
                     ↓
              Charts + Insights
```

---

# 📌 Recruiter-Facing Project Description

**AI Data Analyst — Python, Pandas, Groq, LLM**

> Built an LLM-powered data analysis application that allows users to query CSV datasets using natural language. Implemented a deterministic Python/Pandas analytics layer for data preprocessing, statistical analysis, aggregations, revenue calculations, and trend analysis, then supplied structured analytical results to an LLM through the Groq API for grounded natural-language explanations. Used environment-based API key management and an OpenAI-compatible SDK architecture to separate deterministic computation from probabilistic language generation.

### Key skills demonstrated

```text
Python
Pandas
Data Analysis
Statistics
LLM APIs
Prompt Engineering
Groq
OpenAI-compatible APIs
Environment Variables
API Integration
GenAI Application Development
```

---

# ⚡ Fast Revision

If I need to remember this project quickly:

```text
PROJECT:
AI Data Analyst

PROBLEM:
Allow users to ask natural-language questions
about CSV data.

CORE IDEA:
Python calculates.
LLM explains.

FLOW:
CSV
 ↓
Pandas
 ↓
Statistics + Business Analysis
 ↓
Structured Results
 ↓
Prompt
 ↓
Groq LLM
 ↓
Natural-language Answer

PYTHON:
• read_csv()
• groupby()
• describe()
• isnull()
• IQR
• derived columns
• aggregations

LLM:
• prompt
• messages
• system/user roles
• API call
• response parsing

API:
client.chat.completions.create()

RESPONSE:
response
 → choices
 → [0]
 → message
 → content

SECURITY:
.env
GROQ_API_KEY
.gitignore

KEY LESSON:
Deterministic computation should be handled
by code; LLMs should primarily handle
language understanding and generation.

NEXT:
Conversation history
→ dynamic analysis
→ tools
→ charts
→ Streamlit
→ AI analytical agent
```

---

# ⭐ What This Project Demonstrates

This isn't just a "CSV + ChatGPT" project.

The important engineering concept is the separation:

```text
        DETERMINISTIC               PROBABILISTIC

           Python                      LLM
             │                          │
             │                          │
       Exact calculations          Language
       Statistics                  Understanding
       Aggregations                Explanation
       Data processing             Summarization
             │                          │
             └──────────┬───────────────┘
                        ↓
                 AI Data Analyst
```

That architecture is the foundation we'll build on when turning this into a **conversational AI data analyst and eventually an agent that can decide which Python analysis tools to call.**
