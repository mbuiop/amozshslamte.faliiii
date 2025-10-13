#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import webbrowser

def send_notification():
    print("🚀 در حال ارسال اعلان به سایت...")
    
    # باز کردن سایت
    url = "https://mbuiop.github.io/amozshslamte.faliiii/"
    webbrowser.open(url)
    
    print("✅ سایت باز شد!")
    print("\n🎯 حالا این کارها را انجام بده:")
    print("1. در سایت F12 بزن")
    print("2. به تب Console برو") 
    print("3. کد زیر را کپی کن و Enter بزن:\n")
    
    # کد JavaScript با پیام کامل شما
    js_code = """var n=document.createElement('div');
n.style.cssText='position:fixed;top:20px;right:20px;background:linear-gradient(135deg,#27ae60,#219653);color:white;padding:20px;border-radius:10px;box-shadow:0 5px 20px rgba(0,0,0,0.3);z-index:10000;max-width:500px;border:2px solid white;font-family:Segoe UI,sans-serif;animation:slideInRight 0.5s ease-out;';
n.innerHTML='<div style=\"font-size:1.2em;margin-bottom:8px;font-weight:bold;\">🚀 معرفی پلتفرم حسابداری پیشرفته</div><div style=\"font-size:0.9em;white-space:pre-line;line-height:1.4;\">پلتفرم حسابداری و حسابرسی ما یک راه‌حل کامل برای مدیریت مالی، حسابرسی و امور تولیدی کسب‌وکار شماست.\\\\n\\\\nویژگی‌های اصلی:\\\\n\\\\n• حسابداری خودکار و دقیق\\\\n• مدیریت امور تولید و مواد اولیه\\\\n• گزارش‌گیری مالی لحظه‌ای و حرفه‌ای\\\\n• حسابرسی هوشمند و بررسی خطاهای مالی\\\\n• محیط کاربرپسند و پشتیبانی سریع\\\\n\\\\nبا این پلتفرم، همه چیز در یک‌جا جمع شده تا مدیریت مالی شما ساده‌تر، سریع‌تر و دقیق‌تر از همیشه باشد.</div><button onclick=\"this.parentElement.remove()\" style=\"margin-top:10px;padding:5px 10px;background:#e74c3c;color:white;border:none;border-radius:5px;cursor:pointer;\">بستن</button>';
document.body.appendChild(n);
var s=document.createElement('style');
s.textContent='@keyframes slideInRight{from{opacity:0;transform:translateX(100px);}to{opacity:1;transform:translateX(0);}}';
document.head.appendChild(s);
setTimeout(function(){if(n.parentElement)n.remove();},20000);"""
    
    print(js_code)
    print("\n⏳ اعلان برای 20 ثانیه نمایش داده می‌شود...")

if __name__ == "__main__":
    send_notification()
