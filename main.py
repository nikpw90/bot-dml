import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]

pics = {
    "pic1": 'dragon.png',
    "fireinfo": 'fire element.jpg' ,
    "windinfo" : 'wind element.jpg',
    "earthinfo" : 'earth element.jpg',
    "waterinfo" : 'water element.jpg',
    "plantinfo" : 'plant element.jpg',
    "metalinfo" : 'metal element.jpg',
    "energyinfo" : 'energy element.jpg',
    "voidinfo" : 'void element.jpg',
    "lightinfo" : 'light element.jpg',
    "shadowinfo" : 'shadow element.jpg',
    "fabledinfo" : 'fabled element.jpg',
    "primalinfo" : 'primal element.jpg',
    "divineinfo" : 'divine element.jpg',
    "ancientinfo" : 'ancient element.jpg',
    "tyrantinfo" : 'tyrant element.jpg',
    "prisminfo" : 'prism element.jpg',
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("привіт")

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Список картинок:\n" + "\n".join([f"/{cmd}" for cmd in pics])
    await update.message.reply_text(text)

async def send_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text[1:]
    path = pics.get(name)
    if path and os.path.exists(path):
        with open(path, 'rb') as img:
            await update.message.reply_photo(img)
    else:
        await update.message.reply_text("картинка не знайдена")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("commands", commands))
    for cmd in pics:
        app.add_handler(CommandHandler(cmd, send_pic))
    app.run_polling()

if __name__ == "__main__":
    main()


