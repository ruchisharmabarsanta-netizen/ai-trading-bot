import asyncio

from telegram import Bot


BOT_TOKEN = "8831168547:AAFAFvDlkwK_XIn8DpaiTlaqQcoB14wHevs"

CHAT_ID = "5155739109"


async def send_message(message):

    bot = Bot(token=BOT_TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )


def send_telegram_alert(message):

    try:

        asyncio.run(
            send_message(message)
        )

        print(
            "\nTELEGRAM ALERT SENT"
        )

    except Exception as e:

        print(
            "\nTELEGRAM ERROR"
        )

        print(e)