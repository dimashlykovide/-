import logging
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatJoinRequestHandler, ContextTypes
from telegram.constants import ParseMode

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "8658602081:AAEBfzXMQakAk0eStYxpTY0S-0e1yg4bdq0"
POST_LINK = "https://t.me/c/2645114369/73"  # Ссылка на пост с гайдом

# Пути к изображениям
FIRST_IMAGE_PATH = "gleb_photo.jpg"  # Изображение для первого сообщения (знакомство)
SECOND_IMAGE_PATH = "gleb1.jpg"  # Изображение для второго сообщения (проект)

# Проверяем наличие изображений
if os.path.exists(FIRST_IMAGE_PATH):
    logger.info(f"✅ Изображение для первого сообщения найдено: {FIRST_IMAGE_PATH}")
else:
    logger.warning(f"⚠️ Изображение для первого сообщения не найдено: {FIRST_IMAGE_PATH}")

if os.path.exists(SECOND_IMAGE_PATH):
    logger.info(f"✅ Изображение для второго сообщения найдено: {SECOND_IMAGE_PATH}")
else:
    logger.warning(f"⚠️ Изображение для второго сообщения не найдено: {SECOND_IMAGE_PATH}")

def create_post_button():
    """Создает кнопку для перехода к посту"""
    keyboard = [[InlineKeyboardButton("📖 Читать пост + гайд", url=POST_LINK)]]
    return InlineKeyboardMarkup(keyboard)

async def send_first_message_with_photo(user_id: int, user_first_name: str, context: ContextTypes.DEFAULT_TYPE):
    """Отправка первого сообщения с фото (знакомство) - используем имя пользователя"""
    try:
        # Текст первого сообщения с HTML форматированием
        first_message_text = f"""<b>Привет</b>, {user_first_name}. Давай знакомиться

Меня зовут Глеб. Мне всего 18 лет и в свои годы я уже перепробовал разные способы заработка

От работы в найме и написания отзывов за копейки до реально прибыльной ниши

<blockquote>Если бы не РКО, то я бы никогда не выбрался из ямы шабашек и одноразовых темок</blockquote>

Я знаю какого это не иметь денег в кармане, не видеть перспектив и каждый день просыпаться с мыслью что ненавидишь свою жизнь

И именно поэтому я создал канал BLACKHOLE и знаю как тебе помочь

👇👇👇"""
        
        # Отправляем изображение с подписью, если файл существует
        if os.path.exists(FIRST_IMAGE_PATH):
            try:
                with open(FIRST_IMAGE_PATH, 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=user_id,
                        photo=photo,
                        caption=first_message_text,
                        parse_mode=ParseMode.HTML
                    )
                logger.info(f"📸 Первое сообщение с фото и форматированием отправлено для {user_first_name}")
            except Exception as photo_error:
                logger.error(f"❌ Ошибка отправки первого фото: {photo_error}")
                # Если фото не отправилось, отправляем только текст с форматированием
                await context.bot.send_message(
                    chat_id=user_id,
                    text=first_message_text,
                    parse_mode=ParseMode.HTML
                )
                logger.info(f"📝 Первое сообщение с форматированием без фото отправлено для {user_first_name}")
        else:
            # Если файл не найден, отправляем только текст с форматированием
            await context.bot.send_message(
                chat_id=user_id,
                text=first_message_text,
                parse_mode=ParseMode.HTML
            )
            logger.info(f"📝 Первое сообщение с форматированием без фото отправлено для {user_first_name}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке первого сообщения: {e}")

async def send_second_message_with_photo(user_id: int, user_first_name: str, context: ContextTypes.DEFAULT_TYPE):
    """Функция для отправки второго сообщения с фото через 5 секунд"""
    await asyncio.sleep(5)  # Ждем 5 секунд
    
    try:
        # Текст второго сообщения
        second_message_text = """<b>BLACKHOLE</b> — это проект посвященный онлайн-заработку

Я не сливаю деньги на крипте и прочей ерунде, а строю систему заработка на сотрудничестве с банками

<blockquote>Речь идёт про РКО и другие финансовые продукты</blockquote>

Сейчас советую тебе ознакомиться с этим постом чтобы войти в курс дела

Там же я подготовил для вас бесплатный ГАЙД в который входит:

<blockquote>- Понятие ниши мотивированного трафика
- С чего лучше всего начать
- Как масштабироваться
</blockquote>
И секретный подарок который ждет тебя после прочтения"""
        
        # Отправляем изображение с подписью, если файл существует
        if os.path.exists(SECOND_IMAGE_PATH):
            try:
                with open(SECOND_IMAGE_PATH, 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=user_id,
                        photo=photo,
                        caption=second_message_text,
                        parse_mode=ParseMode.HTML,
                        reply_markup=create_post_button()
                    )
                logger.info(f"📸 Второе сообщение с фото и кнопкой отправлено для {user_first_name}")
            except Exception as photo_error:
                logger.error(f"❌ Ошибка отправки второго фото: {photo_error}")
                # Если фото не отправилось, отправляем текст с кнопкой
                await context.bot.send_message(
                    chat_id=user_id,
                    text=second_message_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=create_post_button()
                )
                logger.info(f"📝 Второе сообщение с кнопкой без фото отправлено для {user_first_name}")
        else:
            # Если файл не найден, отправляем только текст с кнопкой
            await context.bot.send_message(
                chat_id=user_id,
                text=second_message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=create_post_button()
            )
            logger.info(f"📝 Второе сообщение с кнопкой без фото отправлено для {user_first_name}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке второго сообщения: {e}")

async def chat_join_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Автоматическое принятие заявки и отправка приветствия
    """
    user = update.chat_join_request.from_user
    
    # Используем только имя пользователя (first_name)
    user_name = user.first_name or "Пользователь"
    logger.info(f"Пользователь: {user_name} (ID: {user.id})")
    
    try:
        # Автоматически принимаем заявку
        await update.chat_join_request.approve()
        logger.info(f"✅ Заявка принята: {user_name}")
        
        # Отправляем первое сообщение с фото и форматированием
        await send_first_message_with_photo(user.id, user_name, context)
        
        # Запускаем задачу для отправки второго сообщения с фото через 5 секунд
        asyncio.create_task(send_second_message_with_photo(user.id, user_name, context))
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        
        if "bot was blocked" in str(e).lower():
            logger.warning(f"Пользователь {user_name} заблокировал бота")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    await update.message.reply_text(
        "👋 Я бот канала BLACKHOLE. Если ты подал заявку на вступление, я автоматически её приму и отправлю информацию."
    )

def main():
    """Запуск бота"""
    logger.info("=" * 50)
    logger.info("🤖 Бот BLACKHOLE запущен!")
    logger.info("=" * 50)
    logger.info(f"🔗 Ссылка на пост с гайдом: {POST_LINK}")
    logger.info(f"🖼  Первое изображение: {FIRST_IMAGE_PATH}")
    logger.info(f"🖼  Второе изображение: {SECOND_IMAGE_PATH}")
    logger.info("👤 Используется имя пользователя (first_name)")
    logger.info("📨 Первое сообщение: Знакомство + фото + форматирование")
    logger.info("📨 Второе сообщение: Описание проекта BLACKHOLE + фото + кнопка")
    logger.info("⏰ Второе сообщение отправляется через 5 секунд")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(ChatJoinRequestHandler(chat_join_request_handler))
    
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()