#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import time

def send_accounting_notification():
    """
    ارسال اعلان معرفی پلتفرم حسابداری به سایت
    """
    
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
    
    # داده‌های اعلان
    notification_data = {
        "title": "🚀 معرفی پلتفرم حسابداری پیشرفته",
        "message": message,
        "type": "system_introduction",
        "timestamp": "1403/05/15"
    }
    
    # آدرس‌های سرور ممکن
    server_urls = [
        "http://localhost:5000",
        "http://127.0.0.1:5000", 
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    for server_url in server_urls:
        try:
            print(f"🔍 در حال آزمایش اتصال به: {server_url}")
            
            # ارسال درخواست POST به سرور
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
                
        except requests.exceptions.ConnectionError:
            print(f"❌ سرور در دسترس نیست: {server_url}")
            continue
        except requests.exceptions.Timeout:
            print(f"⏰ زمان انتظار به پایان رسید: {server_url}")
            continue
        except Exception as e:
            print(f"⚠️ خطا در اتصال به {server_url}: {e}")
            continue
    
    print("\n💡 راهنمایی:")
    print("1. مطمئن شوید سرور Flask در حال اجرا است")
    print("2. آدرس سرور را بررسی کنید")
    print("3. پورت‌های 5000 یا 8000 را بررسی کنید")
    return False

def check_server_status():
    """بررسی وضعیت سرور"""
    server_urls = [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:8000", 
        "http://127.0.0.1:8000"
    ]
    
    for server_url in server_urls:
        try:
            response = requests.get(f"{server_url}/", timeout=3)
            if response.status_code == 200:
                print(f"✅ سرور فعال است: {server_url}")
                return server_url
        except:
            continue
    
    print("❌ هیچ سرور فعالی یافت نشد")
    return None

if __name__ == "__main__":
    print("🚀 در حال ارسال اعلان معرفی پلتفرم حسابداری...")
    print("=" * 60)
    
    # بررسی وضعیت سرور
    active_server = check_server_status()
    
    if active_server:
        print(f"🎯 سرور فعال پیدا شد: {active_server}")
    else:
        print("🔍 در حال جستجوی سرور...")
    
    # ارسال اعلان
    success = send_accounting_notification()
    
    if success:
        print("\n🎉 عملیات با موفقیت انجام شد!")
        print("📋 پیام معرفی پلتفرم حسابداری ارسال گردید")
    else:
        print("\n😞 ارسال اعلان ناموفق بود")
        print("💡 لطفاً مطمئن شوید سرور Flask اجرا شده است")
        
    print("\n⏹️  برنامه به پایان رسید")
