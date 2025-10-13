from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import json
import time
import os

app = Flask(__name__)
CORS(app, origins=["*"], methods=["GET", "POST"], allow_headers=["*"])

notifications = []

# HTML template سازگار با همه مرورگرها
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 سیستم حساب داری پیشرفته</title>
    <style>
        {{ original_css }}
        
        /* استایل اعلان برای همه مرورگرها */
        .flask-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #27ae60, #219653);
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
            border: 2px solid white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            -webkit-animation: slideInRight 0.5s ease-out;
            -moz-animation: slideInRight 0.5s ease-out;
            -o-animation: slideInRight 0.5s ease-out;
            animation: slideInRight 0.5s ease-out;
        }
        
        @-webkit-keyframes slideInRight {
            from { opacity: 0; -webkit-transform: translateX(100px); }
            to { opacity: 1; -webkit-transform: translateX(0); }
        }
        @-moz-keyframes slideInRight {
            from { opacity: 0; -moz-transform: translateX(100px); }
            to { opacity: 1; -moz-transform: translateX(0); }
        }
        @-o-keyframes slideInRight {
            from { opacity: 0; -o-transform: translateX(100px); }
            to { opacity: 1; -o-transform: translateX(0); }
        }
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(100px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
</head>
<body>
    {{ original_html }}

    <script>
        // سیستم اعلان‌ها - سازگار با همه مرورگرها
        (function() {
            'use strict';
            
            var receivedNotifications = [];
            var isInitialized = false;
            
            function initializeNotifications() {
                if (isInitialized) return;
                isInitialized = true;
                
                console.log('🚀 سیستم اعلان‌ها فعال شد');
                
                // بررسی اعلان‌ها هر 2 ثانیه
                setInterval(fetchNotifications, 2000);
                
                // بررسی اولیه
                setTimeout(fetchNotifications, 1000);
            }
            
            function fetchNotifications() {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/api/get-notifications', true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        try {
                            var data = JSON.parse(xhr.responseText);
                            console.log('📨 اعلان‌های دریافت شده:', data);
                            
                            if (data.notifications && data.notifications.length > 0) {
                                for (var i = 0; i < data.notifications.length; i++) {
                                    var notification = data.notifications[i];
                                    if (receivedNotifications.indexOf(notification.id) === -1) {
                                        showNotification(notification);
                                        receivedNotifications.push(notification.id);
                                    }
                                }
                            }
                        } catch (e) {
                            console.log('خطا در پردازش اعلان‌ها:', e);
                        }
                    }
                };
                xhr.send();
            }
            
            function showNotification(notification) {
                console.log('🎯 نمایش اعلان:', notification);
                
                // ایجاد المان اعلان (سازگار با همه مرورگرها)
                var notificationElement = document.createElement('div');
                notificationElement.className = 'flask-notification';
                
                var titleElement = document.createElement('div');
                titleElement.style.cssText = 'font-size: 1.2em; margin-bottom: 8px; font-weight: bold;';
                titleElement.textContent = notification.title;
                
                var messageElement = document.createElement('div');
                messageElement.style.cssText = 'font-size: 0.9em; white-space: pre-line; line-height: 1.4; margin-bottom: 10px;';
                messageElement.textContent = notification.message;
                
                var closeButton = document.createElement('button');
                closeButton.textContent = 'بستن';
                closeButton.style.cssText = 'margin-top: 10px; padding: 5px 10px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer;';
                closeButton.onclick = function() {
                    if (notificationElement.parentNode) {
                        notificationElement.parentNode.removeChild(notificationElement);
                    }
                };
                
                notificationElement.appendChild(titleElement);
                notificationElement.appendChild(messageElement);
                notificationElement.appendChild(closeButton);
                
                document.body.appendChild(notificationElement);
                
                // حذف خودکار بعد از 15 ثانیه
                setTimeout(function() {
                    if (notificationElement.parentNode) {
                        notificationElement.parentNode.removeChild(notificationElement);
                    }
                }, 15000);
            }
            
            // راه‌اندازی وقتی DOM آماده شد
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initializeNotifications);
            } else {
                initializeNotifications();
            }
            
            // همچنین وقتی window لود شد
            window.addEventListener('load', initializeNotifications);
            
        })();
    </script>
</body>
</html>"""

@app.route('/')
def serve_index():
    try:
        # خواندن فایل اصلی index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # استخراج استایل‌ها
        import re
        css_match = re.search(r'<style>(.*?)</style>', original_content, re.DOTALL)
        original_css = css_match.group(1) if css_match else ''
        
        # استخراج محتوای بدنه
        body_match = re.search(r'<body>(.*?)</body>', original_content, re.DOTALL)
        original_html = body_match.group(1) if body_match else original_content
        
        return render_template_string(
            HTML_TEMPLATE,
            original_css=original_css,
            original_html=original_html
        )
    except Exception as e:
        return f"خطا در بارگذاری صفحه: {str(e)}", 500

@app.route('/api/send-notification', methods=['POST', 'OPTIONS'])
def receive_notification():
    if request.method == 'OPTIONS':
        response = jsonify({"status": "ok"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
    
    try:
        data = request.get_json()
        
        if not data or 'title' not in data or 'message' not in data:
            return jsonify({"error": "داده‌های ناقص"}), 400
        
        notification = {
            "id": int(time.time() * 1000),
            "title": data['title'],
            "message": data['message'],
            "type": data.get('type', 'terminal'),
            "timestamp": data.get('timestamp', '1403/05/15'),
            "read": False
        }
        
        notifications.append(notification)
        
        print(f"📢 اعلان جدید دریافت شد!")
        print(f"📝 عنوان: {notification['title']}")
        print(f"📄 متن: {notification['message']}")
        print("=" * 50)
        
        response = jsonify({
            "status": "success",
            "message": "اعلان با موفقیت دریافت شد",
            "notification_id": notification['id']
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-notifications', methods=['GET', 'OPTIONS'])
def get_notifications():
    if request.method == 'OPTIONS':
        response = jsonify({"status": "ok"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
        
    response = jsonify({
        "notifications": notifications,
        "count": len(notifications)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

if __name__ == '__main__':
    print("🚀 سرور Flask با سیستم اعلان‌ها در حال راه‌اندازی...")
    print("📡 آدرس سایت: http://localhost:5000")
    print("🌍 سازگار با همه مرورگرها و اپلیکیشن‌ها")
    print("⏳ آماده دریافت اعلان‌ها...")
    app.run(debug=True, host='0.0.0.0', port=5000)
