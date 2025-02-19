import os
import telebot
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Отправляй свое видео, получишь кружочек в ответ.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("input.mp4", 'wb') as new_file:
        new_file.write(downloaded_file)

    clip = VideoFileClip("input.mp4").subclip(0, 60)
    (w, h) = clip.size
    crop_size = min(w, h)
    clip_cropped = crop(clip, width=crop_size, height=crop_size, x_center=w/2, y_center=h/2)
    clip_cropped.write_videofile("output.mp4")

    with open("output.mp4", 'rb') as video:
        bot.send_video(message.chat.id, video)

bot.polling()