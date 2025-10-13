#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import time

def send_accounting_notification():
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
    
    try:
        print(f"🔍 در حال آزمایش اتصال به: {server_url}")
        
        response = requests.post(
            f"{server_url}/api/send-notification",
            json=notification_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ اعلان با موفقیت ارسال شد به: {server_url}")
            print("📢 پیام معرفی پلتفرم حسابداری ارسال شد!")
            return True
        else:
            print(f"❌ سرور پاسخ داد اما خطا: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ سرور در دسترس نیست: {server_url}")
    except requests.exceptions.Timeout:
        print(f"⏰ زمان انتظار به پایان رسید: {server_url}")
    except Exception as e:
        print(f"⚠️ خطا در اتصال به {server_url}: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 در حال ارسال اعلان معرفی پلتفرم حسابداری...")
    print("=" * 60)
    
    success = send_accounting_notification()
    
    if success:
        print("\n🎉 عملیات با موفقیت انجام شد!")
        print("📋 پیام معرفی پلتفرم حسابداری ارسال گردید")
    else:
        print("\n😞 ارسال اعلان ناموفق بود")
        
    print("\n⏹️  برنامه به پایان رسید")
