
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace with your Telegram bot token from BotFather
TELEGRAM_BOT_TOKEN = '7872995076:AAFw4M1kQcqNwkejmR844buZKZClL1pyEsY'

# Replace with the free sports API URL (e.g., TheSportsDB or another API)
API_URL = 'https://www.thesportsdb.com/api/v1/json/1/eventsday.php?s=basketball&d={date}'

# Function to fetch fixtures
def fetch_fixtures(date):
    try:
        response = requests.get(API_URL.format(date=date))
        response.raise_for_status()
        data = response.json()
        events = data.get('events', [])

        if not events:
            return "No basketball fixtures found for today."

        fixtures = []
        for event in events:
            league = event.get('strLeague', 'Unknown League')
            home_team = event.get('strHomeTeam', 'Unknown')
            away_team = event.get('strAwayTeam', 'Unknown')
            time = event.get('strTime', 'Unknown Time')
            fixtures.append(f"{league}: {home_team} vs {away_team} at {time}")

        return "\n".join(fixtures)
    except Exception as e:
        return f"Error fetching fixtures: {str(e)}"

# Command to send daily fixtures
def daily_fixtures(update: Update, context: CallbackContext):
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    fixtures = fetch_fixtures(today)
    update.message.reply_text(fixtures)

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /fixtures to get today's basketball fixtures.")

# Main function to run the bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fixtures", daily_fixtures))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
