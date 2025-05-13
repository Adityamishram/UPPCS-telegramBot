
import json
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, PollAnswerHandler, CallbackContext
from telegram import Poll

# Load MCQs from JSON
with open("mcqs.json", "r") as f:
    mcqs = json.load(f)

user_state = {}

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_state[user_id] = {"index": 0, "score": 0}
    send_poll(update.effective_chat.id, context, user_id)

def send_poll(chat_id, context, user_id):
    idx = user_state[user_id]["index"]
    if idx < len(mcqs):
        q = mcqs[idx]
        correct_option = ord(q["answer"].upper()) - ord('A')
        context.bot.send_poll(
            chat_id=chat_id,
            question=f"Q{idx+1}: {q['question']}",
            options=[opt[3:].strip() for opt in q["options"]],
            type=Poll.QUIZ,
            correct_option_id=correct_option,
            is_anonymous=False
        )
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=f"🎉 Quiz complete! You scored {user_state[user_id]['score']}/{len(mcqs)}")

def handle_poll_answer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    poll_answer = update.poll_answer
    selected = poll_answer.option_ids[0]
    idx = user_state[user_id]["index"]
    correct = ord(mcqs[idx]["answer"].upper()) - ord('A')

    if selected == correct:
        user_state[user_id]["score"] += 1

    user_state[user_id]["index"] += 1
    send_poll(poll_answer.user.id, context, user_id)

def main():
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7453734359:AAEeBffcPyw_mvi0qgrqNo8gEj5gfw7sNmw")
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(PollAnswerHandler(handle_poll_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
