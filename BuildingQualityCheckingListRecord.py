from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from urllib.request import urlopen

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
    msg = []
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
    msg.append(query.data)
##    keyboard = [
##        [InlineKeyboardButton("1", callback_data="1"),
##        InlineKeyboardButton("2", callback_data="2"),
##        InlineKeyboardButton("3", callback_data="3"),
##        InlineKeyboardButton("5", callback_data="5"),
##        InlineKeyboardButton("6", callback_data="6"),
##        InlineKeyboardButton("7", callback_data="7")]
##    ]
    keyboard = genKeyboard("", ["1", "2", "3", "5", "6", "7"])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='_'.join(msg) + "...\n請選擇樓:")
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
    msg.append(query.data)
    print(query.data)
##    keyboard = [
##        [InlineKeyboardButton("1", callback_data="1"),
##        InlineKeyboardButton("2", callback_data="2"),
##        InlineKeyboardButton("3", callback_data="3"),
##        InlineKeyboardButton("5", callback_data="5"),
##        InlineKeyboardButton("6", callback_data="6"),
##        InlineKeyboardButton("7", callback_data="7"),
##        InlineKeyboardButton("12", callback_data="12"),
##        InlineKeyboardButton("19", callback_data="19")]
##    ]
    # keyboard = genKeyboard("Floor", ["01", "02", "03", "05", "06", "07", "08", "09", "10", "11", "11duplex", "12", "12duplex", "15", "16", "17", "18", "19", "20"])
    keyboard = genKeyboard("", ["1", "2", "3", "5", "6", "7", "12", "19"])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='_'.join(msg) + "...\n請選擇樓層:"
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
    msg.append(query.data)
    # print(msg)
##    keyboard = [
##        [InlineKeyboardButton("A", callback_data="A"),
##        InlineKeyboardButton("B", callback_data="B"),
##        InlineKeyboardButton("D", callback_data="D"),
##        InlineKeyboardButton("F", callback_data="F"),
##        InlineKeyboardButton("G", callback_data="G"),
##        InlineKeyboardButton("J", callback_data="J"),
##        InlineKeyboardButton("L", callback_data="L")]
##    ]
    keyboard = genKeyboard("", ["A", "B", "D", "F", "G", "J", "L"])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text= '_'.join(msg) + u"... \n請選擇單位:"
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
    msg.append(query.data)
    url = 'http://localhost:8100/Building/Form%20Review?vf_Team=' + msg[0] +'&vf_Tower=Tower%20' + msg[1] + '&vf_Floor=' + msg[2] +'/F&vf_Flat=' + msg[3]
    data = urlopen(url)

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='_'.join(msg)
    )
    print('_'.join(msg))
    print(url)
    try:
        for line in data:
            bot.send_photo(chat_id=query.message.chat_id, photo=open(line.decode("utf-8"), 'rb'))
            break
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
