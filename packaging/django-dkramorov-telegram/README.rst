========
Telegram
========

Telegram is a simple Django for send message to Telegram chats

Quick start
-----------

1. Add "telegram" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'telegram',
    ]

2. Add settings for telegram::

    TELEGRAM_TOKEN = env('TELEGRAM_TOKEN', default='')
    TELEGRAM_PROXY = env('TELEGRAM_PROXY', default='')
    TELEGRAM_CHAT_ID = env('TELEGRAM_CHAT_ID', default=0)
    TELEGRAM_ENABLED = env('TELEGRAM_ENABLED', cast=bool, default=False)

3. Create bot over father's bot, insert bot token in TELEGRAM_TOKEN
then create telegram group and add your bot to it,
send message to your new group with bot, receive TELEGRAM_CHAT_ID with command:

python manage.py telegram_get_updates

4. Test send message

python manage.py telegram_send_test_message


