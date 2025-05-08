import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, PicklePersistence

# Use environment variable for the token
TOKEN = os.getenv("BOT_TOKEN")
#TOKEN = '7833602107:AAHVVCVRfcTkVRLvi7V9fOcQaYnXBQs47MY'

# Define folders with custom names and pictures
FOLDERS = {
    "buildings": {
        "display_name": "Buildings Info",
        "path": "buildings",
        "pictures": {
            "academy": "Academrg",
            "enchantmentaltar": "Enchantment Altar",
            "ancientportal": "Ancient Portal",
            "breedingden": "Dragon Market",
            "eternalfruittree": "Eternal Fruit Tree",
            "goldvault": "Gold Vault",
            "clanfortress": "Clan Fortress",
            "hatchery": "Hatchery",
            "lighthouse": "Lighthouse",
            "dragonvault": "Dragon Vault",
            "totemfriendship": "Totem of Friendship",
            "farm": "Farm",
            "fontainyouth": "Fountain of Youth",
            "firetample": "Temple of Fire",
            "windtample": "Temple of Wind",
            "earthtample": "Temple of Earth",
            "watertample": "Temple of Water",
            "planttample": "Temple of Plant",
            "energytample": "Temple of Energy",
            "metaltample": "Temple of Metal",
            "voidtample": "Temple of Void",
            "lighttample": "Temple of Light",
            "shadowtample": "Temple of Shadow",
            "fabledtample": "Temple of Fabled"
        }
    },
    "dragonbreeding": {
        "display_name": "Basic information about dragon breeding",
        "path": "dragonbreeding",
        "pictures": {
            "basics": "Basics of dragon Breeding",
            "threeelements": "Three elements dragons breeding",
            "fabled": "fabled dragons breeding",
            "vipdragons": "VIP dragons breeding",
            "enchantedbreeding": "Enchanted breeding",
            "ovddragons": "Ovd dragons",
            "ovdbreeding": "Ovd breeding"    
        }
    },
    "elementsinfo": {
        "display_name": "Elements Info",
        "path": "elementsinfo",
        "pictures": {
            "basestat": "basestats calculation",
            "teamelementsbase": "basic elements of the team",
            "teamelements": "elements of the team",
            "otherp1": "other details: ancient element",
            "otherp2": "other details: divine element",
            "fireelement": "Fire Element Card",
            "windelement": "Wind Element Card",
            "earthelement": "Earth Element Card",
            "waterelement": "Water Element Card",
            "plantelement": "Plant Element Card",
            "metalelement": "Metal Element Card",
            "energyelement": "Energy Element Card",
            "voidelement": "Void Element Card",
            "lightelement": "Light Element Card",
            "shadowelement": "Shadow Element Card",
            "fabledelement": "Fabled Element Card",
            "primalelement": "Primal Element Card",
            "divineelement": "Divine Element Card",
            "ancientelement": "Ancient Element Card",
            "tyrantelement": "Mythic Element Card",
            "prismelement": "Prism Element Card"
        }
    },
    "eventsguides": {
        "display_name": "Guides for Events",
        "path": "eventsguides",
        "pictures": {
            "treasurehunt": "Primal Event - Treasure Hunt",
            "castlep1": "Divine castle event - part 1",
            "castlep2": "Divine castle event - part 2",
            "cakecraze": "Winter Carnival",
            "dragonboardp1": "Dragon Board - part 1",
            "dragonboardp2": "Dragon Board - part 2",
            "talismans": "action talismans",
            "shop": "shop"
        }
    },
    "habitats": {
        "display_name": "Habitats information",
        "path": "habitats",
        "pictures": {
            "habitatnum": "number of habitats",
            "habitatnumperlvl": "number of habitats per level",
            "firehabitat": "fire habitat",
            "windhabitat": "wind habitat",
            "earthehabitat": "earth habitat",
            "waterhabitat": "water habitat",
            "planthabitat": "plant habitat",
            "metalhabitat": "metal habitat",
            "energyhabitat": "energy habitat",
            "voidhabitat": "void habitat",
            "lighthabitat": "light habitat",
            "shadowhabitat": "shadow habitat",
            "fabledhabitat": "fabled habitat",
            "divinehabitat": "divine habitat",
            "ancienthabitat": "ancient habitat",
            "tyranthabitat": "tyrant habitat",
            "prismhabitat": "prism habitat",
            "dragonlimp": "dragon limp habitat",
            "bosshabitat": "boss habitat",
            "talesmegabitat": "tales mega habitat",
            "majicgrotmegabitat": "majicgrot mega habitat",
            "fruittree": "fruit tree habitat",
            "timehabitat": "time habitat",
            "celebrationmegabitat": "celebration mega habitat",
            "zodiachabitat": "zodiac habitat",
            "primalhabitat": "primal habitat",
            "beachhabitat": "beach habitat",
            "snowyhabitat": "snowy habitat",
            "lovehabitat": "love habitat",
            "heloweenhabitat": "heloween habitat",
            "usahabitat": "usa habitat",
            "icehabitat": "ice habitat",
            "wintercelebrationhabitat": "winter celebration habitat",
            "ghosthabitat": "ghost habitat",
            "celebrationhabitat": "celebration habitat",
            "househabitat": "house habitat",
            "autumnhabitat": "autumn habitat",
            "wintermegabitat": "winter mega habitat",
            "calmhabitat": "calm habitat"
        }
    },
    "islandsandruins": {
        "display_name": "Information about each island and ruins",
        "path": "islandsandruins",
        "pictures": {
            "optplacement": "best placement",
            "island1": "-",
            "island2": "-",
            "island3": "-",
            "island4": "-",          
            "island5": "-",
            "island6": "-",
            "island7": "-",
            "island8": "-",
            "island9": "-",
            "island10": "-",
            "dungeoun1": "-",
            "dungeoun2": "-",
            "dungeoun3": "-",
            "island12": "-",
            "island13": "-",
            "ruinexp": "-",
            "ruin1": "-",
            "ruin2": "-",
            "ruin3": "-",           
            "ruin4": "-",   
            "ruin5": "-",
            "ruin6": "-",
            "przes": "-",
            "dragonlimp": "-",
            "dragonlimp2": "-",
            "dragonlimp3": "-"
        }
    },
    "other": {
        "display_name": "Other",
        "path": "other",
        "pictures": {
            "academycost": "Academy Training Cost",
            "difffood": "Difference between food",
            "enchantment": "Enchantment",
            "foodperlvl": "Food per level",
            "viplvlcost": "VIP Level Cost",
            "daystillvip": "Amount of days till VIP"
        }
    },
    "sigilsmaster": {
        "display_name": "Sigils Master",
        "path": "sigilsmaster",
        "pictures": {
            "sigilsdef": "definition of sigils",
            "synergies": "synergies",
            "sigilseffects1": "sigils effects part1",
            "sigilseffects2": "sigils effects part2",
            "sigilseffects3": "sigils effects part3",
            "whatsigils1": "what sigils p1",
            "whatsigils2": "what sigils p2",
            "whatsigils3": "what sigils p3",
            "whatsigils4": "what sigils p4",
            "calc1": "calculation of sigils p1",
            "calc2": "calculation of sigils p2",
            "calc3": "calculation of sigils p3",
            "calc4": "calculation of sigils p4"
        }
    }
}

# Helper function to arrange buttons dynamically
def arrange_buttons(buttons, max_columns=5):
    """
    Arrange buttons into rows with a specified maximum number of columns.
    """
    keyboard = []
    for i in range(0, len(buttons), max_columns):
        keyboard.append(buttons[i:i + max_columns])
    return keyboard

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я ваш бот. Використовуйте /commands для перегляду доступних команд.")

# Callback handler for deleting messages
async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        # Delete the bot's message
        bot_message_id = context.user_data.get("bot_message_id")
        if bot_message_id:
            await query.message.delete()

        # Delete the user's message
        user_message_id = context.user_data.get("user_message_id")
        if user_message_id:
            await query.message.chat.delete_message(user_message_id)
    except Exception as e:
        print(f"Error deleting messages: {e}")

# /commands handler: shows folder-level commands with buttons
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Here are all your folders:\n"
    buttons = []

    for idx, (folder_key, folder_data) in enumerate(FOLDERS.items(), start=1):
        # Only display the folder name without the description or "-"
        text += f"{idx}. {folder_data['display_name']}\n"
        buttons.append(InlineKeyboardButton(str(idx), callback_data=f"folder_{folder_key}"))

    # Arrange buttons dynamically into rows
    keyboard = arrange_buttons(buttons, max_columns=5)

    # Add a "Delete Message" button in a separate row
    keyboard.append([InlineKeyboardButton("❌ Clear Chat", callback_data="delete_message")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot_message = await update.message.reply_text(text, reply_markup=reply_markup)
    context.user_data["user_message_id"] = update.message.message_id
    context.user_data["bot_message_id"] = bot_message.message_id

# Callback handler for folder selection
async def folder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    folder_key = query.data.split("_")[1]
    if folder_key not in FOLDERS:
        await query.edit_message_text("Folder not found.")
        return

    folder_data = FOLDERS[folder_key]
    pictures = folder_data.get("pictures", {})

    if not pictures:
        await query.edit_message_text(f"The folder '{folder_data['display_name']}' is empty.")
        return

    text = f"You selected '{folder_data['display_name']}'.\nHere are the pictures:\n"
    buttons = []

    for idx, (file_name, custom_name) in enumerate(pictures.items(), start=1):
        text += f"{idx}. {custom_name}\n"
        buttons.append(InlineKeyboardButton(str(idx), callback_data=f"picture_{folder_key}_{file_name}"))

    # Arrange buttons dynamically into rows
    keyboard = arrange_buttons(buttons, max_columns=5)

    # Add a "Go Back" button and a "Delete Message" button in separate rows
    keyboard.append([InlineKeyboardButton("⬅️ Back to Folders", callback_data="back_to_folders")])
    keyboard.append([InlineKeyboardButton("❌ Clear Chat", callback_data="delete_message")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# Callback handler for picture selection
async def picture_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, folder_key, file_name = query.data.split("_")
    folder_data = FOLDERS.get(folder_key)
    if not folder_data:
        await query.edit_message_text("Folder not found.")
        return

    folder_path = folder_data["path"]
    file_path = os.path.join(folder_path, f"{file_name}.jpg")  # Assuming all files are .jpg

    if not os.path.exists(file_path):
        await query.edit_message_text("Picture not found.")
        return

    with open(file_path, "rb") as photo:
        await query.message.reply_photo(photo)

# Callback handler for "Go Back" button
async def back_to_folders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Reuse the /commands logic to display the list of folders
    text = "Here are all your folders:\n"
    buttons = []

    for idx, (folder_key, folder_data) in enumerate(FOLDERS.items(), start=1):
        # Only display the folder name without the description or "-"
        text += f"{idx}. {folder_data['display_name']}\n"
        buttons.append(InlineKeyboardButton(str(idx), callback_data=f"folder_{folder_key}"))

    # Arrange buttons dynamically into rows
    keyboard = arrange_buttons(buttons, max_columns=5)

    # Add a "Delete Message" button in a separate row
    keyboard.append([InlineKeyboardButton("❌ Clear Chat", callback_data="delete_message")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# Run the bot
def main():
    # Enable persistence for user_data
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("commands", commands))
    app.add_handler(CallbackQueryHandler(folder_callback, pattern="^folder_"))
    app.add_handler(CallbackQueryHandler(picture_callback, pattern="^picture_"))
    app.add_handler(CallbackQueryHandler(back_to_folders, pattern="^back_to_folders$"))
    app.add_handler(CallbackQueryHandler(delete_message, pattern="^delete_message$"))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()