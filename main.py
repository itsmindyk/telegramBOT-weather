from telegram import *
from telegram.ext import *
import key as token
import replies as R

# WHAT CAN IT DO:
# 1. manual input of weeklies
# 1a. add countdown when weeklies end

# 2. battle pass profile - tier, deadline of current season's bp
# 2a. list of bp by tier
# 3. (ADV) get API? or upload and interpret bp


print("Starting up...")

def start_command(update, context):
    buttons = [[KeyboardButton("Weekly Challenges")], [KeyboardButton("Seasonal Battle Pass")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Seige Challenge Tracker for forgetful people like mindy",
    reply_markup=ReplyKeyboardMarkup(buttons))

    # update.message.reply_text('say something to start ah')

def help_command(update, context):
    update.message.reply_text('???? you lost ah')

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)

def error(update, context):
    print(f"Error: {update} caused error {context.error}")

# ------------------------------------------------------------------------------------------

def main():
    updater = Updater(token.API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()