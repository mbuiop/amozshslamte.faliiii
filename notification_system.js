// فایل: notification_system.js
// این فایل را در کنار index.html قرار بده

console.log('🚀 سیستم اعلان‌ها در حال بارگذاری...');

// سیستم دریافت اعلان‌ها از سرور Flask
let receivedNotifications = [];

// تابع برای دریافت اعلان‌ها از سرور
function fetchNotifications() {
    fetch('/api/get-notifications')
        .then(response => {
            if (!response.ok) {
                throw new Error('خطا در دریافت اعلان‌ها');
            }
            return response.json();
        })
        .then(data => {
            console.log('📨 داده‌های دریافت شده:', data);
            
            if (data.notifications && data.notifications.length > 0) {
                // نمایش اعلان‌های جدید
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

// تابع برای نمایش اعلان
function showNotification(notification) {
    console.log('🎯 نمایش اعلان:', notification);
    
    // ایجاد المان اعلان
    const notificationElement = document.createElement('div');
    notificationElement.className = 'flask-notification-popup';
    notificationElement.innerHTML = `
        <div style="font-size: 1.2em; margin-bottom: 8px; font-weight: bold;">${notification.title}</div>
        <div style="font-size: 0.9em; white-space: pre-line; line-height: 1.4;">${notification.message}</div>
        <button onclick="this.parentElement.remove()" style="margin-top: 10px; padding: 5px 10px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer;">بستن</button>
    `;
    
    // اضافه کردن به صفحه
    document.body.appendChild(notificationElement);
    
    // حذف خودکار بعد از 15 ثانیه
    setTimeout(() => {
        if (notificationElement.parentElement) {
            notificationElement.remove();
        }
    }, 15000);
}

// اضافه کردن استایل به صفحه
const style = document.createElement('style');
style.textContent = `
.flask-notification-popup {
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
}

@keyframes slideInRight {
    from { 
        opacity: 0; 
        transform: translateX(100px); 
    }
    to { 
        opacity: 1; 
        transform: translateX(0); 
    }
}
`;
document.head.appendChild(style);

// بررسی اعلان‌ها هر 2 ثانیه
setInterval(fetchNotifications, 2000);

// بررسی اولیه
setTimeout(fetchNotifications, 1000);

console.log('✅ سیستم اعلان‌ها فعال شد!');
