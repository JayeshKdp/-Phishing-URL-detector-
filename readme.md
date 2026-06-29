phishing-url-detector/
│
├── app.py                 # Main Flask application
├── model.pkl              # Trained ML model
├── vectorizer.pkl         # URL feature/vectorizer
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version (optional)
├── Procfile               # For deployment (if needed)
├── render.yaml            # Render deployment configuration (optional)
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── dataset/
│   └── phishing_dataset.csv
│
├── model/
│   ├── train_model.py
│   └── feature_extraction.py
│
├── screenshots/
│   ├── homepage.png
│   └── result.png
│
├── LICENSE
└── README.md
