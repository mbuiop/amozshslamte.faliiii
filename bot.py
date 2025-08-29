import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import math

# کلاس اصلی ربات
class AdvancedTradingBot:
    def __init__(self):
        self.user_states = {}
        self.templates = {
            "قالب یک": {"rsi": 25, "ema20": 20, "ema50": 18, "upper": 15, "macd": 22},
            "قالب دو": {"rsi": 30, "ema20": 25, "ema50": 20, "upper": 12, "macd": 13},
            "قالب سه": {"rsi": 22, "ema20": 28, "ema50": 25, "upper": 10, "macd": 15},
            "قالب چهار": {"rsi": 35, "ema20": 15, "ema50": 30, "upper": 8, "macd": 12},
            "قالب پنج": {"rsi": 28, "ema20": 22, "ema50": 22, "upper": 14, "macd": 14}
        }
        
    def load_data(self):
        """بارگیری داده‌ها از فایل JSON"""
        try:
            if os.path.exists('m1.json'):
                with open('m1.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except:
            return []
    
    def save_data(self, data):
        """ذخیره داده‌ها در فایل JSON"""
        try:
            with open('m1.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطا در ذخیره: {e}")

    def calculate_rsi_signal(self, rsi_value, weight):
        """محاسبه سیگنال RSI با وزن‌دهی پیشرفته"""
        if rsi_value < 20:
            return weight * 1.0  # خرید قوی
        elif rsi_value < 30:
            return weight * 0.8  # خرید متوسط
        elif rsi_value < 40:
            return weight * 0.4  # خرید ضعیف
        elif rsi_value > 80:
            return weight * -1.0  # فروش قوی
        elif rsi_value > 70:
            return weight * -0.8  # فروش متوسط
        elif rsi_value > 60:
            return weight * -0.4  # فروش ضعیف
        else:
            return 0  # خنثی

    def calculate_ema_signal(self, ema20, ema50, current_price, weight):
        """محاسبه سیگنال EMA با الگوریتم پیچیده"""
        ema_diff = ((ema20 - ema50) / ema50) * 100
        price_to_ema20 = ((current_price - ema20) / ema20) * 100
        
        if ema20 > ema50 and price_to_ema20 > 0.5:
            signal_strength = min(abs(ema_diff) / 2, 1.0)
            return weight * signal_strength
        elif ema20 < ema50 and price_to_ema20 < -0.5:
            signal_strength = min(abs(ema_diff) / 2, 1.0)
            return weight * -signal_strength
        else:
            return weight * 0.2 if ema20 > ema50 else weight * -0.2

    def calculate_upper_band_signal(self, current_price, upper_band, weight):
        """محاسبه سیگنال نوار بولینگر بالایی"""
        distance_ratio = (upper_band - current_price) / upper_band * 100
        
        if distance_ratio < 1:  # نزدیک به نوار بالایی
            return weight * -0.9
        elif distance_ratio < 3:
            return weight * -0.6
        elif distance_ratio > 10:
            return weight * 0.7
        else:
            return weight * 0.2

    def calculate_macd_signal(self, macd_line, signal_line, histogram, weight):
        """محاسبه سیگنال MACD پیشرفته"""
        macd_diff = macd_line - signal_line
        
        # تشخیص کراس اور
        if macd_diff > 0 and histogram > 0:
            signal_strength = min(abs(macd_diff) * 10, 1.0)
            return weight * signal_strength
        elif macd_diff < 0 and histogram < 0:
            signal_strength = min(abs(macd_diff) * 10, 1.0)
            return weight * -signal_strength
        else:
            return weight * 0.1 if macd_diff > 0 else weight * -0.1

    def generate_advanced_signal(self, data, template_weights):
        """تولید سیگنال فوق‌العاده پیشرفته"""
        # محاسبه سیگنال‌های جداگانه
        rsi_signal = self.calculate_rsi_signal(data['rsi'], template_weights['rsi'])
        
        ema_signal = self.calculate_ema_signal(
            data['ema20'], data['ema50'], 
            (data['support'] + data['resistance']) / 2,
            (template_weights['ema20'] + template_weights['ema50']) / 2
        )
        
        upper_signal = self.calculate_upper_band_signal(
            (data['support'] + data['resistance']) / 2,
            data['upper'], template_weights['upper']
        )
        
        macd_signal = self.calculate_macd_signal(
            data.get('macd_line', data['macd']),
            data.get('signal_line', data['macd'] * 0.9),
            data.get('histogram', data['macd'] * 0.1),
            template_weights['macd']
        )
        
        # ترکیب سیگنال‌ها با الگوریتم هوشمند
        total_signal = rsi_signal + ema_signal + upper_signal + macd_signal
        total_weight = sum(template_weights.values())
        
        # نرمال‌سازی سیگنال
        normalized_signal = total_signal / total_weight * 100
        
        # تعیین جهت معامله
        if normalized_signal > 30:
            direction = "خرید قوی 🟢"
            leverage = min(int(abs(normalized_signal) / 10) + 2, 10)
        elif normalized_signal > 15:
            direction = "خرید متوسط 🔵"
            leverage = min(int(abs(normalized_signal) / 15) + 1, 5)
        elif normalized_signal < -30:
            direction = "فروش قوی 🔴"
            leverage = min(int(abs(normalized_signal) / 10) + 2, 10)
        elif normalized_signal < -15:
            direction = "فروش متوسط 🟠"
            leverage = min(int(abs(normalized_signal) / 15) + 1, 5)
        else:
            direction = "خنثی ⚪"
            leverage = 1
        
        # محاسبه نقاط ورود، سود و ضرر
        mid_price = (data['support'] + data['resistance']) / 2
        
        if "خرید" in direction:
            entry = data['support'] + (mid_price - data['support']) * 0.2
            take_profit = data['resistance'] * 0.98
            stop_loss = data['support'] * 1.02
        else:
            entry = data['resistance'] - (data['resistance'] - mid_price) * 0.2
            take_profit = data['support'] * 1.02
            stop_loss = data['resistance'] * 0.98
        
        # تولید توضیح دقیق
        explanation = f"""
🔍 تحلیل دقیق {data['symbol']}:
📊 RSI: {data['rsi']} (وزن: {template_weights['rsi']})
📈 EMA20: {data['ema20']} (وزن: {template_weights['ema20']})
📈 EMA50: {data['ema50']} (وزن: {template_weights['ema50']})
🔵 Upper Band: {data['upper']} (وزن: {template_weights['upper']})
⚡ MACD: {data['macd']} (وزن: {template_weights['macd']})

🧮 امتیاز کل: {normalized_signal:.2f}/100
        """
        
        return {
            "symbol": data['symbol'],
            "direction": direction,
            "entry": round(entry, 6),
            "take_profit": round(take_profit, 6),
            "stop_loss": round(stop_loss, 6),
            "leverage": leverage,
            "explanation": explanation,
            "timestamp": datetime.now().isoformat(),
            "signal_strength": abs(normalized_signal)
        }

# ایجاد نمونه از ربات
bot = AdvancedTradingBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع ربات"""
    keyboard = [
        [InlineKeyboardButton("قالب یک", callback_data="template_1")],
        [InlineKeyboardButton("قالب دو", callback_data="template_2")],
        [InlineKeyboardButton("قالب سه", callback_data="template_3")],
        [InlineKeyboardButton("قالب چهار", callback_data="template_4")],
        [InlineKeyboardButton("قالب پنج", callback_data="template_5")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 به ربات تحلیل پیشرفته تلگرام خوش آمدید!\n\n"
        "این ربات با استفاده از الگوریتم‌های پیچیده و سیستم وزن‌دهی هوشمند،"
        " دقیق‌ترین سیگنال‌های معاملاتی را تولید می‌کند.\n\n"
        "لطفاً یکی از قالب‌های آماده را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def template_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت انتخاب قالب"""
    query = update.callback_query
    await query.answer()
    
    template_map = {
        "template_1": "قالب یک",
        "template_2": "قالب دو", 
        "template_3": "قالب سه",
        "template_4": "قالب چهار",
        "template_5": "قالب پنج"
    }
    
    template_name = template_map.get(query.data)
    user_id = update.effective_user.id
    
    bot.user_states[user_id] = {
        "template": template_name,
        "step": "symbol",
        "data": {}
    }
    
    weights = bot.templates[template_name]
    await query.edit_message_text(
        f"✅ {template_name} انتخاب شد\n\n"
        f"🎯 وزن‌های این قالب:\n"
        f"RSI: {weights['rsi']}/100\n"
        f"EMA20: {weights['ema20']}/100\n"
        f"EMA50: {weights['ema50']}/100\n"
        f"Upper Band: {weights['upper']}/100\n"
        f"MACD: {weights['macd']}/100\n\n"
        f"📝 لطفاً نام ارز را وارد کنید (مثال: BTCUSDT):"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پیام‌های کاربر"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id not in bot.user_states:
        await update.message.reply_text("لطفاً ابتدا /start را فشار دهید.")
        return
    
    state = bot.user_states[user_id]
    
    if state["step"] == "symbol":
        state["data"]["symbol"] = text.upper()
        state["step"] = "resistance"
        await update.message.reply_text("📈 مقاومت را وارد کنید:")
        
    elif state["step"] == "resistance":
        try:
            state["data"]["resistance"] = float(text)
            state["step"] = "support"
            await update.message.reply_text("📉 حمایت را وارد کنید:")
        except ValueError:
            await update.message.reply_text("❌ لطفاً عدد معتبر وارد کنید:")
            
    elif state["step"] == "support":
        try:
            state["data"]["support"] = float(text)
            state["step"] = "rsi"
            await update.message.reply_text("📊 RSI را وارد کنید (0-100):")
        except ValueError:
            await update.message.reply_text("❌ لطفاً عدد معتبر وارد کنید:")
            
    elif state["step"] == "rsi":
        try:
            rsi = float(text)
            if 0 <= rsi <= 100:
                state["data"]["rsi"] = rsi
                state["step"] = "ema20"
                await update.message.reply_text("📈 EMA20 را وارد کنید:")
            else:
                await update.message.reply_text("❌ RSI باید بین 0 تا 100 باشد:")
        except ValueError:
            await update.message.reply_text("❌ لطفاً عدد معتبر وارد کنید:")
            
    elif state["step"] == "ema20":
        try:
            state["data"]["ema20"] = float(text)
            state["step"] = "ema50"
            await update.message.reply_text("📈 EMA50 را وارد کنید:")
        except ValueError:
            await update.message.reply_text("❌ لطفاً عدد معتبر وارد کنید:")
            
    elif state["step"] == "ema50":
        try:
            state["data"]["ema50"] = float(text)
            state["step"] = "upper"
            await update.message.reply_text("🔵 Upper Band را وارد کنید:")
        except ValueError:
            await update.message.reply_text("❌ لطفاً عدد معتبر وارد کنید:")
            
    elif state["step"] == "upper":
        try:
            state["data"]["upper"] = float(text)
            state["step"] = "macd"
            await update.message.reply_text("⚡ MACD را وارد کنید:")
        except ValueError:
            await update.message.reply_text("❌ لطفاً عدد معتبر وارد کنید:")
            
    elif state["step"] == "macd":
        try:
            state["data"]["macd"] = float(text)
            
            # تولید سیگنال پیشرفته
            template_weights = bot.templates[state["template"]]
            signal = bot.generate_advanced_signal(state["data"], template_weights)
            
            # ذخیره در فایل
            all_data = bot.load_data()
            all_data.append(signal)
            bot.save_data(all_data)
            
            # ارسال سیگنال
            signal_message = f"""
🎯 **سیگنال معاملاتی پیشرفته**

💰 **ارز:** {signal['symbol']}
📍 **جهت:** {signal['direction']}
🚀 **ورود:** {signal['entry']}
🎯 **حد سود:** {signal['take_profit']}
🛡 **حد ضرر:** {signal['stop_loss']}
📊 **اهرم:** {signal['leverage']}x

{signal['explanation']}

⭐ **قدرت سیگنال:** {signal['signal_strength']:.1f}/100
🕐 **زمان:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ سیگنال در فایل m1.json ذخیره شد
            """
            
            await update.message.reply_text(signal_message, parse_mode='Markdown')
            
            # ریست کردن وضعیت
            del bot.user_states[user_id]
            
        except ValueError:
            await update.message.reply_text("❌ لطفاً عدد معتبر وارد کنید:")

def main():
    """اجرای ربات"""
    # توکن ربات تلگرام خود را اینجا وارد کنید
    TOKEN = "7685135237:AAEmsHktRw9cEqrHTkCoPZk-fBimK7TDjOo"
    
    application = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(template_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 ربات تحلیل پیشرفته راه‌اندازی شد...")
    application.run_polling()

if __name__ == "__main__":
    main()
