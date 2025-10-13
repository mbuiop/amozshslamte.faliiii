from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import time
import os

app = Flask(__name__)
CORS(app)

notifications = []

@app.route('/')
def serve_index():
    return send_file('index.html')

# سرویس برای سرو فایل JavaScript
@app.route('/notification_system.js')
def serve_js():
    return send_file('notification_system.js')

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
    print("🚀 سرور Flask در حال راه‌اندازی...")
    print("📡 آدرس سایت: http://localhost:5000")
    print("⏳ آماده دریافت اعلان‌ها...")
    app.run(debug=True, host='0.0.0.0', port=5000)
