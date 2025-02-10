from flask import Flask, request, jsonify, render_template
import spacy
from fuzzywuzzy import process
import random

app = Flask(__name__)  # Membuat aplikasi Flask

# Load model NLP
nlp = spacy.load("xx_ent_wiki_sm")

# Daftar intent dan kata kunci  
intents = {
    "hobi": ["hobi", "kesukaan", "kegiatan", "suka melakukan apa"],
    "nama": ["siapa namamu", "siapa kamu", "nama kamu"],
    "keahlian": ["keahlian", "bakat", "apa yang bisa kamu lakukan"],
    "umur": ["berapa usiamu", "berapa umurmu", "lahir tahun berapa"]
}

# Jawaban chatbot
responses = {
    "nama": [
        "Saya adalah Chatbot bernama VIMAX. Panggil saja aku VIMAX!",
        "Namaku VIMAX, chatbot cerdas buatan Tuan Alfin.",
        "Orang-orang memanggilku VIMAX! Senang bertemu denganmu!",
        "Saya VIMAX, chatbot yang siap membantumu!"
    ],
    "hobi": [
        "Saya suka membantu orang belajar coding dan memahami AI!",
        "Hobiku adalah menjawab pertanyaan dan ngobrol dengan manusia!",
        "Saya senang belajar hal baru, terutama tentang kecerdasan buatan!",
        "Menjadi asisten digital yang baik adalah hobiku!"
    ],
    "keahlian": [
        "Saya bisa menjawab pertanyaan tentang AI dan menebak kepribadian!",
        "Kemampuanku adalah memahami teks dan memberi jawaban yang cerdas!",
        "Saya bisa membantu dengan pertanyaan teknologi dan coding!",
        "Keahlianku adalah memberikan informasi dan menjadi teman ngobrol yang baik!"
    ],
    "umur": [
        "Saya hanyalah program komputer, jadi saya tidak punya umur!",
        "Saya tidak menua, karena saya hanya sebuah AI!",
        "Aku dibuat oleh Tuan Alfin, tapi aku tidak punya tanggal lahir.",
        "Usiaku tidak bisa dihitung seperti manusia, karena aku selalu ada!"
    ]
}

def detect_intent(user_input):
    """
    Fungsi untuk mendeteksi maksud (intent) pengguna berdasarkan teks yang diberikan.
    """
    user_input = user_input.lower()
    doc = nlp(user_input)

    best_match, confidence = None, 0
    for intent, keywords in intents.items():
        match, score = process.extractOne(user_input, keywords) # Cari kecocokan kata

        if score > confidence: #Jika kemiripan lebih dari 80%
            best_match, confidence = intent, score
        
        if best_match and confidence > 75:
            return random.choice(responses[best_match])


    return "Maaf, aku tidak mengerti. Coba tanyakan hal lain!"

@app.route('/')
def home():
    """
    Menampilkan halaman utama chatbot.
    """
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint untuk menerima input teks dari pengguna dan mengembalikan jawaban chatbot.
    """
    user_input = request.json.get("message")  # Ambil pesan pengguna dari request
    response = detect_intent(user_input)  # Dapatkan jawaban chatbot
    return jsonify({"reply": response})  # Kirimkan jawaban dalam format JSON

if __name__ == '__main__':
    app.run(debug=True)  # Jalankan server Flask
