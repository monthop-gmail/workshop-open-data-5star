#!/bin/bash
# ตัวอย่างการเรียก API ด้วย curl

echo "=== ดึงข้อมูลทุกภูมิภาค ==="
curl -s http://localhost:5000/api/v1/energy/regions | jq .

echo ""
echo "=== ดึงข้อมูลภาคอีสาน ==="
curl -s http://localhost:5000/api/v1/energy/regions/TH-NE | jq .

echo ""
echo "=== ดึงข้อมูลสรุป ==="
curl -s http://localhost:5000/api/v1/energy/summary | jq .
