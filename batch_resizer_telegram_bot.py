#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import io
import batch_resizer
import batch_resizer_config_helper
import os
from PIL import Image
import tempfile
import uuid
from zipfile import ZipFile
import shutil
import configparser

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Default sizes.
image_sizes = []

# Handlers

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! Please send an uncompressed image for batch resizing.')


def help(update, context):
    """Send a message when the command /help is issued."""
    help_text = '''
    Please send an uncompressed image for batch resizing.
    '''
    update.message.reply_text(help_text)


def handle_file(update, context):
    uploaded_file = update.message.document.get_file()
    url = uploaded_file.file_path
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))

    temp_dir = tempfile.gettempdir()
    uid = str(uuid.uuid4())
    target_path = os.path.join(temp_dir, uid)
    os.mkdir(target_path)

    update.message.reply_text('Please wait while the image is being processed...')

    success = batch_resizer.batch_resize_image(img, target_path, image_sizes,
                                     resample=Image.BICUBIC, max_size_kilobytes=95, max_quality=95, min_quality=1)

    if not success:
        update.message.reply_text('Procedure failed!')

    zip_path = os.path.join(target_path, 'batch_resize.zip')
    with ZipFile(zip_path, 'w') as zip:
        # writing each file one by one
        for f in os.listdir(target_path):
            if (f.endswith('.' + "jpg")):
                zip.write(os.path.join(target_path, f), f)

    context.bot.send_document(chat_id=update.message.chat_id,
                           document=open(zip_path, 'rb'))

    shutil.rmtree(target_path)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    # restrict bot for spesific users.
    username = cfg["telegram_bot"]["Usernames"].split(",")
    # read the api token.
    api_token = cfg["telegram_bot"]["ApiToken"]
    # read image sizes
    sizes_text = cfg["DEFAULT"]["ImageSizes"]
    image_sizes.extend(batch_resizer_config_helper.parse_image_sizes(sizes_text))

    # create the Updater and pass it your bot's token.
    # make sure to set use_context=True to use the new context based callbacks
    # post version 12 this will no longer be necessary
    updater = Updater(
        api_token, use_context=True)

    # get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # handle file uploads.
    dp.add_handler(MessageHandler(Filters.document & Filters.user(username=username), handle_file))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
