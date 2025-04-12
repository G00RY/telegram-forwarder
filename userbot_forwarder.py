import asyncio
import re
import tkinter as tk
from tkinter import messagebox
from telethon import TelegramClient, events
import threading

# === TELEGRAM CREDENTIALS ===
API_ID = you api id  # Replace with your actual API_ID
API_HASH = 'you api hash'  # Replace with your actual API_HASH

# === GUI APP ===
class ForwarderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("📢 Telegram Channel Forwarder")
        self.master.geometry("400x250")

        # Source channel input
        tk.Label(master, text="🔗 Source Channel Username (@channel):").pack(pady=(10, 0))
        self.source_entry = tk.Entry(master, width=45)
        self.source_entry.pack()

        # Target chat input
        tk.Label(master, text="🎯 Target Chat ID (e.g., -1001234567890):").pack(pady=(10, 0))
        self.target_entry = tk.Entry(master, width=45)
        self.target_entry.pack()

        # Start button
        self.start_btn = tk.Button(master, text="🚀 Start Forwarding", command=self.start_forwarding)
        self.start_btn.pack(pady=20)

        # Setup Telegram client
        self.client = TelegramClient('user_session', API_ID, API_HASH)

    def clean_text(self, text):
        if not text:
            return ""
        # Replace all @usernames with @SOURCE_CHANNEL
        text = re.sub(r'@\w+', '@SOURCE_CHANNEL', text)
        # Remove t.me links
        text = re.sub(r'https?://(t\.me|telegram\.me)/\S+', '', text)
        return text.strip()

    def start_forwarding(self):
        source = self.source_entry.get().strip()
        target = self.target_entry.get().strip()

        if not source or not target:
            messagebox.showerror("Error", "Please fill in both source and target fields.")
            return

        try:
            target_id = int(target)
        except ValueError:
            messagebox.showerror("Error", "Target chat ID must be a number (e.g., -100...).")
            return

        # Start the asynchronous task using asyncio's event loop
        threading.Thread(target=self.run_telethon_thread, args=(source, target_id), daemon=True).start()

    def run_telethon_thread(self, source, target_id):
        loop = asyncio.new_event_loop()  # Create a new event loop
        asyncio.set_event_loop(loop)  # Set the new event loop
        loop.run_until_complete(self.run_telethon(source, target_id))  # Run the asynchronous task

    async def run_telethon(self, source, target_id):
        await self.client.start()
        messagebox.showinfo("Success", "✅ Logged in! Now listening for new messages...")

        @self.client.on(events.NewMessage(chats=source))
        async def handler(event):
            msg = event.message
            content = msg.text or msg.message or ""
            cleaned = self.clean_text(content)

            try:
                if msg.media:
                    await self.client.send_file(target_id, file=msg.media, caption=cleaned)
                else:
                    await self.client.send_message(target_id, cleaned)
                print("✅ Forwarded message")
            except Exception as e:
                print(f"❌ Failed to forward: {e}")

        # Run until disconnected (blocks here)
        await self.client.run_until_disconnected()

# === RUN GUI ===
def run_gui():
    root = tk.Tk()
    app = ForwarderApp(root)
    
    # Run the Tkinter GUI
    root.mainloop()

if __name__ == "__main__":
    run_gui()
