from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from yandex_client import yandex_client
from handlers.callback_handler import user_playback

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Если это команда, используем context.args, иначе берем текст сообщения
    if context.args:
        query = ' '.join(context.args)
    else:
        query = update.message.text.strip() if update.message and update.message.text else ''

    if not query:
        await update.message.reply_text("Пожалуйста, укажи поисковый запрос: /search <название или артист>")
        return
    
    # 🔍 ШАГ 1: Отправляем промежуточное сообщение для быстрого отклика
    status_message = await update.message.reply_text("🔍 Идёт поиск треков в Yandex Music...")
    
    try:
        # 🔍 ШАГ 2: Проверяем доступность Yandex клиента
        if not yandex_client.is_available():
            await status_message.edit_text("❌ Yandex Music недоступен. Попробуйте позже.")
            return
        
        # 🔍 ШАГ 3: Ищем треки через Yandex
        tracks = yandex_client.search_track(query)
        
        if not tracks:
            # ❌ Если ничего не найдено, обновляем сообщение
            await status_message.edit_text("❌ Треки не найдены в Yandex Music. Попробуйте другой запрос.")
            return

        # ✅ ШАГ 4: Сохраняем результаты для пользователя
        user_playback[update.effective_user.id] = tracks
        
        # 🎵 ШАГ 5: Создаем кнопки с эмодзи
        buttons = []
        for i, track in enumerate(tracks):
            title = track.get('name', 'Unknown')
            artist = track.get('artist', [{}])[0].get('name', 'Unknown')
            buttons.append([InlineKeyboardButton(
                f"🎵 {i+1}. {title} - {artist}", 
                callback_data=str(i)
            )])
        
        markup = InlineKeyboardMarkup(buttons)
        
        # ✅ ШАГ 6: Обновляем сообщение с результатами
        await status_message.edit_text(
            f"✅ Найдено {len(tracks)} треков в Yandex Music\n"
            f"🎵 Выберите трек для скачивания",
            reply_markup=markup
        )
        
    except Exception as e:
        # ❌ ШАГ 7: Обработка ошибок
        await status_message.edit_text(f"❌ Ошибка при поиске: {str(e)}")