# News Summarization and 
Text-to-Speech Application 

The **Financial News Analyzer** is a web-based application that fetches and analyzes financial news for publicly traded companies. It provides **sentiment analysis, topic extraction, comparative analysis,** and **text-to-speech** features, including a **Hindi summary** with audio output. The project consists of a **Flask-based backend API** and a **Streamlit-based frontend**, deployed on **Hugging Face Spaces**.

---

## 🚀 Live Demo

- **Frontend (Streamlit App):** [https://yashwanthnayak-financial-news-analyzer.hf.space](https://yashwanthnayak-financial-news-analyzer.hf.space)
- **Backend (Flask API):** [https://yashwanthnayak-financial-news-api.hf.space](https://yashwanthnayak-financial-news-api.hf.space)

---

## 🏗️ Project Structure

```
financial-news-analyzer/
│── backend/
│   ├── api.py           # Flask API
│   ├── utils.py         # Helper functions for news fetching and NLP processing
│   ├── requirements.txt # Dependencies for backend
│   ├── Dockerfile       # Containerization setup for Hugging Face deployment
│   ├── README.md        # Backend-specific README
│
│── frontend/
│   ├── app.py           # Streamlit frontend application
│   ├── utils.py         # Helper functions for frontend processing
│   ├── requirements.txt # Dependencies for frontend
│   ├── README.md        # Frontend-specific README
│
│── README.md            # This README file
│── .gitignore           # Git ignore file
```

---

## ⚙️ Features

✅ Fetches **latest news** for a given stock symbol from **Yahoo Finance**  
✅ **Sentiment Analysis** using **NLTK Vader**  
✅ **Topic Extraction** using **spaCy**  
✅ **Text Summarization** using **Sumy LSA**  
✅ **Hindi Translation** using **Google Translator**  
✅ **Text-to-Speech (TTS)** using **gTTS**  
✅ **Interactive UI** using **Streamlit**  
✅ **Comparative Analysis** of news articles   
✅ **Dockerized Deployment** for seamless execution  

---

## 🛠️ Dependencies

### **Backend (Flask API)**
- **Flask** (API framework)
- **Gunicorn** (WSGI server for Flask)
- **pandas, numpy** (Data processing)
- **BeautifulSoup4, requests** (Web scraping)
- **spaCy, NLTK, Sumy** (NLP processing)
- **Deep Translator** (Language translation)
- **gTTS** (Text-to-Speech)

### **Frontend (Streamlit App)**
- **Streamlit** (Web UI)
- **Flask, requests** (API integration)
- **pandas, numpy** (Data processing)

---

## 🛠️ Setup & Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YashwanthNayak/financial-news-analyzer.git
cd financial-news-analyzer
```

### **2️⃣ Setup the Backend (Flask API)**
#### **Option 1: Run Locally**
```bash
cd backend
pip install -r requirements.txt
python api.py
```
> The API will run on **http://localhost:7860**

#### **Option 2: Run with Docker**
```bash
cd backend
docker build -t financial-news-api .
docker run -p 7860:7860 financial-news-api
```

### **3️⃣ Setup the Frontend (Streamlit App)**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
> The frontend will be accessible at **http://localhost:8501**

### **4️⃣ Update API URL in Frontend**
- Edit **app.py** in `frontend/`
- Update `API_URL` with your backend URL (default: `http://localhost:7860/api`)

---

## 🎯 How It Works

1. Enter a **company stock symbol** (e.g., `AAPL`, `TSLA`)
2. Click **"Analyze News"**
3. The backend fetches the latest **news articles** from **Yahoo Finance**
4. The **NLP pipeline** processes the data:
   - Extracts key **topics**
   - Performs **sentiment analysis** (Positive, Negative, Neutral)
   - Summarizes the news in English and translates to **Hindi**
   - Generates **audio output** using **gTTS**
5. The frontend **displays results** with interactive charts and downloads.

---

## 📌 API Endpoints (Flask Backend)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status check |
| `/api/news/fetch` | POST | Fetches news for a given company |
| `/api/news/analyze` | POST | Analyzes sentiment, topics, and generates summaries |

---

## 🌍 Deployment on Hugging Face Spaces
### **Deploy Backend** (Flask API)
1. Push the **backend** code to a Hugging Face Space with **Docker** enabled.
2. Ensure `Dockerfile` installs required packages.
3. Deploy and note the **Flask API URL**.

### **Deploy Frontend** (Streamlit App)
1. Push the **frontend** code to a Hugging Face Space.
2. Set the **API_URL** environment variable in Streamlit settings.
3. Deploy and test the connection.

---

## 🤝 Contributing
Feel free to **fork** this repo, create a new **branch**, and submit a **Pull Request**! 🚀

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 📬 Contact
**Yashwanth Nayak**  
📧 Email: yashwanth.nayak@example.com  
🔗 LinkedIn: [linkedin.com/in/yashwanthnayak](https://linkedin.com/in/yashwanthnayak)  

---

⭐ If you like this project, please **star** this repository on GitHub! ⭐

