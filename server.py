from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import json
import time
import os

app = Flask(__name__)
CORS(app)

notifications = []

# HTML template که فایل JS را هم شامل می‌شود
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 سیستم حساب داری پیشرفته</title>
    <!-- استایل‌های اصلی سایت شما -->
    <style>
        /* استایل‌های اصلی سایت شما اینجا کپی شود */
        {{ original_css }}
    </style>
</head>
<body>
    <div class="container">
        <!-- محتوای اصلی سایت شما -->
        {{ original_html }}
    </div>

    <!-- سیستم اعلان‌ها -->
    <script>
        // سیستم دریافت اعلان‌ها
        let receivedNotifications = [];

        function fetchNotifications() {
            fetch('/api/get-notifications')
                .then(response => response.json())
                .then(data => {
                    console.log('📨 اعلان‌های دریافت شده:', data);
                    if (data.notifications && data.notifications.length > 0) {
                        data.notifications.forEach(notification => {
                            if (!receivedNotifications.includes(notification.id)) {
                                showNotification(notification);
                                receivedNotifications.push(notification.id);
                            }
                        });
                    }
                })
                .catch(error => console.log('خطا در دریافت اعلان‌ها:', error));
        }

        function showNotification(notification) {
            console.log('🎯 نمایش اعلان:', notification);
            
            const notificationElement = document.createElement('div');
            notificationElement.style.cssText = `
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
                animation: slideInRight 0.5s ease-out;
                border: 2px solid white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            `;
            
            notificationElement.innerHTML = `
                <div style="font-size: 1.2em; margin-bottom: 8px; font-weight: bold;">${notification.title}</div>
                <div style="font-size: 0.9em; white-space: pre-line; line-height: 1.4;">${notification.message}</div>
                <button onclick="this.parentElement.remove()" style="margin-top: 10px; padding: 5px 10px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer;">بستن</button>
            `;
            
            document.body.appendChild(notificationElement);

            setTimeout(() => {
                if (notificationElement.parentElement) {
                    notificationElement.remove();
                }
            }, 15000);
        }

        // اضافه کردن انیمیشن
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from { opacity: 0; transform: translateX(100px); }
                to { opacity: 1; transform: translateX(0); }
            }
        `;
        document.head.appendChild(style);

        // شروع سیستم اعلان‌ها
        setInterval(fetchNotifications, 2000);
        setTimeout(fetchNotifications, 1000);
        console.log('🚀 سیستم اعلان‌ها فعال شد!');
    </script>
</body>
</html>
"""

@app.route('/')
def serve_index():
    # خواندن فایل اصلی index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # استخراج محتوای بین <style> و </style>
    import re
    css_match = re.search(r'<style>(.*?)</style>', original_content, re.DOTALL)
    original_css = css_match.group(1) if css_match else ''
    
    # استخراج محتوای بین <body> و </body>
    body_match = re.search(r'<body>(.*?)</body>', original_content, re.DOTALL)
    original_html = body_match.group(1) if body_match else original_content
    
    # رندر کردن template با محتوای اصلی
    return render_template_string(
        HTML_TEMPLATE,
        original_css=original_css,
        original_html=original_html
    )

@app.route('/api/send-notification', methods=['POST', 'OPTIONS'])
def receive_notification():
    if request.method == 'OPTIONS':
        return '', 200
    
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
        
        return jsonify({
            "status": "success",
            "message": "اعلان با موفقیت دریافت شد",
            "notification_id": notification['id']
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-notifications', methods=['GET', 'OPTIONS'])
def get_notifications():
    if request.method == 'OPTIONS':
        return '', 200
        
    return jsonify({
        "notifications": notifications,
        "count": len(notifications)
    }), 200

if __name__ == '__main__':
    print("🚀 سرور Flask با سیستم اعلان‌ها در حال راه‌اندازی...")
    print("📡 آدرس سایت: http://localhost:5000")
    print("⏳ آماده دریافت اعلان‌ها...")
    app.run(debug=True, host='0.0.0.0', port=5000)
