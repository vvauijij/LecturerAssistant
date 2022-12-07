import bot_main
import app
import bot_launcher
import threading

if __name__ == "__main__":
    bot_main.init()
    threading.Thread(target=lambda: app.app.run(debug=False)).start()
    bot_launcher.launch()


