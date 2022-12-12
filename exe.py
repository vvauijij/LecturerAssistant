from telegram_bot import lecturer_assistant_bot
import app
import threading

if __name__ == "__main__":
    threading.Thread(target=lambda: app.app.run(debug=False)).start()
    lecturer_assistant_bot.launch()
