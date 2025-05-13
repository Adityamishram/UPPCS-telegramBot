
import json
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load MCQs
with open("mcqs.json", "r") as f:
    mcqs = json.load(f)

user_data = {}

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data[user_id] = {"index": 0, "score": 0}
    send_question(update, context)

def send_question(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    index = user_data[user_id]["index"]
    if index < len(mcqs):
        q = mcqs[index]
        options = "\n".join(q["options"])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Q{index+1}: {q['question']}\n\n{options}\n\nReply with A/B/C/D")
    else:
        score = user_data[user_id]["score"]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"🎉 Quiz finished! Your score: {score}/{len(mcqs)}")

def handle_answer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_data:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please type /start to begin the quiz.")
        return

    answer = update.message.text.strip().upper()
    if answer not in ['A', 'B', 'C', 'D']:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please reply with A, B, C or D.")
        return

    index = user_data[user_id]["index"]
    correct_answer = mcqs[index]["answer"]
    if answer == correct_answer:
        user_data[user_id]["score"] += 1
        reply = "✅ Correct!"
    else:
        reply = f"❌ Incorrect. Correct answer: {correct_answer}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    user_data[user_id]["index"] += 1
    send_question(update, context)

def main():
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7453734359:AAEeBffcPyw_mvi0qgrqNo8gEj5gfw7sNmw")
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
