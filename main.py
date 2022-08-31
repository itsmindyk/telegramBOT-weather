from telegram import *
from telegram.ext import *
import key as token
import replies as R
import weekly_challenges as wc

# WHAT CAN IT DO:
# 1. manual input of weeklies
# 1a. add countdown when weeklies end

# 2. battle pass profile - tier, deadline of current season's bp
# 2a. list of bp by tier
# 3. (ADV) get API? or upload and interpret bp


print("Starting up...")

# when /start
def start_command(update, context):
    buttons = [[KeyboardButton("Weekly Challenges")], [KeyboardButton("Seasonal Battle Pass")]]
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Seige Challenge Tracker for forgetful people like mindy, what do you wanna do?",
    reply_markup=ReplyKeyboardMarkup(buttons))

    # update.message.reply_text('say something to start ah')

def help_command(update, context):
    update.message.reply_text('???? you lost ah')

def handle_message(update, context):
    reply = str(update.message.text).lower() # user reply

    # update.message.reply_text("you said " + reply + " right?")

    if (reply == "weekly challenges"):
        update.message.reply_text("you said " + reply + " right?")
        update.message.reply_text("Weekly Challenges for 23/8/22 - 30/8/22")

        buttons = [
            [InlineKeyboardButton("Add challenge", callback_data="add")],
            [InlineKeyboardButton("Delete challenge", callback_data="delete")]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        update.message.reply_text("This week's challenges: \n\n" +
                                    "1) Win 3 rounds as GSG9 \n"+
                                    "2/5 done \n\n" +
                                    "2) Win 5 rounds as Jackal or Mira in Training Grounds\n" +
                                    "4/5 done", reply_markup = reply_markup)

    print(update.callback_data)


    if (reply == "seasonal battle pass"):
        update.message.reply_text("sorry not working later come back pls")


#     update.message.reply_text(R.sample_responses(reply))

# def button (update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     query.answer()

#     choice = query.data
#     if choice == "add"


def error(update, context):
    print(f"Error: {update} caused error {context.error}")

# ------------------------------------------------------------------------------------------

def main():
    updater = Updater(token.API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command)) # when the app starts 
    dp.add_handler(CommandHandler("help", help_command)) #when you asking for help

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()