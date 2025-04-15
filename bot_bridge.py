import time
import requests

# 🔐 Токени
TG_TOKEN = "7729914687:AAGIiJ18cIFfd2xLD6ChWNsRKXm2RbczKjQ"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1361725683906117822/8KuTSIFRohQxPCixgKZRBiD-oCP547ZTwryfjLC0EaU3JEgbU4AgGcpdK9_W2KhLsN8-"

# 📍 Chat ID твоєї групи (замінити після запуску)
CHAT_ID = -1000000000000  # тимчасово, зараз скрипт його визначить

# 💬 Останній update_id для Telegram
last_update_id = None

def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates"
    if last_update_id:
        url += f"?offset={last_update_id + 1}"
    return requests.get(url).json()

def send_to_discord(text):
    data = {
        "content": f"{text}"
    }
    requests.post(DISCORD_WEBHOOK, json=data)

while True:
    updates = get_updates()
    if "result" in updates:
        for update in updates["result"]:
            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")
                
                # 🧑‍💻 Дістаємо ім'я юзера
                user = message.get("from", {})
                first_name = user.get("first_name", "Хтось")
                last_name = user.get("last_name", "")
                username = user.get("username", "")
                full_name = f"{first_name} {last_name}".strip()
                user_display = f"{full_name}" if username else full_name

                # 💡 Виводимо хто і що написав
                print(f"[TG] {user_display}: {text}")

                # Якщо перший запуск — запам'ятати chat_id
                if CHAT_ID == -1000000000000:
                    CHAT_ID = chat_id
                    print(f"[LOG] Встановлено CHAT_ID = {CHAT_ID}")

                if chat_id == CHAT_ID and text:
                    send_to_discord(f"{user_display}:\n    {text}")

                last_update_id = update["update_id"]
    time.sleep(2)
