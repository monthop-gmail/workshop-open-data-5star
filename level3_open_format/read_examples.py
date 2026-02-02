"""
ตัวอย่างการอ่านข้อมูล Level 3: Open Format
รองรับทั้ง JSON และ XML

รัน: python read_examples.py
"""

import json
import xml.etree.ElementTree as ET


def read_json():
    """อ่านข้อมูลจาก JSON"""
    print("=" * 50)
    print("อ่านจาก JSON")
    print("=" * 50)

    with open("energy_stats_2566.json", encoding="utf-8") as f:
        data = json.load(f)

    print(f"แหล่งข้อมูล: {data['metadata']['source']}")
    print(f"ปี: {data['metadata']['year']}")
    print(f"สัญญาอนุญาต: {data['metadata']['license']}")
    print()

    print("ข้อมูลรายภูมิภาค:")
    for region in data["data"]:
        print(f"  {region['region_th']}: {region['consumption_gwh']:,} GWh")

    print()
    print(f"รวมทั้งประเทศ: {data['summary']['total_consumption_gwh']:,} GWh")
    print()


def read_xml():
    """อ่านข้อมูลจาก XML"""
    print("=" * 50)
    print("อ่านจาก XML")
    print("=" * 50)

    tree = ET.parse("energy_stats_2566.xml")
    root = tree.getroot()

    # อ่าน metadata
    metadata = root.find("metadata")
    source = metadata.find("source").text
    year = metadata.find("year").text
    license_text = metadata.find("license").text

    print(f"แหล่งข้อมูล: {source}")
    print(f"ปี: {year}")
    print(f"สัญญาอนุญาต: {license_text}")
    print()

    # อ่านข้อมูลรายภูมิภาค
    print("ข้อมูลรายภูมิภาค:")
    for region in root.findall(".//region"):
        name_th = region.find("name[@lang='th']").text
        consumption = int(region.find("consumptionGWh").text)
        print(f"  {name_th}: {consumption:,} GWh")

    # อ่านข้อมูลสรุป
    summary = root.find("summary")
    total = int(summary.find("totalConsumptionGWh").text)
    print()
    print(f"รวมทั้งประเทศ: {total:,} GWh")
    print()


def compare_formats():
    """เปรียบเทียบ JSON vs XML"""
    print("=" * 50)
    print("เปรียบเทียบ JSON vs XML")
    print("=" * 50)

    import os

    json_size = os.path.getsize("energy_stats_2566.json")
    xml_size = os.path.getsize("energy_stats_2566.xml")

    print(f"ขนาดไฟล์ JSON: {json_size:,} bytes")
    print(f"ขนาดไฟล์ XML:  {xml_size:,} bytes")
    print()
    print("JSON:")
    print("  ✅ ขนาดเล็กกว่า")
    print("  ✅ Parse ง่าย/เร็ว")
    print("  ✅ เหมาะกับ Web APIs")
    print()
    print("XML:")
    print("  ✅ รองรับ attributes และ namespaces")
    print("  ✅ มี schema validation (XSD)")
    print("  ✅ รองรับหลายภาษาใน element เดียวกัน")
    print("  ✅ เหมาะกับ enterprise systems")


if __name__ == "__main__":
    read_json()
    read_xml()
    compare_formats()
