from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram import InputFile
# from telegram.error import BadRequest
from speechkit import Session, SpeechSynthesis, ShortAudioRecognition
from dotenv import load_dotenv
from io import BytesIO
import openai
import os
from functools import wraps

load_dotenv()

TOKEN = os.environ.get("TOKEN")
GPT_SECRET_KEY = os.environ.get("GPT_SECRET_KEY")
SK_TOKEN = os.environ.get("SK_TOKEN")
CATALOG_ID = os.environ.get("CATALOG_ID")
USER_LIST = os.environ.get("ADMINS")
ALLOWED_USERS = [int(user_id) for user_id in USER_LIST.split(',')]

openai.api_key = GPT_SECRET_KEY

# экземпляр класса `Session` и авторизация по токену и id
session = Session.from_yandex_passport_oauth_token(SK_TOKEN, CATALOG_ID)

TEXT_VOICE = 'voice'
MAN_VOICE = 'madirus'

def user_allowed(func):
    @wraps(func)
    async def wrapper(update, context):
        if update.message.from_user.id not in ALLOWED_USERS:
            txt = f'{update.message.from_user.username} <code>{update.message.from_user.id}</code>'
            await update.message.reply_text(f"{txt}\nВы не допущены к использованию тестового бота...", parse_mode='HTML')
            return
        return await func(update, context)
    return wrapper

keyboard_voice = [
    [
        InlineKeyboardButton("🗣 Голосовой режим", callback_data='voice'),
        InlineKeyboardButton("📄 Текстовый режим", callback_data='text'),
    ],
    [
        InlineKeyboardButton("👧 Алена", callback_data='alena'),
        InlineKeyboardButton("🧔‍♂️ Филипп", callback_data='filipp'),
        InlineKeyboardButton("👩🏻‍🦱 Джейн", callback_data='jane'),
        InlineKeyboardButton("👳🏻‍♂️ Мадирус", callback_data='madirus'),
    ]
]

keyboard_text = [
    [
        InlineKeyboardButton("🗣 Голосовой режим", callback_data='voice'),
        InlineKeyboardButton("📄 Текстовый режим", callback_data='text'),
    ]
]

keyboard = lambda: keyboard_voice if TEXT_VOICE == 'voice' else keyboard_text

#@user_allowed  # Этот декоратор ограничивает доступ к функции
async def voice_command(update, context):
    reply_markup = InlineKeyboardMarkup(keyboard())
    txt = f'⚙️ Установлен режим: <b>{TEXT_VOICE}</b>\n🎼 Выбран голос: <b>{MAN_VOICE}</b>'
    await update.message.reply_text(txt, reply_markup=reply_markup, parse_mode='HTML')

#@user_allowed  # Этот декоратор ограничивает доступ к функции
async def button(update, context):
    global TEXT_VOICE, MAN_VOICE
    query = update.callback_query

    old_text_voice = TEXT_VOICE
    old_man_voice = MAN_VOICE

    if query.data in ['voice', 'text']:
        TEXT_VOICE = query.data
    else:
        MAN_VOICE = query.data

    reply_markup = InlineKeyboardMarkup(keyboard())
    if old_text_voice != TEXT_VOICE or old_man_voice != MAN_VOICE:
        txt = f'⚙️ Установлен режим: <b>{TEXT_VOICE}</b>\n🎼 Выбран голос: <b>{MAN_VOICE}</b>'
        await query.edit_message_text(text=txt, reply_markup=reply_markup, parse_mode='HTML')


#@user_allowed  # Этот декоратор ограничивает доступ к функции
async def get_answer(text):
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-0301",
        messages=[{"role": "user", "content": text}])
    return completion.choices[0].message["content"]

@user_allowed  # Этот декоратор ограничивает доступ к функции
async def start(update, context):
    txt = f'\n🎼 Для смены настроек выполните команду <b>/voice</b>'
    await update.message.reply_text(f'📡 Задайте любой вопрос chatGPT...{txt}', parse_mode='HTML')

@user_allowed  # Этот декоратор ограничивает доступ к функции
async def help_command(update, context):
    txt = f'\n🎤 Для отправки голосового сообщения зажмите справа внизу иконку микрофона и удерживайте до окончания записи...'
    txt = f'{txt}\n🎼 Для смены настроек выполните команду <b>/voice</b>'
    await update.message.reply_text(f'💡 Вы можете пообщаться с chatGPT на любую тему.{txt}', parse_mode='HTML')

@user_allowed  # Этот декоратор ограничивает доступ к функции
async def gpt(update, context):
    user = update.message.from_user  # Получение данных user отправителя

    if TEXT_VOICE == 'voice':
        if update.message.voice is not None:
            # получаем файл аудиосообщения от пользователя
            file = await update.message.voice.get_file()
            byte_voice = await file.download_as_bytearray()
            # экземпляр класса распознавания речи
            recognizeShortAudio = ShortAudioRecognition(session)
            # выполняем распознавание речи
            text = recognizeShortAudio.recognize(BytesIO(byte_voice), sampleRateHertz='48000')
            await update.message.reply_text(text)
        else:
            txt = '‼️ Ожидалось голосовое сообщение, но оно не было получено. Пожалуйста, попробуйте ввод еще раз или <b>/help</b>'
            await update.message.reply_text(txt, parse_mode='HTML')
            return
    else:
        text = update.message.text

    # Запись user_id и запроса в файл
    with open("/app/data/requests.txt", "a", encoding="utf-8") as file:
        file.write(f"🔸{user.username} [{user.id}]: 🎼 {text}\n")
    # print(f'\n🔸{user.username} [{user.id}]: 🎼 {text}\n')
    # отправляем текст в chatGPt
    res = await get_answer(text)

    if TEXT_VOICE == 'voice':
        # Создаем экземляр класса `SpeechSynthesis`, передавая `session`
        synthesizeAudio = SpeechSynthesis(session)
        gen_voice = synthesizeAudio.synthesize_stream(text=res,
                                    voice=MAN_VOICE,  # 'madirus',
                                    speed=1.0,
                                    sampleRateHertz='48000')
        # Сохранение текстового контента в файл
        file_path = "gpt_response.md"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(res)
        # Отправка файла вместо текстового сообщения
        with open(file_path, "rb") as file:
            await update.message.reply_document(document=file)
        # Отправка звукового файла
        await update.message.reply_voice(gen_voice)
    else:
        # Отправка текстового контента пользователю в виде сообщения Markdown
        await update.message.reply_text(f'🔰 {res}')

def main():
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    application.add_handler(CommandHandler("start", start, block=False))
    application.add_handler(CommandHandler("help", help_command, block=False))
    application.add_handler(CommandHandler('voice', voice_command, block=False))
    application.add_handler(MessageHandler(filters.TEXT | filters.VOICE, gpt, block=False))
    application.add_handler(CallbackQueryHandler(button))

    # запуск приложения. Для остановки нужно нажать Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
