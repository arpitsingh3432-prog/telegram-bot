from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

TOKEN = "8679703645:AAGY3dL9j0MuEakyQiCmseGtCWQy-qDrfyc "

# Keep alive server (for Render)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# 🎉 Welcome Function
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.full_name
        username = f"@{member.username}" if member.username else "No username"

        caption = f"""🎉🌸 A Special Welcome! 🌸🎉

💖 Everyone, let's give a huge warm welcome to our newest member! 🥳✨

👤 Name: {name}
📌 Username: {username}

We're so excited to have you with us! 🤗 May you enjoy great conversations, make wonderful friends, and have an amazing time here. 🌟💬

Feel free to introduce yourself and jump into the chats anytime—we'd love to get to know you! 💕😊

🌈 Wishing you happiness, laughter, and lots of unforgettable moments with our family! 🫶💖

🎊 Once again, welcome to the family! 🎉🎈
"""

        # Get profile pic
        photos = await context.bot.get_user_profile_photos(member.id)

        if photos.total_count > 0:
            file = await context.bot.get_file(photos.photos[0][-1].file_id)
            await update.message.reply_photo(photo=file.file_path, caption=caption)
        else:
            await update.message.reply_text(caption)

# 🏷️ Tag All Command
async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    members = await context.bot.get_chat_administrators(chat.id)

    message = "👥 Tagging members:\n\n"

    for member in members:
        user = member.user
        if user.username:
            message += f"@{user.username} "
        else:
            message += f"[{user.full_name}](tg://user?id={user.id}) "

    await update.message.reply_text(message, parse_mode="Markdown")

# 🚀 Main Function
def main():
    bot = ApplicationBuilder().token(TOKEN).build()

    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    bot.add_handler(CommandHandler("tagall", tagall))

    keep_alive()
    bot.run_polling()

if __name__ == "__main__":
    main()
