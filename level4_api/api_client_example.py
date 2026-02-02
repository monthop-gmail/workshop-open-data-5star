"""
ตัวอย่างการเรียกใช้ Energy Statistics API ด้วย Python

ก่อนรัน:
    pip install requests
    python api_server.py  (ในอีก terminal)

รัน:
    python api_client_example.py
"""

import requests

API_BASE = "http://localhost:5000/api/v1"


def get_all_regions():
    """ดึงข้อมูลทุกภูมิภาค"""
    response = requests.get(f"{API_BASE}/energy/regions")
    data = response.json()

    print("=== ข้อมูลทุกภูมิภาค ===")
    for region in data["data"]:
        print(f"  {region['region_th']}: {region['consumption_gwh']:,} GWh")
    print()


def get_single_region(region_code):
    """ดึงข้อมูลภูมิภาคเดียว"""
    response = requests.get(f"{API_BASE}/energy/regions/{region_code}")
    data = response.json()

    if data["status"] == "success":
        region = data["data"]
        print(f"=== {region['region_th']} ({region['region_en']}) ===")
        print(f"  การใช้ไฟฟ้า: {region['consumption_gwh']:,} GWh")
        print(f"  จำนวนผู้ใช้: {region['customers']:,} ราย")
        print(f"  อัตราเติบโต: {region['growth_rate']}%")
    else:
        print(f"Error: {data['message']}")
    print()


def get_summary():
    """ดึงข้อมูลสรุป"""
    response = requests.get(f"{API_BASE}/energy/summary")
    data = response.json()["data"]

    print("=== สรุปภาพรวม ===")
    print(f"  ปี: {data['year']}")
    print(f"  การใช้ไฟฟ้ารวม: {data['total_consumption_gwh']:,} GWh")
    print(f"  ผู้ใช้ไฟฟ้ารวม: {data['total_customers']:,} ราย")
    print(f"  อัตราเติบโตเฉลี่ย: {data['average_growth_rate']}%")
    print()


if __name__ == "__main__":
    print("Energy Statistics API Client Demo\n")

    # ตัวอย่างการเรียก API
    get_all_regions()
    get_single_region("TH-NE")  # ภาคอีสาน
    get_summary()
