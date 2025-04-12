# 📢 Telegram Channel Forwarder (Web API)

This is a Python-based Flask + Telethon web service that listens to messages from a Telegram channel and forwards them to another Telegram group or channel.

## 🚀 Features

- Replaces @usernames with SOURCE_CHANNEL_ID or the @channel
- Removes t.me and telegram.me links
- Forwards both text and media messages
- Exposes a REST API to start forwarding remotely

---

## ⚙️ Requirements

- Python 3.7+
- Telethon
- Flask

Install dependencies:

```bash
pip install -r requirements.txt
