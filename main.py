import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, PicklePersistence, MessageHandler, filters
from datetime import datetime, timedelta

TOKEN = '7833602107:AAHVVCVRfcTkVRLvi7V9fOcQaYnXBQs47MY'

WEBHOOK_URL = "https://nax90.pythonanywhere.com"

# Define folders with custom names and pictures
FOLDERS = {
    "buildings": {
        "display_name": "Здания",
        "path": "buildings",
        "pictures": {
            "academy": "Академия драконов",
            "enchantmentaltar": "Алтарь колдовства",
            "ancientportal": "Древний портал",
            "breedingden": "Гнездовье",
            "eternalfruittree": "Вечное фруктовое дерево (ВФД)",
            "goldvault": "Золотойхранилище",
            "clanfortress": "Крепость клана",
            "hatchery": "Инкубатор",
            "lighthouse": "Маяк",
            "dragonvault": "Пансионат драконов",
            "totemfriendship": "Тотем дружбы",
            "farm": "Фермы",
            "fontainyouth": "Фонтан молодости",
            "firetample": "Храм Огня",
            "windtample": "Храм Ветра",
            "earthtample": "Храм Земли",
            "watertample": "Храм Воды",
            "planttample": "Храм Зелени",
            "energytample": "Храм Энергии",
            "metaltample": "Храм Металла",
            "voidtample": "Храм Пустоты",
            "lighttample": "Храм Света",
            "shadowtample": "Храм Тени",
            "fabledtample": "Храм Прославленных"
        }
    },
    "dragonbreeding": {
        "display_name": "Разведение драконов (Общая информация)",
        "path": "dragonbreeding",
        "pictures": {
            "basics": "Основы",
            "threeelements": "Выведение трёхстихийных драконов",
            "fabled": "Выведение магазинных прославленных драконов",
            "vipdragons": "Выведение VIP драконов",
            "enchantedbreeding": "Колдовское разведение",
            "ovddragons": "ОВД драконы",
            "ovdbreeding": "ОВД разведение"    
        }
    },
    "elementsinfo": {
        "display_name": "Мастер Элементов",
        "path": "elementsinfo",
        "pictures": {
            "basestat": "Расчёт базовых характеристик драконов по стихиям",
            "teamelementsbase": "Элементы отряда",
            "teamelements": "Комбинации элементов в отряде",
            "otherp1": "Прочие нюансы Часть 1 (Древняя стихия)",
            "otherp2": "Прочие нюансы Часть 2 (Божественная стихия)",
            "weakandstrongattacks": "Слабые и сильные атаки каждой стихии",
            "fireelement": "Огонь",
            "windelement": "Ветер",
            "earthelement": "Земля",
            "waterelement": "Вода",
            "plantelement": "Зелень",
            "metalelement": "Металл",
            "energyelement": "Энергия",
            "voidelement": "Пустота",
            "lightelement": "Свет",
            "shadowelement": "Тень",
            "fabledelement": "Прославленный",
            "primalelement": "Первородная",
            "divineelement": "Божество",
            "ancientelement": "Древняя",
            "tyrantelement": "Тиран",
            "prismelement": "Призма"
        }
    },
    "eventsguides": {
        "display_name": "Гайды на акции",
        "path": "eventsguides",
        "pictures": {
            "treasurehunt": "Охота за сокровищами",
            "castlep1": "Замок Часть 1 (Инфо об акции)",
            "castlep2": "Замок Часть 2 (Сбор еды и Выведение дракона)",
            "cakecraze": "Кулинарное безумие",
            "dragonboardp1": "Драконья доска Часть 1",
            "dragonboardp2": "Драконья доска Часть 2",
            "talismans": "Драконья доска (Камни и Талисманы)",
            "shop": "Драконья доска (Магазин)"
        }
    },
    "habitats": {
        "display_name": "Жилища",
        "path": "habitats",
        "pictures": {
            "habitatnum": "Количество жилищ",
            "habitatnumperlvl": "Количество жилищ по уровням игрока",
            "firehabitat": "Жилище Огня",
            "windhabitat": "Жилище Ветра",
            "earthhabitat": "Жилище Земли",
            "waterhabitat": "Жилище Воды",
            "planthabitat": "Жилище Зелени",
            "metalhabitat": "Жилище Металла",
            "energyhabitat": "Жилище Энергии",
            "voidhabitat": "Жилище Пустоты",
            "lighthabitat": "Жилище Света",
            "shadowhabitat": "Жилище Тени",
            "fabledhabitat": "Жилище Прославленных",
            "divinehabitat": "Жилище Богов",
            "ancienthabitat": "Жилище Древних",
            "tyranthabitat": "Жилище Тиранов",
            "prismhabitat": "Жилище Призмы",
            "dragonlimp": "Благословенный Вседраконий Стадион",
            "bosshabitat": "Жилище Боссов",
            "talesmegabitat": "Сказочное Мегажилище",
            "majicgrotmegabitat": "Мегажилище Волшебный Грот",
            "fruittree": "Вечное Фруктовое Дерево (ВФД)",
            "timehabitat": "Жилище Времени",
            "celebrationmegabitat": "Именное Мегажилище",
            "zodiachabitat": "Жилище Зодиака",
            "primalhabitat": "Обитель Первородных",
            "beachhabitat": "Пляжный Домик",
            "snowyhabitat": "Заснеженное Жилище",
            "lovehabitat": "Жилище Любви",
            "heloweenhabitat": "Жуткое Жилище",
            "usahabitat": "Звездно-Полосатое Жилище",
            "icehabitat": "Леденцовое Жилище",
            "wintercelebrationhabitat": "Праздничное Жилище(Зима)",
            "ghosthabitat": "Призрачное Жилище",
            "celebrationhabitat": "Праздничное Жилище",
            "househabitat": "Пряничный Домик",  
            "autumnhabitat": "Жилище Даров Осени",
            "wintermegabitat": "Мегажилище Зимняя Ярмарка",
            "calmhabitat": "Жилище Тихий Пруд"
        }
    },
    "islandsandruins": {
        "display_name": "Острова и руины",
        "path": "islandsandruins",
        "pictures": {
            "optplacement": "Оптимальное расположение посроек на островах",
            "island1": "Стартовый остров(1)",
            "island2": "Болотный остров(2)",
            "island3": "Угасающая земля(3)",
            "island4": "Затерянный мир(4)",          
            "island5": "Остров Магма(5)",
            "island6": "Черепаший остров",
            "island7": "Сад спокойствия",
            "island8": "Северный скалистый",
            "island9": "Остров малышей",
            "island10": "Мистические высоты",
            "dungeoun1": "Плато темницы(1)",
            "dungeoun2": "Грот Отто(2)",
            "dungeoun3": "Паровые поля(3)",
            "island12": "Остров алмазов(Донат)",
            "island13": "Раскалённый остров(Донат)",
            "ruinexp": "Очки ОП руин",
            "ruin1": "Мистическая пещера(1)",
            "ruin2": "Призрачный корабль",
            "ruin3": "Огненные топи(2)",           
            "ruin4": "Врата черепа(3)",   
            "ruin5": "Древний чертог(4)",
            "ruin6": "Месторождение магмы(5)",
            "przes": "Награды руин",
            "dragonlimp": "Благословенный Вседраконий Остров(Целый)",
            "dragonlimp2": "Благословенный Вседраконий Остров(Верхняя часть)",
            "dragonlimp3": "Благословенный Вседраконий Остров(Нижняя часть)"
        }
    },
    "other": {
        "display_name": "Прочие таблицы",
        "path": "other",
        "pictures": {
            "academycost": "Цена обучения разных стихий в академии",
            "difffood": "Сравнение разных видов еды с ферм",
            "enchantment": "Колдовство драконов",
            "foodperlvl": "Количество еды в зависимости от уровня дракона",
            "viplvlcost": "Стоимость VIP уровней в VIP очках)",
            "daystillvip": "Количество дней до n-ого VIP уровня"
        }
    },
    "sigilsmaster": {
        "display_name": "Мастер Символов",
        "path": "sigilsmaster",
        "pictures": {
            "sigilsdef": "Что такое символы?",
            "synergies": "Сингергии",
            "sigilseffects1": "Эффекты символов(Школа Роста)",
            "sigilseffects2": "Эффекты символов(Школа Силы)",
            "sigilseffects3": "Эффекты символов(Школа Гостеприимства)",
            "whatsigils1": "Кому какие символы ставить?",
            "whatsigils2": "Кому какие символы ставить? (чудо,принятие,колдовство)",
            "whatsigils3": "Кому какие символы ставить? (символы для иксов в темнице)",
            "whatsigils4": "Кому какие символы ставить? (прочие символы)",
            "calc1": "Рассчёт силы умения (1)",
            "calc2": "Рассчёт силы умения (2)",
            "calc3": "Рассчёт силы умения (3)",
            "calc4": "Рассчёт силы умения (4)"
        }
    },
    "dungeoun": {
        "display_name": "Темница(Команды, пулы и слабые атаки)",
        "path": "dungeoun",
        "pictures": {
            "jopa": "Цикл Жопы",
            "50ko": "Слабые атаки каждого пула (50ko)",
            "weakattacks": "Слабые атаки каждой стихии"
            
        },
        "subfolders": {
            "pools": {
                "display_name": "Пулы",
                "path": "dungeoun/pools",
                "pictures": {
                    "1": "Пул 1",
                    "2": "Пул 2",
                    "3": "Пул 3",
                    "4": "Пул 4",
                    "5": "Пул 5",
                    "6": "Пул 6",
                    "7": "Пул 7",
                    "8": "Пул 8"
                }
            },
            "dragucci": {
                "display_name": "Драгучи",
                "path": "dungeoun/dragucci",
                "pictures": {
                    "a": "Драгучи Часть 1",
                    "b": "Драгучи Часть 1",
                    "c": "Драгучи Часть 1",
                    "d": "Драгучи Часть 1",
                    "e": "Драгучи Часть 1",
                    "f": "Драгучи Часть 1",
                    "g": "Драгучи Часть 1",
                    "h": "Драгучи Часть 1",
                    "i": "Драгучи Часть 1",
                    "j": "Драгучи Часть 1",
                    "k": "Драгучи Часть 2",
                    "l": "Драгучи Часть 2",
                    "m": "Драгучи Часть 2",
                    "n": "Драгучи Часть 2",
                    "o": "Драгучи Часть 2"
                }
            }
        }
    }
}

# Define sticker packs with custom names and corresponding sticker IDs
STICKERS = {
    "tyrantdragons": {
        "display_name": "Драконы Тираны",
        "sticker_id": "CAACAgIAAxkBAfuJAWgd4r6AUoaGVN1MNO8TbBVDx2BuAAIOTAACPTfhSOXCEO_QPxk2NgQ"
    },
    "ancientdragons": {
        "display_name": "Древние Драконы",
        "sticker_id": "CAACAgIAAxkBAfuLBmgd5ehDbpUZyME6aYadg6prMHD0AAKaPgACk__hSCvUTwaILGAxNgQ"
    },
    "divinedragons": {
        "display_name": "Божественные Драконы",
        "sticker_id": "CAACAgIAAxkBAfuLDGgd5fu7PWxTfO8na630puxZrF5EAAJFSAACfFHgSAVEG_aWNb9rNgQ"
    },
    "primaldragons": {
        "display_name": "Первородные драконы",
        "sticker_id": "CAACAgIAAxkBAfuLFmgd5ghCAZUkqx5YKuEhuMfkcAN7AALEZwACg_n5SkMUY9g5yRLbNgQ"
    },
    "babydragons": {
        "display_name": "Детские формы драконов",
        "sticker_id": "CAACAgQAAxkBAfuLHWgd5iBGmVJXquv7deCLQzV6aK-MAALwGAAC_1IxUPhXXHHQLZ3lNgQ"
    },
    "dmlstickers": {
        "display_name": "DML for DragonUnion",
        "sticker_id": "CAACAgIAAxkBAfuLNGgd5kc4u2NVniPR2GNsG9KImEAXAAIWKwACU-64SilqLHumbZ10NgQ"
    },
    "legendstickers": {
        "display_name": "Стикеры Легенды Дракономании",
        "sticker_id": "CAACAgIAAxkBAfuLRGgd5nJZWagM15-H6h2_rzcCPuCmAAIVAANGxtgNRagtn3Ps_xA2BA"
    },
    "prikol": {
        "display_name": "Дракономания с приколами",
        "sticker_id": "CAACAgIAAxkBAfuMLGgd6DwP9XEPUKwJK-GfUfZd0siKAAIzYAAC4M-YSe2_q-wZG39ONgQ"
    },
    "eutistic": {
        "display_name": "Легенды аутиста",
        "sticker_id": "CAACAgIAAxkBAfuMb2gd6PTRzhXV9Q0gHAiAcX8vh69wAAL5XAACn3hISpW-XY-Aa8R3NgQ"
    }
}

# Helper function to arrange buttons dynamically
def arrange_buttons(buttons, max_columns=5, back_button=None, delete_button=None):
    """
    Arrange buttons into rows with a specified maximum number of columns.
    Optionally, add "⬅️ Назад" and "❌ Удалить" buttons as a separate row at the bottom.
    """
    keyboard = []
    for i in range(0, len(buttons), max_columns):
        keyboard.append(buttons[i:i + max_columns])

    # Add "⬅️ Назад" and "❌ Удалить" buttons as a separate row
    if back_button and delete_button:
        keyboard.append([back_button, delete_button])

    return keyboard

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я ДМЛ бот который поможет найти необходимую информацию с легкостью. \n"
        "Используйте /commands чтобы открыть главное меню."
    )

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
        print(f"Error: {e}")

# /commands handler: main menu
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Выберите опцию:\n1. Список карточек\n2. Список стикеров\n3. Полезные ссылки/статьи"
    buttons = [
        InlineKeyboardButton("1", callback_data="main_cards"),
        InlineKeyboardButton("2", callback_data="main_stickers"),
        InlineKeyboardButton("3", callback_data="useful_links"),  # Correct callback data
        InlineKeyboardButton("❌ Удалить", callback_data="delete_message")
    ]

    # Arrange buttons into rows
    keyboard = arrange_buttons(buttons, max_columns=3)
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot_message = await update.message.reply_text(text, reply_markup=reply_markup)
    context.user_data["user_message_id"] = update.message.message_id
    context.user_data["bot_message_id"] = bot_message.message_id

# Callback handler for "список карточек"
async def main_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "Вот список всех карточек:\n"
    buttons = []

    for idx, (folder_key, folder_data) in enumerate(FOLDERS.items(), start=1):
        text += f"{idx}. {folder_data['display_name']}\n"
        buttons.append(InlineKeyboardButton(str(idx), callback_data=f"folder_{folder_key}"))

    # Create "⬅️ Назад" and "❌ Удалить" buttons
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data="back_to_commands")
    delete_button = InlineKeyboardButton("❌ Удалить", callback_data="delete_message")

    # Arrange buttons dynamically into rows
    keyboard = arrange_buttons(buttons, max_columns=5, back_button=back_button, delete_button=delete_button)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, reply_markup=reply_markup)

# Callback handler for "список стикеров"
async def main_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "Вот список всех стикеров:\n"
    buttons = []

    for idx, (sticker_key, sticker_data) in enumerate(STICKERS.items(), start=1):
        text += f"{idx}. {sticker_data['display_name']}\n"
        buttons.append(InlineKeyboardButton(str(idx), callback_data=f"sticker_{sticker_key}"))

    # Create "⬅️ Назад" and "❌ Удалить" buttons
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data="back_to_commands")
    delete_button = InlineKeyboardButton("❌ Удалить", callback_data="delete_message")

    # Arrange buttons dynamically into rows
    keyboard = arrange_buttons(buttons, max_columns=5, back_button=back_button, delete_button=delete_button)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, reply_markup=reply_markup)

# Callback handler for "назад" button to return to main menu
async def back_to_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        # Edit the message to display the main menu
        text = "Выберите опцию:\n1. Список карточек\n2. Список стикеров\n3. Полезные ссылки/статьи"
        buttons = [
            InlineKeyboardButton("1", callback_data="main_cards"),
            InlineKeyboardButton("2", callback_data="main_stickers"),
            InlineKeyboardButton("3", callback_data="useful_links"),
            InlineKeyboardButton("❌ Удалить", callback_data="delete_message")
        ]

        # Arrange buttons into rows
        keyboard = arrange_buttons(buttons, max_columns=3)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text, reply_markup=reply_markup)

# Callback handler for folder selection
async def folder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    folder_key = query.data.split("_")[1]
    folder_data = FOLDERS.get(folder_key)

    if not folder_data:
        await query.edit_message_text("Папка с карточками не найдена.")
        return

    # Check if the folder has subfolders
    subfolders = folder_data.get("subfolders", {})
    pictures = folder_data.get("pictures", {})

    if not subfolders and not pictures:
        await query.edit_message_text(f"Папка '{folder_data['display_name']}' пустая.")
        return

    text = f"Вы выбрали '{folder_data['display_name']}'\nВот список содержимого:\n"
    buttons = []

    # Add subfolders to the list
    for idx, (subfolder_key, subfolder_data) in enumerate(subfolders.items(), start=1):
        text += f"{idx}. {subfolder_data['display_name']}\n"
        buttons.append(InlineKeyboardButton(str(idx), callback_data=f"subfolder_{folder_key}_{subfolder_key}"))

    # Add pictures to the list
    for idx, (file_name, custom_name) in enumerate(pictures.items(), start=len(subfolders) + 1):
        text += f"{idx}. {custom_name}\n"
        buttons.append(InlineKeyboardButton(str(idx), callback_data=f"picture_{folder_key}_{file_name}"))

    # Create "⬅️ Назад" and "❌ Удалить" buttons
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data="main_cards")
    delete_button = InlineKeyboardButton("❌ Удалить", callback_data="delete_message")

    # Arrange buttons dynamically into rows
    keyboard = arrange_buttons(buttons, max_columns=5, back_button=back_button, delete_button=delete_button)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, reply_markup=reply_markup)

# Callback handler for subfolder selection
async def subfolder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extract parent folder and subfolder keys from the callback data
    _, parent_folder_key, subfolder_key = query.data.split("_")
    parent_folder = FOLDERS.get(parent_folder_key, {})
    subfolder_data = parent_folder.get("subfolders", {}).get(subfolder_key)

    if not subfolder_data:
        await query.edit_message_text("Подпапка не найдена.")
        return

    pictures = subfolder_data.get("pictures", {})
    if not pictures:
        await query.edit_message_text(f"Подпапка '{subfolder_data['display_name']}' пустая.")
        return

    # Decide which function to use based on the folder
    if subfolder_key == "dragucci":  # Send as media groups
        await send_pictures_as_media_groups(update, context, subfolder_data)
    elif subfolder_key == "pools":  # Send one picture at a time
        await send_pictures_one_by_one(update, context, parent_folder_key, subfolder_key, subfolder_data)
    else:
        await query.message.reply_text("Эта папка не настроена для отправки.")

# Callback handler for picture selection
async def picture_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extract folder and file information from the callback data
    data_parts = query.data.split("_")
    folder_key = data_parts[1]
    file_name = data_parts[2]

    # Check if the folder exists in the FOLDERS dictionary
    folder_data = FOLDERS.get(folder_key)
    if not folder_data:
        await query.message.reply_text("Папка с карточками не найдена.")
        return

    # Construct the file path
    folder_path = folder_data["path"]
    file_path = os.path.join(folder_path, f"{file_name}.jpg")  # Assuming all files are .jpg

    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file is not found, check for subfolders
        subfolders = folder_data.get("subfolders", {})
        for subfolder_key, subfolder_data in subfolders.items():
            subfolder_path = subfolder_data["path"]
            subfolder_file_path = os.path.join(subfolder_path, f"{file_name}.jpg")
            if os.path.exists(subfolder_file_path):
                file_path = subfolder_file_path
                break
        else:
            # If the file is still not found, send an error message
            await query.message.reply_text(f"Картинка '{file_name}.jpg' не найдена.")
            return

    # Send the image
    with open(file_path, "rb") as photo:
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo)

# Callback handler for sticker selection
async def sticker_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, sticker_key = query.data.split("_")
    sticker_data = STICKERS.get(sticker_key)
    if not sticker_data:
        await query.message.reply_text("Стикер не найден.")
        return

    sticker_id = sticker_data["sticker_id"]

    # Send the specific sticker by its ID
    await context.bot.send_sticker(chat_id=query.message.chat_id, sticker=sticker_id)

    # Do not edit the catalog message; leave it unchanged

# Callback handler for "Полезные ссылки/статьи"
async def useful_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Text with clickable links
    text = (
        "Вот список полезных ссылок/статей:\n"
        "1. [Статья о составлении команд и умениях боевых элементов](https://telegra.ph/Legendy-Drakonomanii--Dragon-Mania-Legends-03-31)\n"
        "2. [DML Planner](https://dml-planner.eu/)\n"
        "3. [DML Wiki](https://www.dragon-mania-legends.wiki/wiki/Main_Page)\n"
        "4. [DML Wiki Fandom](https://dragon-mania-legends.fandom.com/ru/wiki/Dragon_Mania_Legends_Wiki)\n"
        "5. [Форум](https://t.me/drakonomaniyaa_forum)"
    )

    # Create "⬅️ Назад" and "❌ Удалить" buttons
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data="back_to_commands")
    delete_button = InlineKeyboardButton("❌ Удалить", callback_data="delete_message")

    # Arrange buttons dynamically into rows
    keyboard = arrange_buttons([], max_columns=1, back_button=back_button, delete_button=delete_button)
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Edit the message to display the links without link previews
    await query.edit_message_text(
        text, reply_markup=reply_markup, parse_mode="Markdown", disable_web_page_preview=True
    )

# Function to greet new members and store their join time
async def greet_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        username = member.username or member.first_name
        user_id = member.id
        # Store the join time in context.chat_data
        context.chat_data[user_id] = datetime.now()
        await update.message.reply_text(f"Добро пожаловать @{username}!")

# Function to say goodbye to users who leave the group and calculate time spent
async def goodbye_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.message.left_chat_member
    username = member.username or member.first_name
    user_id = member.id

    # Retrieve the join time from context.chat_data
    join_time = context.chat_data.get(user_id)
    if join_time:
        time_spent = datetime.now() - join_time
        # Calculate time components
        years, remainder = divmod(time_spent.days, 365)
        months, days = divmod(remainder, 30)
        hours, remainder = divmod(time_spent.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Dynamically construct the time string with non-zero components
        time_components = []
        if years > 0:
            time_components.append(f"{years}y")
        if months > 0:
            time_components.append(f"{months}m")
        if days > 0:
            time_components.append(f"{days}d")
        if hours > 0:
            time_components.append(f"{hours}h")
        if minutes > 0:
            time_components.append(f"{minutes}m")
        if seconds > 0:
            time_components.append(f"{seconds}s")

        time_spent_str = " ".join(time_components)
        await update.message.reply_text(
            f"Пока пока @{username}!\nПользователь был с нами: {time_spent_str}"
        )
        # Remove the user from chat_data
        del context.chat_data[user_id]
    else:
        await update.message.reply_text(f"Пока пока @{username}!")

# Function to send pictures as media groups
async def send_pictures_as_media_groups(update: Update, context: ContextTypes.DEFAULT_TYPE, subfolder_data):
    query = update.callback_query
    subfolder_path = subfolder_data["path"]
    pictures = subfolder_data.get("pictures", {})

    # Prepare media groups
    media_group = []
    for idx, (file_name, custom_name) in enumerate(pictures.items(), start=1):
        file_path = os.path.join(subfolder_path, f"{file_name}.jpg")  # Assuming all files are .jpg
        if os.path.exists(file_path):
            with open(file_path, "rb") as photo:
                media_group.append(InputMediaPhoto(media=photo, caption=custom_name if idx == 1 else None))

        # Send the media group if it reaches 10 images or it's the last image
        if len(media_group) == 10 or idx == len(pictures):
            try:
                await context.bot.send_media_group(chat_id=query.message.chat_id, media=media_group)
            except Exception as e:
                await query.message.reply_text(f"Ошибка при отправке группы: {e}")
            media_group = []  # Reset the group

# Function to send pictures one by one
async def send_pictures_one_by_one(update: Update, context: ContextTypes.DEFAULT_TYPE, parent_folder_key, subfolder_key, subfolder_data):
    query = update.callback_query
    await query.answer()

    # Extract subfolder details
    subfolder_name = subfolder_data["display_name"]
    pictures = subfolder_data.get("pictures", {})

    # Create a message with the list of pictures
    text = f"Вы выбрали '{subfolder_name}'\nВот список содержимого:\n"
    buttons = []

    for idx, (file_name, custom_name) in enumerate(pictures.items(), start=1):
        text += f"{idx}. {custom_name}\n"
        buttons.append(InlineKeyboardButton(str(idx), callback_data=f"picture_{parent_folder_key}_{subfolder_key}_{file_name}"))

    # Add "⬅️ Назад" and "❌ Удалить" buttons
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data=f"folder_{parent_folder_key}")
    delete_button = InlineKeyboardButton("❌ Удалить", callback_data="delete_message")

    # Arrange buttons dynamically into rows
    keyboard = arrange_buttons(buttons, max_columns=5, back_button=back_button, delete_button=delete_button)
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the list of options
    await query.edit_message_text(text, reply_markup=reply_markup)

# Run the bot
def main():
    # Enable persistence for user_data and chat_data
    persistence = PicklePersistence(filepath="bot_data.pkl")
    app = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("commands", commands))  # New /commands command
    app.add_handler(CommandHandler("cards", commands))  # Redirect to /commands
    app.add_handler(CommandHandler("stickers", main_stickers))  # Redirect to /commands
    app.add_handler(CallbackQueryHandler(main_cards, pattern="^main_cards$"))
    app.add_handler(CallbackQueryHandler(main_stickers, pattern="^main_stickers$"))
    app.add_handler(CallbackQueryHandler(folder_callback, pattern="^folder_"))
    app.add_handler(CallbackQueryHandler(subfolder_callback, pattern="^subfolder_"))
    app.add_handler(CallbackQueryHandler(picture_callback, pattern="^picture_"))
    app.add_handler(CallbackQueryHandler(sticker_callback, pattern="^sticker_"))
    app.add_handler(CallbackQueryHandler(useful_links, pattern="^useful_links$"))  # Useful links handler
    app.add_handler(CallbackQueryHandler(back_to_commands, pattern="^back_to_commands$"))  # Back button handler
    app.add_handler(CallbackQueryHandler(delete_message, pattern="^delete_message$"))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_members))  # New members handler
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye_member))  # Goodbye members handler

    print("Бот is running...")
    app.run_webhook(
        listen="0.0.0.0",
        port=8443,  # Use a non-restricted port
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

if __name__ == "__main__":
    while True:
        try:
            print("Starting bot...")
            main()  # Your bot's main function
        except Exception as e:
            print(f"Bot crashed with error: {e}. Restarting in 5 seconds...")
            time.sleep(5)