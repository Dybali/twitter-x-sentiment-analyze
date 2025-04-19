import os
import matplotlib
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
matplotlib.use('Agg')
# Twitter API bilgileri
BEARER_TOKEN = ""
# Twitter API'yi başlat
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets(query, max_tweets=10):
    """Twitter API'si ile tweet çekme."""
    tweets = client.search_recent_tweets(query=query, max_results=max_tweets)
    return tweets.data

def clean_tweet_text(text):
    """Tweet'teki istenmeyen karakterleri temizleme."""
    text = re.sub(r"http\S+", "", text)  # Linkleri kaldır
    text = re.sub(r"@\w+", "", text)  # Kullanıcı etiketlerini kaldır
    text = re.sub(r"#", "", text)  # Hashtag işaretlerini kaldır
    text = re.sub(r"RT[\s]+", "", text)  # Retweet yazısını kaldır
    text = re.sub(r"[^\w\s]", "", text)  # Noktalama işaretlerini kaldır
    return text.strip()

def save_and_print_cleaned_tweets(tweets, filename="cleaned_tweets.txt"):
    """Temizlenmiş tweetleri hem ekrana yazdırır hem de bir dosyaya kaydeder."""
    cleaned_texts = []
    with open(filename, "w", encoding="utf-8") as file:
        for tweet in tweets:
            cleaned_text = clean_tweet_text(tweet.text)
            if cleaned_text:
                print(f"Cleaned Tweet: {cleaned_text}")
                file.write(cleaned_text + "\n")
                cleaned_texts.append(cleaned_text)
    
    print(f"Cleaned tweets saved to {filename}")
    return "\n".join(cleaned_texts)  # Tweetleri yeni satırlarla birleştir

def get_tweet_sentiment(tweet):
    """Tweet'in duygu analizini yap."""
    try:
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 'neutral'  # Hata durumunda var

def analyze_tweets(tweets):
    """Tweetlerin duygu analizini yap ve sonuçları döndür."""
    sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
    for tweet in tweets:
        cleaned_text = clean_tweet_text(tweet.text)
        sentiment = get_tweet_sentiment(cleaned_text)
        sentiments[sentiment] += 1
    return sentiments

import matplotlib.pyplot as plt

def plot_sentiment_pie_chart(sentiments, query, filename="dynamic/sentiment_chart.png"):
    """
    Duygu analizi sonuçlarını pastagram olarak görselleştir ve kaydet.
    """
    labels = sentiments.keys()
    sizes = sentiments.values()
    colors = ['#66B2FF', '#99FF99', '#FF9999']  # Positive, Neutral, Negative
    explode = [0.1 if label == 'Positive' else 0 for label in labels]  # Pozitif veriyi öne çıkar

    # Pastagram
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode)
    plt.title(f"Sentiment Analysis for: {query}")
    plt.axis('equal')  # Daireyi düzgün göster
    plt.savefig(filename)
    plt.close()


def generate_word_cloud(text, filename="dynamic/wordcloud_output.png"):
    """Temizlenmiş tweetlerden bir Word Cloud oluştur ve dosyaya kaydet."""
    # Ensure the static directory exists
    static_dir = os.path.dirname(filename)
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(filename)  # Görseli kaydet
    plt.close()  # Figure'i kapat
