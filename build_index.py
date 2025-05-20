from sentence_transformers import SentenceTransformer
import faiss, json, numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("cars.json", "r", encoding="utf-8") as f:
    cars = json.load(f)

# Biến mỗi xe thành 1 đoạn mô tả để vector hóa
texts = [
    f"{car['CarName']} - {car['Seat']} chỗ, màu {car['Color']}, biển số {car['LicensePlate']}, giá {car['Price']} VND. {car['Descriptions'] or ''} {car['Details'] or ''}"
    for car in cars
]

vectors = model.encode(texts)
index = faiss.IndexFlatL2(384)
index.add(np.array(vectors))

faiss.write_index(index, "vector_index.faiss")

with open("car_metadata.json", "w", encoding="utf-8") as f:
    json.dump(cars, f, ensure_ascii=False, indent=2)

print("✅ Đã tạo xong vector index và metadata.")
