#!/bin/bash
# LITHO-SONIC Complete Runner

# إعداد المسارات
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/litho_physics"

echo "🌍 LITHO-SONIC - Lithospheric Resonance Observatory"
echo "Version: 1.0.0 | DOI: 10.5281/zenodo.18931304"
echo "=========================================="
echo "PYTHONPATH: $PYTHONPATH"
echo "=========================================="

# دالة لتنفيذ الأوامر
run_command() {
    echo ""
    echo "▶️  $1"
    echo "------------------------------------------"
    eval "$2"
}

# قائمة الأوامر حسب الاختيار
case "$1" in
    test)
        run_command "تشغيل جميع الاختبارات" "python -m pytest tests/ -v"
        ;;
    test-lsi)
        run_command "اختبار LSI" "python -m pytest tests/test_lsi.py -v"
        ;;
    test-biot)
        run_command "اختبار Biot" "python -m pytest tests/test_biot.py -v"
        ;;
    test-all)
        run_command "تشغيل جميع الاختبارات مع التغطية" "python -m pytest tests/ -v --cov=litho_physics"
        ;;
    example)
        run_command "تشغيل مثال سريع" "
python -c '
from litho_physics.lsi import LithosphericStressIndex
from litho_physics.fracture_resonance import compute_resonance_frequency, FluidPhase
params = {\"b_c\": 0.72, \"z_c\": 0.68, \"f_n\": 2.3, \"alpha_att\": 0.77, \"s_ae\": 0.83}
lsi = LithosphericStressIndex().compute(params)
print(f\"LSI: {lsi:.3f}\")
print(f\"حالة: {LithosphericStressIndex().get_alert_level(lsi)}\")
'
        "
        ;;
    shell)
        echo "دخول إلى قذيفة Python مع المسارات المضبوطة..."
        python -c "import sys; print('✓ PYTHONPATH:', sys.path); import litho_physics; print('✓ litho_physics تم استيراده بنجاح')"
        python
        ;;
    install)
        run_command "تثبيت الحزمة في وضع التطوير" "pip install -e ."
        ;;
    clean)
        run_command "تنظيف ملفات التجميع" "find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true"
        ;;
    *)
        echo "الاستخدام: ./run_lithosonic.sh [الأمر]"
        echo ""
        echo "الأوامر المتاحة:"
        echo "  test        - تشغيل جميع الاختبارات"
        echo "  test-lsi    - تشغيل اختبار LSI فقط"
        echo "  test-biot   - تشغيل اختبار Biot فقط"
        echo "  test-all    - تشغيل جميع الاختبارات مع التغطية"
        echo "  example     - تشغيل مثال سريع"
        echo "  shell       - فتح قذيفة Python مع المسارات المضبوطة"
        echo "  install     - تثبيت الحزمة في وضع التطوير"
        echo "  clean       - تنظيف ملفات التجميع"
        echo ""
        echo "مثال:"
        echo "  ./run_lithosonic.sh test-lsi"
        ;;
esac
