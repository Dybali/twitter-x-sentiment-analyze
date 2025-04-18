# twitter-x-sentiment-analyze
Twitter üzerinde duygu analizi yapan Flask tabanlı bir web uygulamasıdır. Kullanıcılar anahtar kelime girerek Twitter'dan ilgili tweet'leri çekebilir, bu tweet'leri temizleyip analiz edebilir ve duygu analizi  sonuçlarını grafiklerle görebilir.
# 📊 Comeback Sentiment Analysis

Bu proje, kullanıcıların belirli bir konu, kelime veya hashtag'e dair atılmış tweet'leri analiz etmesine olanak tanıyan bir **duygu analizi web uygulamasıdır**. Uygulama, **Flask**, **Twitter API**, **TextBlob** ve **WordCloud** gibi teknolojileri kullanarak tweet'lerin temizlenmesini, analiz edilmesini ve görselleştirilmesini sağlar.

## 🔍 Özellikler

- 🔐 Kullanıcı girişi (Google OAuth ile ya da manuel olarak)
- 📥 Twitter'dan canlı tweet çekme
- 🧹 Tweet temizleme ve kayıt
- 😊 Duygu analizi (pozitif, negatif, nötr)
- ☁️ Word Cloud oluşturma
- 📈 Pasta grafik ile duygu dağılımı
- 👨‍💼 Admin ve kullanıcı rolleri için ayrı paneller
- ✅ Birim testleri ile güvenilirlik

## 📸 Ekran Görüntüleri

| Kullanıcı Girişi | Duygu Analizi Sonuçları |
|------------------|--------------------------|
| ![Login](static/screenshots/login.png) | ![Analysis](static/screenshots/analysis.png) |

## 🧪 Kurulum ve Çalıştırma

### Gereksinimler

- Python 3.9+
- Flask
- Tweepy
- TextBlob
- WordCloud
- matplotlib

### Kurulum

```bash

