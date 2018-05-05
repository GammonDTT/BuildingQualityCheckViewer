from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

# TODO: Create parameters.txt containing the telegram bot token in the working directory
# TODO: Download all Tableau form image print out and place in the working directory with the file name in the following format: [Team]_[Tower#]_[Floor##]_[Flat#].jpg (e.g. Internal_Tower1_Floor01_FlatA)


with open("parameters.txt", "r") as f:
    TELEGRAM_HTTP_API_TOKEN = str(f.readline())

FIRST, SECOND, THIRD, FOURTH = range(4)


def genKeyboard(type, list):
    # Generate an Inline Keyboard by the type (tower / floor / flat) and a list of variables
    keyboard = []
    print(list)
    for i in range(len(list)):
        keyboard.append([
            InlineKeyboardButton("{}{}".format(type, list[i]), callback_data="{}{}".format(type, list[i]))
        ])
    return keyboard

def getFormRecord(bot, update):
    # Step 1 of conversation, ask for TEAM
    global msg
    msg = ""
    keyboard = [
        [InlineKeyboardButton("Internal", callback_data="Internal"),
        InlineKeyboardButton("SPU", callback_data="SPU"),
        InlineKeyboardButton("External", callback_data="External")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        u"請選擇隊伍:",
        reply_markup=reply_markup
    )
    return FIRST


def select_tower(bot, update):
    # Step 2 of conversation, ask for TOWER
    global msg
    query = update.callback_query
    msg += query.data
    keyboard = [
        [InlineKeyboardButton("Tower1", callback_data="Tower1"),
        InlineKeyboardButton("Tower2", callback_data="Tower2"),
        InlineKeyboardButton("Tower3", callback_data="Tower3"),
        InlineKeyboardButton("Tower5", callback_data="Tower5"),
        InlineKeyboardButton("Tower6", callback_data="Tower6"),
        InlineKeyboardButton("Tower7", callback_data="Tower7")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=msg + "...\n請選擇樓:")
    # update.message.reply_text(
    #     u"請選擇大樓:",
    #     reply_markup=reply_markup大
    # )

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return SECOND


def select_floor(bot, update):
    # Step 3 of conversation, ask for FLOOR
    global msg
    query = update.callback_query
    msg += "_" + query.data
    # print(query.data)
    # keyboard = [
    #     InlineKeyboardButton("Floor01", callback_data="Floor01"),
    #     InlineKeyboardButton("Floor02", callback_data="Floor02"),
    #     InlineKeyboardButton("Floor03", callback_data="Floor03")
    # ]
    keyboard = genKeyboard("Floor", ["01", "02", "03", "05", "06", "07", "08", "09", "10", "11", "11duplex", "12", "12duplex", "15", "16", "17", "18", "19", "20"])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=msg + "...\n請選擇樓層:"
    )

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return THIRD


def select_flat(bot, update):
    #  Step 4 of conversation, ask for FLAT
    global msg
    query = update.callback_query
    msg += "_" + query.data
    # print(msg)
    keyboard = genKeyboard("Flat", ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L"])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text= msg + u"... \n請選擇單位:"
    )

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return FOURTH


def final_input(bot, update):
    # Step 5 of conversation, return image
    global msg
    query = update.callback_query
    msg += "_" + query.data

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=msg
    )
    print(msg)
    try:
        bot.send_photo(chat_id=query.message.chat_id, photo=open('{}.jpg'.format(msg), 'rb'))
    except Exception:
        bot.send_message(chat_id=query.message.chat_id, text="Record not found!")


updater = Updater(TELEGRAM_HTTP_API_TOKEN)
msg = ""

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('get_form_record', getFormRecord)],
    states={
        FIRST: [CallbackQueryHandler(select_tower)],
        SECOND: [CallbackQueryHandler(select_floor)],
        THIRD: [CallbackQueryHandler(select_flat)],
        FOURTH: [CallbackQueryHandler(final_input)]
    },
    fallbacks=[CommandHandler('get_form_record', getFormRecord)]
)

updater.dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()

# TODO block other users from editing
# TODO set "msg" as dictionary, then get logic based on dictionary.item