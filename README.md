# 📰 News Bias Checker

A RAG-based AI tool that analyzes news articles from multiple sources on any topic and detects media bias using Google's Gemini AI.

## 🎯 What It Does

Give it any topic, and it will:
- Automatically fetch live news articles from multiple sources (via NewsAPI)
- Analyze each article's tone and bias level individually
- Generate a balanced comparison summary highlighting which source is most neutral vs. biased

## 🛠️ Tech Stack

- **Python**
- **Google Gemini API** (gemini-3.6-flash) — for bias analysis and summarization
- **NewsAPI** — for fetching live news articles
- **Streamlit** — for the web interface
- **RAG (Retrieval-Augmented Generation)** architecture

## 🚀 How It Works

1. **Retrieval**: Fetches relevant news articles for a given topic from NewsAPI
2. **Augmentation**: Combines articles into context for the AI
3. **Generation**: Gemini analyzes tone, bias level, and generates a balanced summary

## 📸 Demo

*(Screenshot yahan add karenge)*

## ⚙️ Setup & Installation

1. Clone this repository
```bash
git clone <your-repo-link>
cd news-bias-checker
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your own API keys (get them free from [Google AI Studio](https://aistudio.google.com/apikey) and [NewsAPI.org](https://newsapi.org))
GEMINI_API_KEY=your_own_gemini_api_key_here
NEWS_API_KEY=your_own_newsapi_key_here
4. Run the app
```bash
streamlit run app.py
```

## 💡 Example

Input topic: `Pakistan petrol price`

Output:
- Individual bias analysis for each source (Dawn, Geo, ARY, etc.)
- Overall neutral vs biased comparison
- Balanced combined summary

## 📌 Future Improvements

- Add sentiment scoring (numerical bias scale)
- Support for more languages
- Historical bias tracking over time

## 👤 Author

Built by Hafiza as a learning project to explore RAG systems and AI-powered media analysis.