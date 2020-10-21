from telegram import *
from telegram.ext import *
import sqlite3


conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# c.execute('''CREATE TABLE persons(data VARCHAR DEFAULT NULL )''')


bot = Bot('YOUR TOKEN')

CHOOSING, SUBCATEGORY, PRODUCT, FINAL = range(4)
facts = []


def start(update, context):
    reply_keyboard = [['Products'],
                      ['Orders', 'Feedback', 'Payments'],
                      ['Cart', 'Chat']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text('Welcome!To be best store for all your social media '
                              'services, like Instagram likes and followers.',
                              reply_markup=reply_markup)
    return CHOOSING


def respond(update, context):
    reply_key = [['Instagram'],
                 ['Spotify'],
                 ['Soundcloud'],
                 ['Cart'],
                 ['Back']]
    reply_markup = ReplyKeyboardMarkup(reply_key)
    update.message.reply_text('Choose Category', reply_markup=reply_markup)
    return SUBCATEGORY


def rept(update, context):
    reply_keyboard = [['Products'],
                      ['Orders', 'Feedback', 'Payments'],
                      ['Cart', 'Chat']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text('Welcome!To be best store for all your social media '
                              'services, like Instagram likes and followers.',
                              reply_markup=reply_markup)
    return CHOOSING


def repeat(update, context):
    keywords = [['Instagram'],
                ['Spotify'],
                ['Soundcloud'],
                ['Cart'],
                ['Back']]
    reply_markup = ReplyKeyboardMarkup(keywords)
    update.message.reply_text('Choose product', reply_markup=reply_markup)
    return SUBCATEGORY


def rpeat(update, context):
    keyboard = [['Likes'],
                ['Followers'],
                ['Cart', 'Back']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Choose subcategory or product', reply_markup=reply_markup)
    return PRODUCT


def insta(update, context):
    words = [['Likes'],
             ['Followers'],
             ['Cart', 'Back']]
    reply_markup = ReplyKeyboardMarkup(words)
    update.message.reply_text('Choose subcategory or product', reply_markup=reply_markup)
    return PRODUCT


def spot(update, context):
    reply = [['Plays'],
             ['Followers'],
             ['Cart', 'Back']]
    reply_markup = ReplyKeyboardMarkup(reply)
    update.message.reply_text('Choose subcategory or product', reply_markup=reply_markup)


def sound_cloud(update, context):
    reply_key = [['Plays', 'Likes'],
                 ['Followers', 'Repost'],
                 ['Cart', 'Back']]
    reply_markup = ReplyKeyboardMarkup(reply_key)
    update.message.reply_text('Choose subcategory or product', reply_markup=reply_markup)


def insta_like(update, context):
    keyboard = [['Instagram Likes | 1000 For 3$ | Lifetime Warranty [$3-30]'],
                ['Instagram High Quality Likes | 1000 For 3$ | Lifetime Warranty [$3-30'],
                ['Instagram Likes | 30000 For 60$ | Lifetime Warranty [$60]'],
                ['Cart', 'Back']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Choose product', reply_markup=reply_markup)
    return FINAL


def insta_fin(update, context):
    custom_keyboard = [[InlineKeyboardButton('1000 Likes-$3.00', callback_data='1000 Likes - $3.00')],
                       [InlineKeyboardButton('2000 Likes -$6.00', callback_data='2000 Likes - $6.00')],
                       [InlineKeyboardButton('3000 Likes -$9.00', callback_data='3000 Likes - $9.00')],
                       [InlineKeyboardButton('4000 Likes -$12.00', callback_data='4000 Likes - $12.00')],
                       [InlineKeyboardButton('5000 Likes -$15.00', callback_data='5000 Likes - $15.00')]]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo='https://i.pinimg.com/originals/72/a3/d9/72a3d9408d41335f39e9f014dc35cf44.jpg')
    update.message.reply_text('Please send us a link to your picture.\nPlease leave your profile on public.\n\nFor '
                              'bulk orders contact us.\nIf you have any questions feel free to send us a private '
                              'message.', reply_markup=reply_markup)


def button(update, context):
    # user = update.message.from_user
    query = update.callback_query
    text = str(query.data)
    query.edit_message_text(text='{} added to your cart'.format(query.data))
    c.execute('''INSERT INTO persons VALUES(?)''', (text,))
    conn.commit()
    # facts.append(text)
    context.user_data['cart'] = get_all_products()


def get_all_products():
    c.execute("SELECT * FROM persons")
    cat = c.fetchall()
    if cat is not None:
        return cat
    else:
        return False


def receive_info(update, context):
    try:
        value = context.user_data['cart']
        res = [' '.join(tups) for tups in value]
        items = "\n".join(res)
        msg = f"*You have the below items in your cart*\n\n{items}"
        update.message.reply_text(msg, parse_mode='markdown')
    except KeyError:
        update.message.reply_text('Cart is empty.')


def insta_foll(update, context):
    keyboard = [['Instagram Followers | 100 For $1 | Lifetime Warranty [$1-5]'],
                ['Instagram Followers | 1000 For $7 | Lifetime warranty [$7-70]'],
                ['Instagram Followers | 1000 For $2 | CHEAPEST [$2-20]'],
                ['Cart', 'Back']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Choose product', reply_markup=reply_markup)


def cancel(update, context):
    chat_id = update.message.chat.id
    update.message.reply_text(chat_id=chat_id, text='Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    # my_persistence = PicklePersistence(filename='my_file')
    updater = Updater('YOUR TOKEN', use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Products|Orders|Feedback|Payments|Chat)$'), respond),
                       MessageHandler(Filters.regex('^Cart$'), receive_info)],
            SUBCATEGORY: [MessageHandler(Filters.regex('^Instagram$'), insta),
                          MessageHandler(Filters.regex('^Spotify$'), spot),
                          MessageHandler(Filters.regex('^Soundcloud$'), sound_cloud),
                          MessageHandler(Filters.regex('^Back$'), rept),
                          MessageHandler(Filters.regex('^Cart$'), receive_info)],
            PRODUCT: [MessageHandler(Filters.regex('^Likes$'), insta_like),
                      MessageHandler(Filters.regex('^Followers$'), insta_foll),
                      MessageHandler(Filters.regex('^Back$'), repeat),
                      MessageHandler(Filters.regex('^Cart$'), receive_info)],
            FINAL: [MessageHandler(Filters.photo | Filters.regex('^Instagram Likes | 1000 For 3$ | Lifetime Warranty '
                                                                 '[$3-30]$'),
                                   insta_fin),
                    MessageHandler(Filters.regex('^Back$'), rpeat),
                    MessageHandler(Filters.regex('^Cart$'), receive_info),
                    CallbackQueryHandler(button)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
