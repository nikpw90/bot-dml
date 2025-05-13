import json  # Import JSON for saving and loading subscription data
import asyncio  # Import asyncio for delay functionality
from telegram import Update, Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, MessageHandler, CallbackQueryHandler, filters

# Replace with your bot token
BOT_TOKEN = "7795138996:AAHAI8AXDEP9aX6uTm4yXXS1XwzW-v5iN2U"

# Replace with your Telegram user ID
ADMIN_ID = 5503857768  # Replace with your actual Telegram user ID

# File to store subscription data
SUBSCRIPTION_FILE = "subscriptions.json"

# Sets to store user and group chat IDs
users = set()
groups = set()

def load_subscriptions():
    """Load subscriptions from a JSON file."""
    global users, groups
    try:
        with open(SUBSCRIPTION_FILE, "r") as file:
            data = json.load(file)
            users = set(data.get("users", []))
            groups = set(data.get("groups", []))
    except FileNotFoundError:
        # If the file doesn't exist, start with empty sets
        users = set()
        groups = set()

def save_subscriptions():
    """Save subscriptions to a JSON file."""
    with open(SUBSCRIPTION_FILE, "w") as file:
        json.dump({"users": list(users), "groups": list(groups)}, file)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'подписка' command to subscribe users or groups."""
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if chat.id in users:
            # User is already subscribed
            response = await update.message.reply_text("Вы уже подписаны.")
            await asyncio.sleep(3)  # Wait for 3 seconds
            await update.message.delete()  # Delete the user's message
            await response.delete()  # Delete the bot's response
        else:
            users.add(chat.id)
            save_subscriptions()  # Save updated subscriptions
            await update.message.reply_text("Вы подписались на бота. Теперь вы будете получать сообщения от него.")
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if chat.id in groups:
            # Group is already subscribed
            response = await update.message.reply_text("Группа уже подписана.")
            await asyncio.sleep(3)  # Wait for 3 seconds
            await update.message.delete()  # Delete the user's message
            await response.delete()  # Delete the bot's response
        else:
            groups.add(chat.id)
            save_subscriptions()  # Save updated subscriptions
            await update.message.reply_text("Группа подписалась на бота. Теперь участники будут получать сообщения от него.")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'отписка' command to unsubscribe users or groups."""
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if chat.id not in users:
            # User is already unsubscribed
            response = await update.message.reply_text("Вы не подписаны.")
            await asyncio.sleep(3)  # Wait for 3 seconds
            await update.message.delete()  # Delete the user's message
            await response.delete()  # Delete the bot's response
        else:
            users.discard(chat.id)
            save_subscriptions()  # Save updated subscriptions
            await update.message.reply_text("Вы отписались от бота.")
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if chat.id not in groups:
            # Group is already unsubscribed
            response = await update.message.reply_text("Группа не подписана.")
            await asyncio.sleep(3)  # Wait for 3 seconds
            await update.message.delete()  # Delete the user's message
            await response.delete()  # Delete the bot's response
        else:
            groups.discard(chat.id)
            save_subscriptions()  # Save updated subscriptions
            await update.message.reply_text("Группа отписалась от бота.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()
    if query.data == "pass_message" and query.from_user.id == ADMIN_ID:
        await query.message.reply_text("Отправь мне сообщение, фото, видео, стикер или GIF, которое нужно разослать всем пользователям и группам, подписанным на бота.")
        context.user_data["awaiting_broadcast"] = True
    elif query.data == "delete_panel" and query.from_user.id == ADMIN_ID:
        # Delete the admin panel message
        await query.message.delete()

async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the message to be broadcasted after the admin presses the button."""
    if update.effective_user.id != ADMIN_ID or not context.user_data.get("awaiting_broadcast"):
        return  # Ignore messages from non-admin users or if not awaiting a broadcast message

    context.user_data["awaiting_broadcast"] = False  # Reset the flag

    # Broadcast to individual users
    for user_id in users:
        if user_id == ADMIN_ID:
            continue  # Skip sending the message back to the admin's private chat
        try:
            await context.bot.copy_message(chat_id=user_id, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        except Exception as e:
            print(f"Не удалось прислать сообщение пользователю: {user_id}: {e}")

    # Broadcast to groups
    for group_id in groups:
        try:
            await context.bot.copy_message(chat_id=group_id, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
        except Exception as e:
            print(f"Не удалось прислать сообщение группе: {group_id}: {e}")

    # Send confirmation message to the admin
    await update.message.reply_text("Сообщение успешно разослано всем подписанным пользователям и группам.")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the admin panel when the admin sends 'админ'."""
    if update.effective_user.id == ADMIN_ID and update.effective_chat.type == Chat.PRIVATE:
        keyboard = [
            [InlineKeyboardButton("Разослать сообщение", callback_data="pass_message")],
            [InlineKeyboardButton("Удалить", callback_data="delete_panel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Команды админа:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Вы не администратор. Доступ к этой команде только у администратора.")

def main() -> None:
    """Start the bot."""
    # Load subscriptions from file
    load_subscriptions()

    application = Application.builder().token(BOT_TOKEN).build()

    # Message handlers
    application.add_handler(MessageHandler(filters.Regex(r"^подписка$"), subscribe))  # Match only the exact word "подписка"
    application.add_handler(MessageHandler(filters.Regex(r"^отписка$"), unsubscribe))  # Match only the exact word "отписка"
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Text("админ") & filters.ChatType.PRIVATE, admin_panel))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_broadcast_message))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()