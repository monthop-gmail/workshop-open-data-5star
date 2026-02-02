"""
Level 4: Open Data with API (Docker version)
Energy Statistics REST API

Endpoints:
    GET /                               - API documentation
    GET /api/v1/energy/regions          - ดึงข้อมูลทุกภูมิภาค
    GET /api/v1/energy/regions/{code}   - ดึงข้อมูลภูมิภาคเดียว
    GET /api/v1/energy/summary          - ดึงข้อมูลสรุป
    GET /health                         - Health check
"""

import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ข้อมูลสถิติพลังงานไฟฟ้า ปี 2566
ENERGY_DATA = {
    "TH-C": {
        "region_code": "TH-C",
        "region_th": "ภาคกลาง",
        "region_en": "Central",
        "consumption_gwh": 45230,
        "customers": 8542000,
        "growth_rate": 3.2,
        "year": 2566
    },
    "TH-N": {
        "region_code": "TH-N",
        "region_th": "ภาคเหนือ",
        "region_en": "North",
        "consumption_gwh": 18450,
        "customers": 4125000,
        "growth_rate": 2.8,
        "year": 2566
    },
    "TH-NE": {
        "region_code": "TH-NE",
        "region_th": "ภาคตะวันออกเฉียงเหนือ",
        "region_en": "Northeast",
        "consumption_gwh": 22180,
        "customers": 7890000,
        "growth_rate": 4.1,
        "year": 2566
    },
    "TH-S": {
        "region_code": "TH-S",
        "region_th": "ภาคใต้",
        "region_en": "South",
        "consumption_gwh": 15620,
        "customers": 3456000,
        "growth_rate": 2.5,
        "year": 2566
    },
    "TH-E": {
        "region_code": "TH-E",
        "region_th": "ภาคตะวันออก",
        "region_en": "East",
        "consumption_gwh": 28970,
        "customers": 2987000,
        "growth_rate": 5.3,
        "year": 2566
    }
}


@app.route("/")
def index():
    """API Documentation"""
    return jsonify({
        "name": "Energy Statistics API",
        "version": "1.0",
        "source": "กรมพัฒนาพลังงานทดแทนและอนุรักษ์พลังงาน (พพ.)",
        "level": "★★★★ Level 4: Open with API",
        "endpoints": {
            "GET /api/v1/energy/regions": "ดึงข้อมูลทุกภูมิภาค",
            "GET /api/v1/energy/regions/{code}": "ดึงข้อมูลภูมิภาคเดียว (TH-C, TH-N, TH-NE, TH-S, TH-E)",
            "GET /api/v1/energy/summary": "ดึงข้อมูลสรุป",
            "GET /health": "Health check"
        },
        "related_services": {
            "sparql_endpoint": "http://localhost:3030/energy/sparql",
            "sparql_ui": "http://localhost:3030/#/dataset/energy/query"
        }
    })


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "energy-api"})


@app.route("/api/v1/energy/regions")
def get_all_regions():
    """ดึงข้อมูลทุกภูมิภาค"""
    return jsonify({
        "status": "success",
        "count": len(ENERGY_DATA),
        "data": list(ENERGY_DATA.values())
    })


@app.route("/api/v1/energy/regions/<region_code>")
def get_region(region_code):
    """ดึงข้อมูลภูมิภาคเดียว"""
    region_code = region_code.upper()
    if region_code in ENERGY_DATA:
        return jsonify({
            "status": "success",
            "data": ENERGY_DATA[region_code]
        })
    else:
        return jsonify({
            "status": "error",
            "message": f"Region '{region_code}' not found",
            "valid_codes": list(ENERGY_DATA.keys())
        }), 404


@app.route("/api/v1/energy/summary")
def get_summary():
    """ดึงข้อมูลสรุป"""
    total_consumption = sum(r["consumption_gwh"] for r in ENERGY_DATA.values())
    total_customers = sum(r["customers"] for r in ENERGY_DATA.values())
    avg_growth = sum(r["growth_rate"] for r in ENERGY_DATA.values()) / len(ENERGY_DATA)

    return jsonify({
        "status": "success",
        "data": {
            "year": 2566,
            "total_consumption_gwh": total_consumption,
            "total_customers": total_customers,
            "average_growth_rate": round(avg_growth, 2),
            "region_count": len(ENERGY_DATA)
        }
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    print(f"Starting Energy Statistics API on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=debug)
