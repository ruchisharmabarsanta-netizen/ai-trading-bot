from telegram.ext import (
    Application,
    CommandHandler
)

from paper_trader import (
    get_stats
)

BOT_TOKEN = "YOUR_TOKEN"


async def stats_command(
    update,
    context
):

    stats = get_stats()

    await update.message.reply_text(
        stats
    )


app = Application.builder().token(
    BOT_TOKEN
).build()

app.add_handler(
    CommandHandler(
        "stats",
        stats_command
    )
)

print("Telegram Commands Running...")

app.run_polling()