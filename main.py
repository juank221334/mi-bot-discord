from ticket_bot import bot
import os

bot.run(os.getenv("DISCORD_TOKEN"))
