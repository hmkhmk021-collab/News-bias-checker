import os
import requests
import streamlit as st
from google import genai
from dotenv import load_dotenv

# ===== Setup =====
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
client = genai.Client(api_key=api_key)


# ===== Function 1: Topic se automatically articles fetch karo =====
def fetch_articles_by_topic(topic, num_articles=3):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f'"{topic}"',
        "apiKey": news_api_key,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": num_articles
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "ok":
        return [], data.get("message", "Kuch masla hua")

    if len(data["articles"]) == 0:
        return [], "Koi article nahi mila is topic ke liye."

    fetched_articles = []
    for item in data["articles"]:
        content = f"{item['title']}\n\n{item['description'] or ''}\n\n{item['content'] or ''}"
        fetched_articles.append({
            "filename": item["source"]["name"],
            "content": content
        })

    return fetched_articles, None


# ===== Function 2: Individual bias analysis =====
def analyze_bias(article_text, source_name):
    prompt = f"""
Tum ek media analyst ho. Neeche diya gaya news article padho aur uska bias analysis do.

Article Source: {source_name}
Article Text: {article_text}

Ye batao:
1. Tone kya hai? (Neutral / Critical / Supportive)
2. Kis angle se story likhi gayi hai? (1-2 lines mein)
3. Bias Level: (Low / Medium / High)

Jawab short aur clear format mein do.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text


# ===== Function 3: Comparison summary =====
def compare_all_articles(articles, topic):
    combined_text = ""
    for article in articles:
        combined_text += f"\n\n--- Source: {article['filename']} ---\n{article['content']}"

    prompt = f"""
Tum ek media analyst ho. Neeche alag alag news sources ke articles diye gaye hain, 
sab "{topic}" topic pe hain.

{combined_text}

Ab in sabka COMPARISON karo:

1. Har source ka tone/angle ek line mein batao
2. Kaunsa source sabse NEUTRAL hai aur kyun?
3. Kaunsa source sabse zyada BIASED/ONE-SIDED hai aur kyun?
4. Ek 3-4 line ka overall summary do jo sab sources ko combine kare (balanced view)

Jawab clear headings ke sath do.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text


# ===== STREAMLIT UI =====
st.set_page_config(page_title="News Bias Checker", page_icon="📰", layout="wide")

# Custom styling
st.markdown("""
<style>
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #E63946;
        color: white;
    }
    .stExpander {
        border: 1px solid #333;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📰 News Bias Checker")
st.write("Koi bhi topic likho, alag alag news sources ka bias compare karo.")

topic = st.text_input("Topic likho:", placeholder="jaise: Pakistan budget, climate change")

if st.button("Check Karo 🔍"):
    if not topic:
        st.warning("Pehle koi topic likho!")
    else:
        with st.spinner(f"'{topic}' pe articles dhoonde ja rahe hain..."):
            articles, error = fetch_articles_by_topic(topic)

        if error:
            st.error(error)
        else:
            st.success(f"{len(articles)} articles mile!")

            # Sources dikhao
            st.subheader("📋 Sources")
            for article in articles:
                st.write(f"- {article['filename']}")

            # Individual analysis
            st.subheader("🔍 Individual Bias Analysis")
            for article in articles:
                with st.expander(f"📰 {article['filename']}"):
                    with st.spinner("Analyze ho raha hai..."):
                        analysis = analyze_bias(article['content'], article['filename'])
                    st.write(analysis)

            # Final comparison
            st.subheader("⚖️ Final Comparison Summary")
            with st.spinner("Comparison ban raha hai..."):
                final_summary = compare_all_articles(articles, topic)
            st.write(final_summary)