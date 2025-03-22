import requests
import pandas as pd
from bs4 import BeautifulSoup
import spacy
import nltk
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.sentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO, StringIO


# Download necessary NLTK resources lazily
def download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)


# Load spaCy model for Named Entity Recognition (NER)
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")


# Initialize sentiment analyzer
def get_sentiment_analyzer():
    download_nltk_resources()
    return SentimentIntensityAnalyzer()


def get_yahoo_finance_news(company_symbol):
    url = f"https://finance.yahoo.com/quote/{company_symbol}/latest-news/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("section", {"data-testid": "storyitem", "role": "article"}, limit=10)

    news_data = []
    for article in articles:
        title_tag = article.find("h3")
        link_tag = article.find("a")

        if title_tag and link_tag:
            title = " ".join(title_tag.text.strip().split())
            link = "https://finance.yahoo.com" + link_tag["href"] if link_tag["href"].startswith("/") else link_tag["href"]
            news_data.append({"Title": title, "Link": link})

    return news_data


def get_article_metadata(article_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(article_url, headers=headers)

    if response.status_code != 200:
        return "No author", "No date", "No summary"

    soup = BeautifulSoup(response.text, "html.parser")
    author_tag = soup.find("div", class_="byline-attr-author yf-1k5w6kz")
    date_tag = soup.find("div", class_="byline-attr-time-style")
    summary_tag = soup.find("div", class_="atoms-wrapper")

    author = author_tag.text.strip() if author_tag else "No author"
    date = date_tag.text.strip() if date_tag else "No date"
    summary = " ".join([p.text.strip() for p in summary_tag.find_all("p")]) if summary_tag else "No summary"
    summary = " ".join(summary.split())

    return author, date, summary


def summarize_text(text, max_sentences=7):
    text = " ".join(text.split())
    sentences = text.split('.')
    if len(sentences) <= max_sentences:
        return text
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, max_sentences)
    summary = " ".join([str(sentence) for sentence in summary_sentences])
    return summary


def extract_topics(text, nlp):
    doc = nlp(text)
    topics = {ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT", "EVENT"]}
    return list(topics)


def process_news_data(company_symbol, nlp):
    news_articles = get_yahoo_finance_news(company_symbol)

    if not news_articles:
        return None

    enriched_data = []
    for i, article in enumerate(news_articles):
        author, date, summary = get_article_metadata(article["Link"])
        enriched_data.append({
            "Title": article["Title"],
            "Author": author,
            "Date": date,
            "Content": summary,
            "Link": article["Link"]
        })

    df = pd.DataFrame(enriched_data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer


def analyze_news_data(csv_buffer, company_symbol, nlp, sia):
    df = pd.read_csv(csv_buffer)

    articles_data = []
    positive_count, negative_count, neutral_count = 0, 0, 0
    all_topics = []
    sentiment_mapping = {}
    all_summaries = []
    coverage_differences = []

    article_summaries = []
    for i, (_, row) in enumerate(df.iterrows()):
        title, content = row['Title'], row['Content']
        if content == "No summary":
            continue

        summary = summarize_text(content)
        all_summaries.append(summary)

        sentiment_score = sia.polarity_scores(summary)['compound']
        sentiment = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"

        if sentiment == "Positive":
            positive_count += 1
        elif sentiment == "Negative":
            negative_count += 1
        else:
            neutral_count += 1

        topics = extract_topics(content, nlp)
        all_topics.append((title, topics, sentiment))
        article_summaries.append((title, summary, sentiment))

        for topic in topics:
            if topic not in sentiment_mapping:
                sentiment_mapping[topic] = []
            sentiment_mapping[topic].append(sentiment)

        articles_data.append({"Title": title, "Summary": summary, "Sentiment": sentiment, "Topics": topics})

    for i in range(len(article_summaries)):
        for j in range(i + 1, len(article_summaries)):
            title1, summary1, sentiment1 = article_summaries[i]
            title2, summary2, sentiment2 = article_summaries[j]

            if sentiment1 != sentiment2:
                sentences1 = summary1.split('.')[:2]
                sentences2 = summary2.split('.')[:2]
                first_two_1 = '. '.join([s.strip() for s in sentences1 if s.strip()]) + '.'
                first_two_2 = '. '.join([s.strip() for s in sentences2 if s.strip()]) + '.'

                comparison_text = f"'{title1}' discusses {first_two_1}, while '{title2}' focuses on {first_two_2}"
                impact_text = f"{title1} presents a {sentiment1.lower()} outlook, whereas {title2} has a {sentiment2.lower()} perspective."

                coverage_differences.append({
                    "Comparison": comparison_text,
                    "Impact": impact_text
                })

    if all_summaries:
        merged_summary_text = " ".join(all_summaries)
        final_summary = summarize_text(merged_summary_text, max_sentences=7)
        translated_final_summary = GoogleTranslator(source="en", target="hi").translate(final_summary)
    else:
        final_summary = "Not enough content to generate a summary."
        translated_final_summary = "पर्याप्त सामग्री नहीं है सारांश बनाने के लिए।"

    common_topics = list(
        {topic for topic_list in all_topics for topic in topic_list[1] if sum(topic in t[1] for t in all_topics) > 1})
    unique_topics = list(
        {topic for topic_list in all_topics for topic in topic_list[1] if sum(topic in t[1] for t in all_topics) == 1})

    contradictory_viewpoints = []
    for topic, sentiments in sentiment_mapping.items():
        if "Positive" in sentiments and "Negative" in sentiments:
            contradictory_viewpoints.append(
                {"Topic": topic, "Contradiction": "Found positive and negative sentiments in different articles."})

    comparative_analysis = {
        "Sentiment Distribution": {"Positive": positive_count, "Negative": negative_count, "Neutral": neutral_count},
        "Topic Analysis": {"Common Topics": common_topics, "Unique Topics": unique_topics},
        "Contradictions": contradictory_viewpoints,
        "Coverage Differences": coverage_differences
    }

    tts = gTTS(text=translated_final_summary, lang="hi", slow=False)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    output_data = {
        "Company": company_symbol,
        "Articles": articles_data,
        "Comparative Sentiment Score": comparative_analysis,
        "Final Sentiment Analysis": final_summary,
        "Hindi Translation": translated_final_summary
    }

    return output_data, audio_buffer