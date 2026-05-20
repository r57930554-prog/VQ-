# 🎮 VQ - Weapon Testing Tool

برنامج اختبار الأسلحة للمسؤولين في لعبة VQ

![VQ Logo](https://img.shields.io/badge/VQ-Weapon%20Tester-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ المميزات

- 🔐 **نظام تسجيل دخول آمن** - 20 مفتاح خصري للمسؤولين
- 🎯 **كشف اللون الأخضر** - كشف تلقائي للدوائر الخضراء `#00FF00`
- 🔫 **نظام الإيم** - سحب الإيم مع التحكم الكامل في القوة
- 💥 **Auto Fire** - إطلاق تلقائي (كليك يسار أو R2)
- 🎲 **اختيار الهدف** - رأس أو صدر أو عشوائي
- ⚡ **أداء عالي** - 60+ FPS على جميع الأجهزة
- 🎨 **واجهة احترافية** - أزرق فاتح + أسود
- 📊 **عرض معلومات** - قوة السحب والهدف و FPS

## 🛠️ المتطلبات

- Python 3.8+
- opencv-python
- numpy
- pynput

## 📦 التثبيت

```bash
# تثبيت المكتبات
pip install -r requirements.txt
```

## 🚀 الاستخدام

```bash
python vq_tool.py
```

ثم أدخل أي مفتاح من المفاتيح:

```
As1, Gf2, Doushhsjuuhrhuh3, Ihsjsjsj4, Hfufifudu5,
Hdhehdudu6, Hdhdhdhdh7, Gfhdhdhdh8, Hrhdhdhdb9, Hsusjsiugfrbd10,
Ughhdhudhehh11, Brhdhdhchdhh12, Bfhfhfhdhxhxh13, Bfhfhfhdhhdh14,
Hfhdhdhdhskai15, Shshdhdhdhdhdhk16, Jdjdhdydvegdvrhdy17,
Hthdbdcrxecrheu18, Jdjdyfyevecdvehddyh19, Hdhdhdhdhdbdv20
```

## 🎮 التحكم

| المفتاح | الوظيفة |
|--------|--------|
| **كليك يسار** | Auto Fire |
| **حرف U** | زيادة قوة السحب |
| **حرف D** | تقليل قوة السحب |
| **حرف T** | تبديل نوع الهدف |
| **ESC/Q** | إيقاف البرنامج |

## 📋 أنواع الأهداف

1. **HEAD** 🎯 - الرأس
2. **CHEST** 💪 - الصدر
3. **RANDOM** 🎲 - عشوائي

## ⚙️ قوة السحب

قوة السحب تتراوح من **0.1** إلى **1.0**
- 0.1 = سحب خفيف جداً
- 0.5 = سحب متوسط (الافتراضي)
- 1.0 = سحب كامل

## 🔒 الأمان

- نظام تسجيل دخول بـ 3 محاولات فقط
- مفاتيح حصرية للمسؤولين
- لا يمكن تخطي التحقق

## 📊 الأداء

- ✅ **60+ FPS** على الأجهزة الضعيفة
- ✅ **120+ FPS** على الأجهزة القوية
- ✅ استهلاك موارد منخفض
- ✅ يشتغل على PS5 Remote Play

## 📝 الترخيص

MIT License - انظر `LICENSE` للتفاصيل

## 👨‍💻 المطور

**VQ Turki** 💙

---

**آخر تحديث**: 2026-05-20