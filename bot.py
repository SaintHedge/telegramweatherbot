import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

CITY = "Kremenchuk,UA"
URL = "https://api.openweathermap.org/data/2.5/weather"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤 Бот погоди\n"
        "Команда: /weather"
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE_TYPE):
    params = {
        "q": CITY,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "uk"
    }

    r = requests.get(URL, params=params, timeout=10)
    data = r.json()

    text = (
        f"📍 Кременчук\n"
        f"🌡 {data['main']['temp']}°C (відч. {data['main']['feels_like']}°C)\n"
        f"💧 Вологість: {data['main']['humidity']}%\n"
        f"🌬 Вітер: {data['wind']['speed']} м/с\n"
        f"☁️ {data['weather'][0]['description'].capitalize()}"
    )

    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    app.run_polling()

if __name__ == "__main__":
    main()

