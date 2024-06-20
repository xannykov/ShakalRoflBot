import telebot, PIL, io, os, tempfile, threading, time, mimetypes
from PIL import Image
from telebot import types
from moviepy.editor import VideoFileClip

bot = telebot.TeleBot('TOKEN')

compression_levels = {
    "Сильный": {"photo": 3, "video": 150, "audio": 16},
    "Средний": {"photo": 6, "video": 300, "audio": 32},
    "Слабый": {"photo": 10, "video": 600, "audio": 64}
}

bot_data = {}
