#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import webbrowser
import time

def send_notification():
    print("🚀 در حال ارسال اعلان به سایت...")
    
    # باز کردن سایت
    url = "https://mbuiop.github.io/amozshslamte.faliiii/"
    webbrowser.open(url)
    
    print("✅ سایت باز شد!")
    print("\n🎯 حالا این کارها را انجام بده:")
    print("1. در سایت F12 بزن")
    print("2. به تب Console برو") 
    print("3. کد زیر را paste کن و Enter بزن:\n")
    
    # کد JavaScript برای نمایش اعلان
    js_code = """
var n=document.createElement('div');
n.style.cssText='position:fixed;top:20px;right:20px;background:linear-gradient(135deg,#27ae60,#219653);color:white;padding:20px;border-radius:10px;box-shadow:0 5px 20px rgba(0,0,0,0.3);z-index:10000;max-width:400px;border:2px solid white;font-family:Segoe UI,sans-serif;animation:slideInRight 0.5s ease-out;';
n.innerHTML='<div style="font-size:1.2em;margin-bottom:8px;font-weight:bold;">🚀 سیستم حسابداری پیشرفته</div><div style="font-size:0.9em;white-space:pre-line;line-height:1.4;">پلتفرم کامل مدیریت مالی و حسابرسی\\\\n\\\\nویژگی‌ها:\\\\n• حسابداری خودکار\\\\n• گزارش‌گیری لحظه‌ای\\\\n• محیط کاربرپسند\\\\n• پشتیبانی سریع</div><button onclick="this.parentElement.remove()" style="margin-top:10px;padding:5px 10px;background:#e74c3c;color:white;border:none;border-radius:5px;cursor:pointer;">بستن</button>';
document.body.appendChild(n);
var s=document.createElement('style');
s.textContent='@keyframes slideInRight{from{opacity:0;transform:translateX(100px);}to{opacity:1;transform:translateX(0);}}';
document.head.appendChild(s);
setTimeout(()=>{if(n.parentElement)n.remove();},15000);
"""
    
    print(js_code)
    print("\n⏳ اعلان برای 15 ثانیه نمایش داده می‌شود...")

if __name__ == "__main__":
    send_notification()
