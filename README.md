# 🎬 Netflix-Style Movie Recommender System

A content-based Movie Recommendation System built using **Machine Learning + Streamlit**, deployed online with a Netflix-inspired UI.

---

## 🚀 Live Demo

👉 https://movie-recommender-2-swv4.onrender.com

---

## 📌 Features

* 🎥 Recommend similar movies based on content
* 🎨 Netflix-style dark UI with hover effects
* 🖼️ Fetch movie posters using TMDB API
* ⚡ Fast recommendations using precomputed similarity matrix
* ☁️ Handles large ML files using cloud storage (Dropbox)
* 🌐 Fully deployed web application

---

## 🧠 How It Works

* Dataset is processed to extract important features (genres, keywords, cast, etc.)
* Text data is converted using **CountVectorizer**
* Similarity between movies is calculated using **Cosine Similarity**
* Top 5 similar movies are recommended

---

## 🛠️ Tech Stack

* **Python**
* **Pandas**
* **Scikit-learn**
* **Streamlit**
* **Requests**
* **TMDB API**
* **Dropbox (for large file handling)**
* **Render (deployment)**

---

## 📂 Project Structure

```
movie-recommender/
│── app.py
│── requirements.txt
│── .gitignore
│── README.md
```

---

## ⚙️ Setup Instructions (Local)

1. Clone the repository

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This project is deployed on **Render**.

* Large `.pkl` files are hosted on **Dropbox**
* Files are downloaded at runtime to avoid GitHub size limits

---

## ⚠️ Challenges Faced

* ❌ GitHub file size limit (100MB)
* ❌ Google Drive download issues for large files
* ✅ Solved using Dropbox direct download links
* ✅ Implemented chunk-based file downloading

---

## 🔥 Future Improvements

* 🔍 Search with autocomplete
* ⭐ Show ratings & reviews
* 🎞️ Add movie trailers
* 🎨 Full Netflix homepage UI (multiple rows)
* 🤖 Hybrid recommendation system

---

## 👨‍💻 Author

**Arpan Mishra**

---

## ⭐ Show Your Support

If you like this project, give it a ⭐ on GitHub!
