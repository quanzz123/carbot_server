from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import faiss, json, numpy as np, requests

app = Flask(__name__)
CORS(app)

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vector_index.faiss")

with open("car_metadata.json", "r", encoding="utf-8") as f:
    cars = json.load(f)

API_KEY = "AIzaSyAosiBnrBuwd-57U4AwQ6f0ddXHwT43IM4"
GENMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("message")
    if not question:
        return jsonify({"error": "Missing question"}), 400

    query_vector = model.encode([question])
    _, I = index.search(np.array(query_vector), k=3)

    context = "\n".join([
        (
            f"- {car['CarName']} ({car['CarBrand']} - {car['Model']}):\n"
            f"  • {car['Seat']} chỗ, màu {car['Color']}, biển số: {car['LicensePlate']}\n"
            f"  • Giá gốc: {car['Price']} VND, giá khuyến mãi: {car['SalePrice']} VND\n"
            f"  • Đánh giá: {car['Rate']} ⭐\n"
            f"  • Mô tả: {car['Descriptions'] or 'Không có mô tả'}\n"
            f"  • Chi tiết: {car['Details'] or 'Không có chi tiết'}"
        )
        for i in I[0]
        for car in [cars[i]]
    ])

    prompt = f"""Người dùng hỏi: {question}

Dưới đây là một số mẫu xe phù hợp:
{context}

Hãy trả lời thân thiện, giải thích rõ vì sao xe phù hợp.
"""

    response = requests.post(
        GENMINI_URL,
        headers={"Content-Type": "application/json"},
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    )

    reply = response.json()['candidates'][0]['content']['parts'][0]['text']
    return jsonify({"response": reply})
if __name__ == "__main__":
    app.run(debug=True, port=5000)
