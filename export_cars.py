import mysql.connector
import json
from decimal import Decimal

def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")
# 1. Kết nối đến MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="carrental_db"
)
cursor = conn.cursor(dictionary=True)

# 2. Truy vấn dữ liệu xe
cursor.execute("""
    SELECT 
    CarID,
    CarName,
    Seat,
    LicensePlate,
    Price,
    SalePrice,
    Color,
    Model,
    Rate,
    CarBrand,
    Details,
    Descriptions 
    from tbl_cars;
""")
rows = cursor.fetchall()

with open("cars.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2, default=convert_decimal)

print(f"✅ Đã ghi {len(rows)} xe vào cars.json")

cursor.close()
conn.close()