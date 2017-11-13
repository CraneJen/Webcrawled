from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from so import so
import os


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def _start(bot, update):
    update.message.reply_text('请输入电话号码！')


def _help(bot, update):
    update.message.reply_text('输入电话号码，查询是否骚扰电话！')


def _search(bot, update):
    phoneNum = update.message.text
    result = so(phoneNum)
    if len(phoneNum) == 11 or len(phoneNum) == 12:
        text = "{}： {}".format(phoneNum, result)
        logger.info('{}: {}'.format(phoneNum, result))
    else:
        text = "输入字数不够！！"
    update.message.reply_text(text)


def _error(bot, update, error):
    logger.warning('Update "{}" caused error "{}"'.format(update, error))


def main():

    token = os.environ['TOKEN']
    updater = Updater(token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", _start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(Filters.text, _search))
    dp.add_error_handler(_error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
