#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import time

def send_instant_notification():
    message = """
---
پلتفرم حسابداری و حسابرسی ما یک راه‌حل کامل برای مدیریت مالی، حسابرسی و امور تولیدی کسب‌وکار شماست.
با این سیستم می‌توانید به‌صورت دقیق و هوشمند درآمدها، هزینه‌ها، موجودی انبار، فاکتورها و گردش حساب‌ها را کنترل کنید.

ویژگی‌های اصلی:

* حسابداری خودکار و دقیق
* مدیریت امور تولید و مواد اولیه
* گزارش‌گیری مالی لحظه‌ای و حرفه‌ای
* حسابرسی هوشمند و بررسی خطاهای مالی
* محیط کاربرپسند و پشتیبانی سریع

با این پلتفرم، همه چیز در یک‌جا جمع شده تا مدیریت مالی شما ساده‌تر، سریع‌تر و دقیق‌تر از همیشه باشد.
---
"""
    
    notification_data = {
        "title": "🚀 معرفی پلتفرم حسابداری پیشرفته",
        "message": message,
        "type": "system_introduction", 
        "timestamp": "1403/05/15"
    }
    
    server_url = "http://localhost:5000"
    
    print("⚡ در حال ارسال فوری اعلان...")
    
    try:
        response = requests.post(
            f"{server_url}/api/send-notification",
            json=notification_data,
            headers={"Content-Type": "application/json"},
            timeout=3  # زمان انتظار کوتاه
        )
        
        if response.status_code == 200:
            print("✅ اعلان فوری ارسال شد!")
            return True
        else:
            print(f"❌ خطا: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ خطا: {e}")
        return False

if __name__ == "__main__":
    # ارسال سریع بدون تاخیر
    success = send_instant_notification()
    
    if success:
        print("🎉 اعلان در کمتر از 1 ثانیه ارسال شد!")
    else:
        print("😞 ارسال ناموفق")
    
    # بستن سریع برنامه
    sys.exit(0 if success else 1)
