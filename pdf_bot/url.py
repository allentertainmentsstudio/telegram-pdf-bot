import logging
import os
import tempfile

from telegram.ext.dispatcher import run_async
from urllib.parse import urlparse
from weasyprint import HTML
from weasyprint.urls import URLFetchingError

from pdf_bot.utils import send_result_file
from pdf_bot.language import set_lang

URLS = 'urls'
logging.getLogger('weasyprint').setLevel(100)


@run_async
def url_to_pdf(update, context):
    _ = set_lang(update, context)
    message = update.effective_message
    url = message.text
    user_data = context.user_data

    if user_data is not None and URLS in user_data and url in user_data[URLS]:
    message.reply_text(_(
        "⚠️ *Conversion Already In Progress*\n\n"
        "You've already submitted this webpage for conversion.\n"
        "Please wait while I complete the current processing task."
    ))
else:
    message.reply_text(_(
    "🌐 *Webpage Conversion Started*\n\n"
    "Your webpage is being processed and converted into a high-quality PDF document.\n"
    "Please wait a moment while I prepare your file..."
))

if URLS in user_data:
    user_data[URLS].add(url)
else:
            user_data[URLS] = {url}

        with tempfile.TemporaryDirectory() as dir_name:
            out_fn = os.path.join(dir_name, f'{urlparse(url).netloc}.pdf')
            try:
                HTML(url=url).write_pdf(out_fn)
                send_result_file(update, context, out_fn, 'url')
            except URLFetchingError:
                message.reply_text(_('Unable to reach your web page'))

        user_data[URLS].remove(url)
