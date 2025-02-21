import telebot
import os
import moviepy.editor as mp
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Отправляй свое видео, получишь кружочек в ответ.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "Обрабатываю видео...")
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем видео
    input_path = "input.mp4"
    with open(input_path, "wb") as new_file:
        new_file.write(downloaded_file)

    # Обрезаем до 60 секунд и создаем кружочек
    output_path = "output.mp4"
    clip = mp.VideoFileClip(input_path).subclip(0, min(60, message.video.duration))
    clip = clip.resize(height=640).set_fps(30).set_duration(clip.duration)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Отправляем результат
    with open(output_path, "rb") as video:
        bot.send_video_note(message.chat.id, video)

    # Удаляем файлы
    os.remove(input_path)
    os.remove(output_path)

bot.polling(none_stop=True)
