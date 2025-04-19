# app.py
from flask import Flask, redirect, url_for, session, render_template, request, flash, g, jsonify
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from api import clean_tweet_text, fetch_tweets, generate_word_cloud, get_tweet_sentiment, plot_sentiment_pie_chart, save_and_print_cleaned_tweets
app = Flask(__name__)
app.secret_key = os.urandom(24)
from flask import send_from_directory
# Veritabanı bağlantısı ve tablo oluşturma
def init_db():
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT
        )
        ''')
        conn.commit()

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('users.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Google OAuth yapılandırması
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='',
    client_secret='',
    authorize_url='',
    access_token_url=""
    api_base_url='',
    client_kwargs={''},
    server_metadata_url='',
)

# Ana sayfa
@app.route('/')
def home():
    return render_template('home.html')

# Kullanıcı girişi
@app.route('/login')
def login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

# Yetkilendirme sonrası geri dönüş
@app.route('/auth')
def google_callback():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()

    email = user_info['email']
    session['name'] = user_info['name']

    if email == 'kocera63@gmail.com':
        return redirect('/admin_dashboard')
    else:
        return redirect('/user_dashboard')

@app.route('/user_dashboard')
def user_dashboard():
    if not session.get('name'):
        flash("Please log in first!")
        return redirect('/')
    return render_template('user_dashboard.html', name=session.get('name'))


@app.route('/analyze', methods=['POST'])
def analyze():
    if not session.get('name'):
        return redirect('/')

    try:
        query = request.form['text']
        tweets = fetch_tweets(query)

        if not tweets:
            flash('No tweets found. Please try again.')
            return redirect('/user_dashboard')

        # Tweet analizi ve temizleme
        cleaned_texts = save_and_print_cleaned_tweets(tweets)
        cleaned_tweets_list = [text for text in cleaned_texts.split('\n') if text.strip()]

        # Duygu analizi
        sentiment_results = {}
        for tweet in tweets:
            cleaned_text = clean_tweet_text(tweet.text)
            sentiment = get_tweet_sentiment(cleaned_text)
            sentiment_results[sentiment] = sentiment_results.get(sentiment, 0) + 1

        # Duygu analizi yüzdesi
        total_tweets = sum(sentiment_results.values())
        sentiment_percentages = {
            key: round((value / total_tweets) * 100, 1) for key, value in sentiment_results.items()
        }

        # Word cloud oluştur
        wordcloud_path = 'wordcloud.png'
        generate_word_cloud(cleaned_texts, f'dynamic/{wordcloud_path}')

        # Duygu analizi pastagramını oluştur
        sentiment_chart_path = 'sentiment_chart.png'
        plot_sentiment_pie_chart(sentiment_percentages, query, f'dynamic/{sentiment_chart_path}')

        return render_template('analysis_results.html',
                               sentiment_results=sentiment_percentages,
                               wordcloud_path=wordcloud_path,
                               sentiment_chart_path=sentiment_chart_path,
                               query=query,
                               cleaned_tweets=cleaned_tweets_list)


    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect('/user_dashboard')


# Genel hata yakalayıcı
@app.errorhandler(429)
def too_many_requests(e):
    flash('Too many requests. Please wait a few minutes and try again.')
    return redirect('/user_dashboard')


@app.errorhandler(Exception)
def handle_error(e):
    flash(f'An error occurred: {str(e)}')
    return redirect('/user_dashboard')
# Admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    name = session.get('name')
    if not name:
        flash("Please log in first!")
        return redirect('/')
    return render_template('admin_dashboard.html', name=name)

@app.route('/dynamic/<filename>')
def send_dynamic_file(filename):
    # dynamic klasörünün doğru yolu
    dynamic_folder = os.path.join(os.getcwd(),'dynamic')
    return send_from_directory(dynamic_folder, filename)

# Kullanıcı çıkış yapma
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
