#!/bin/bash
echo "========================================"
echo "  LITHO-SONIC - اختبارات بسيطة"
echo "========================================"
echo ""

echo "📊 اختبار LSI:"
echo "----------------------------------------"
python tests/simple/test_lsi_simple.py
echo ""

echo "📊 اختبار Biot:"
echo "----------------------------------------"
python tests/simple/test_biot_simple.py
echo ""

echo "📊 اختبار Fracture Resonance:"
echo "----------------------------------------"
python tests/simple/test_fracture_simple.py
echo ""

echo "========================================"
echo "✅ جميع الاختبارات البسيطة اكتملت!"
echo "========================================"
