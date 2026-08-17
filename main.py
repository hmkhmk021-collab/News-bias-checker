import os
import requests
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
        "q": f'"{topic}"',  # Exact phrase match ke liye quotes
        "apiKey": news_api_key,
        "language": "en",
        "sortBy": "relevancy",  # relevancy pe sort karo, sirf latest nahi
        "pageSize": num_articles
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "ok":
        print("Error:", data.get("message", "Kuch masla hua"))
        return []

    if len(data["articles"]) == 0:
        print("⚠️ Koi article nahi mila is exact topic ke liye. Thoda different keyword try karo.")
        return []

    fetched_articles = []
    print("📋 Ye articles mile (titles):\n")
    for item in data["articles"]:
        print(f"   • {item['title']} ({item['source']['name']})")
        content = f"{item['title']}\n\n{item['description'] or ''}\n\n{item['content'] or ''}"
        fetched_articles.append({
            "filename": item["source"]["name"],
            "content": content
        })
    print()

    return fetched_articles


# ===== Function 2: Har article ka individual bias analyze karo =====
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


# ===== Function 3: Sab articles ka comparison summary banao =====
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


# ===== MAIN PROGRAM =====
def main():
    print("=" * 50)
    print("📰 NEWS BIAS CHECKER")
    print("=" * 50)

    topic = input("\nKis topic pe news check karni hai? ")

    print(f"\n🔍 '{topic}' pe articles dhoonde ja rahe hain...\n")
    articles = fetch_articles_by_topic(topic)

    if not articles:
        print("Koi article nahi mila. Doosra topic try karo.")
        return

    print(f"✅ {len(articles)} articles mile:\n")
    for article in articles:
        print(f"- {article['filename']}")

    print("\n\n===== INDIVIDUAL BIAS ANALYSIS =====\n")
    for article in articles:
        print(f"📰 Source: {article['filename']}")
        analysis = analyze_bias(article['content'], article['filename'])
        print(analysis)
        print("-" * 50)

    print("\n\n===== FINAL COMPARISON SUMMARY =====\n")
    final_summary = compare_all_articles(articles, topic)
    print(final_summary)


if __name__ == "__main__":
    main()