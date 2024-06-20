from utils import bot, types, tempfile, Image, bot_data, io, VideoFileClip, \
    os, threading, time, compression_levels, mimetypes


@bot.message_handler(commands=['start'])
def start(message):
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    select_level_button = types.KeyboardButton("Выбрать уровень сжатия")
    markup.add(select_level_button)
    text = f'<b>Привет, {first_name} {last_name}!</b> \nДобро пожаловать в "ShakalRofl".'
    text += '\n\nЭтот бот изменяет качество <b>изображений</b> и <b>видео</b> в худшую сторону.'
    text += '\nЧтобы начать изменение качества выбери уровень сжатия.'
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')


@bot.message_handler(commands=['select_level'])
def return_select_level_compress(message):
    select_level_compress(message)


@bot.message_handler(func=lambda message: message.text == "Выбрать уровень сжатия")
def select_level_compress(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    low_button = types.KeyboardButton("Сильный")
    middle_button = types.KeyboardButton("Средний")
    high_button = types.KeyboardButton("Слабый")
    markup.add(low_button, middle_button, high_button)

    text = "Выбери уровень сжатия для изображения."
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in compression_levels.keys())
def set_compression_level(message):
    selected_level = message.text
    compression_level = compression_levels[selected_level]
    bot_data[message.chat.id] = compression_level
    markup = types.ReplyKeyboardRemove()
    text = 'Пришли мне изображение или видео.'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['document', 'photo', 'video'])
def compress_media(message):
    arg_level = bot_data.get(message.chat.id)
    if arg_level is None:
        bot.send_message(message.chat.id, "Пожалуйста, выбери уровень сжатия сначала.")
        return

    if message.content_type == 'photo':
        compress_image(message, arg_level['photo'])
    elif message.content_type == 'video':
        compress_video(message, arg_level['video'], arg_level['audio'])
    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith('image'):
            compress_image(message, arg_level['photo'])
        elif mime_type and mime_type.startswith('video'):
            compress_video(message, arg_level['video'], arg_level['audio'])
        else:
            bot.send_message(message.chat.id, "Файл не является изображением или видео.")


def compress_image(message, photo_level):
    if message.document:
        waiting_message = init_waiting(message)
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = Image.open(io.BytesIO(downloaded_file))
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = Image.open(io.BytesIO(downloaded_file))
    img = img.convert("RGB")
    compressed_image = io.BytesIO()
    img.save(compressed_image, format='JPEG', quality=photo_level)
    compressed_image.seek(0)

    text = 'Вот твоё зашакаленное изображение.\n' \
           'Если хочешь ещё, то отправь новый файл с изображением или видео.\n'
    bot.send_photo(message.chat.id, compressed_image, caption=text)
    if message.document:
        bot.delete_message(message.chat.id, waiting_message.message_id)
    compressed_image.close()


def compress_video(message, video_level, audio_level):
    waiting_message = init_waiting(message)

    if message.document:
        file_info = bot.get_file(message.document.file_id)
    else:
        file_info = bot.get_file(message.video.file_id)
    downloaded_video = bot.download_file(file_info.file_path)

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
        temp_video.write(downloaded_video)
        temp_video_path = temp_video.name

    video_clip = VideoFileClip(temp_video_path)
    compressed_video_path = tempfile.mktemp(suffix=".mp4")

    video_clip.write_videofile(
        compressed_video_path,
        codec="libx264",
        audio_codec='aac',
        bitrate=f'{video_level}k',
        audio_bitrate=f'{audio_level}k'
    )

    with open(compressed_video_path, 'rb') as video_file:
        text = 'Вот твоё зашакаленное видео.\n' \
               'Если хочешь ещё, то отправь новый файл с изображением или видео.\n'
        bot.send_video(message.chat.id, video_file, caption=text)
        bot.delete_message(message.chat.id, waiting_message.message_id)

    os.remove(temp_video_path)
    os.remove(compressed_video_path)


def init_waiting(message):
    waiting_message = bot.send_message(message.chat.id, "Подождите немного, идёт обработка")

    animation_thread = threading.Thread(target=waiting_animation,
                                        args=(message.chat.id, waiting_message.message_id))
    animation_thread.start()

    return waiting_message


def waiting_animation(chat_id, message_id):
    frames = ["⏳", "⌛", "⏳", "⌛"]
    while True:
        for frame in frames:
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text=f"Подождите немного, идёт обработка{frame}")
                time.sleep(0.5)
            except:
                return


@bot.message_handler(func=lambda message: True)
def true_message(message):
    bot.send_message(message.chat.id, "Упссс, что-то пошло не так...")


bot.polling(none_stop=True)
