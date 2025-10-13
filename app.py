#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def send_notification():
    print("🚀 در حال ایجاد سیستم اعلان...")
    
    # کد JavaScript اعلان
    js_code = """
    // سیستم اعلان حسابداری
    if (!window.accountingAlert) {
        window.accountingAlert = function() {
            var n = document.createElement('div');
            n.style.cssText = 'position:fixed;top:20px;right:20px;background:linear-gradient(135deg,#27ae60,#219653);color:white;padding:20px;border-radius:10px;box-shadow:0 5px 20px rgba(0,0,0,0.3);z-index:10000;max-width:500px;border:2px solid white;font-family:Segoe UI,sans-serif;animation:slideInRight 0.5s ease-out;';
            n.innerHTML = '<div style="font-size:1.2em;margin-bottom:8px;font-weight:bold;">🚀 معرفی پلتفرم حسابداری</div><div style="font-size:0.9em;white-space:pre-line;line-height:1.4;">پلتفرم حسابداری و حسابرسی ما یک راه‌حل کامل برای مدیریت مالی و تولیدی کسب‌وکار شماست.\\\\n\\\\nویژگی‌ها:\\\\n• حسابداری خودکار و دقیق\\\\n• مدیریت امور تولید\\\\n• گزارش‌گیری مالی لحظه‌ای\\\\n• حسابرسی هوشمند\\\\n• محیط کاربرپسند</div><button onclick="this.parentElement.remove()" style="margin-top:10px;padding:5px 10px;background:#e74c3c;color:white;border:none;border-radius:5px;cursor:pointer;">بستن</button>';
            document.body.appendChild(n);
            var s = document.createElement('style');
            s.textContent = '@keyframes slideInRight{from{opacity:0;transform:translateX(100px);}to{opacity:1;transform:translateX(0);}}';
            document.head.appendChild(s);
            setTimeout(() => { if(n.parentElement) n.remove(); }, 15000);
        };
        window.accountingAlert();
    }
    """
    
    try:
        # آپلود به گیت‌هاب
        gist_data = {
            "public": False,  # خصوصی باشه
            "description": "Accounting System Notification",
            "files": {
                "alert.js": {"content": js_code}
            }
        }
        
        response = requests.post(
            "https://api.github.com/gists",
            json=gist_data,
            timeout=10
        )
        
        if response.status_code == 201:
            raw_url = response.json()['files']['alert.js']['raw_url']
            
            print("✅ سیستم اعلان آماده شد!")
            print("\n🎯 کاربران این یک خط را در کنسول اجرا کنند:")
            print("=" * 50)
            print(f"fetch('{raw_url}').then(r=>r.text()).then(eval)")
            print("=" * 50)
            print("\n📱 در مرورگر: F12 → Console → کد بالا → Enter")
            
            return True
            
    except Exception as e:
        print(f"⚠️ خطا: {e}")
        # روش جایگزین
        print("\n📝 کاربران این کد را اجرا کنند:")
        print("=" * 50)
        print(js_code)
        print("=" * 50)
        
    return True

if __name__ == "__main__":
    send_notification()
