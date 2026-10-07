import os
import io
import base64
import requests
import telebot
from flask import Flask
from threading import Thread
from PIL import Image
from groq import Groq

# Environment Variables from Koyeb
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TWELVE_DATA_API_KEY = os.environ.get("TWELVE_DATA_API_KEY")
ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# Flask Server for Koyeb Health Check
app = Flask(__name__)

@app.route('/')
def home():
    return "Tanvir Trader 99 Zone Bot is Running 24/7 on Koyeb!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask).start()

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# High-Accuracy Trading Prompt
SYSTEM_PROMPT = """
You are an ultra-accurate, conservative trading assistant for Tanvir Trader 99 Zone.
Analyze the provided candlestick trading chart image with extreme precision and adhere strictly to these rules:

1. CONFIRMATION RULE: Only output UP (CALL) or DOWN (PUT) if AT LEAST TWO strong technical confirmations are visible (e.g., Support/Resistance Rejection, Engulfing Pattern, Trendline Breakdown).
2. RISK FILTER: If the market is volatile, sideways, or unclear, output "⚪ SKIP / NO CLEAR TRADE". DO NOT GUESS under any circumstances.
3. OUTPUT FORMAT STRICTLY IN BENGALI:
   📊 TANVIR TRADER 99 ZONE - HIGH ACCURACY SIGNAL 📊
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Asset Name: [Chart Asset Name or Unknown]
   Timeframe: 1 Minute (1M)
   🎯 SIGNAL DIRECTION: 🟢 UP (CALL) / 🔴 DOWN (PUT) / ⚪ SKIP

   ⏱️ EXACT ENTRY & DURATION:
   • Entry Timing: রানিং ক্যান্ডেলের ঠিক 00:01 বা 00:02 সেকেন্ডে এন্ট্রি নিন।
   • Expiry Duration: 1 Minute (১ মিনিট)

   🔍 TECHNICAL CONFIRMATION:
   1. [Reason 1 in Bengali]
   2. [Reason 2 in Bengali]

   ⚠️ RISK MANAGEMENT: বাজারে অতিরিক্ত অস্থিরতা (Volatility) থাকলে ট্রেড এভয়েড করুন।
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎉 **Tanvir Trader 99 Zone** বটে আপনাকে স্বাগতম!\n\nআপনার ট্রেডিং চার্টের পরিষ্কার স্ক্রিনশট পাঠান, বট ১ সেকেন্ডের মধ্যে নিখুঁত এন্ট্রি পয়েন্ট সহ অ্যানালাইসিস করে সিগন্যাল দেবে।")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    msg = bot.reply_to(message, "⏳ চার্ট নিখুঁতভাবে অ্যানালাইসিস করা হচ্ছে, অপেক্ষা করুন...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        base64_image = encode_image(downloaded_file)

        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": SYSTEM_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=1024
        )

        analysis = completion.choices[0].message.content
        bot.edit_message_text(analysis, chat_id=msg.chat.id, message_id=msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ অ্যানালাইসিস করতে সমস্যা হয়েছে: {str(e)}", chat_id=msg.chat.id, message_id=msg.message_id)

print("🤖 Tanvir Trader 99 Zone Bot Started on Koyeb...")
bot.infinity_polling()
